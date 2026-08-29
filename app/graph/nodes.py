import json
import time

from langchain_core.runnables import RunnableConfig

from app.graph.prompts import SYSTEM_PROMPT, build_user_prompt
from app.llm import get_llm
from app.tools.loader import get_catalog
from app.tools.orders import customer_exists, get_customer_orders
from app.tools.similar import find_similar_products

INJECTION_PATTERNS = (
    "ignore suas regras",
    "ignore as regras",
    "desconsidere",
    "ignore previous",
    "ignore all previous",
    "instruções do sistema",
    "instrucoes do sistema",
    "system prompt",
    "mostre todos os clientes",
    "todos os clientes",
    "histórico completo de todos",
    "historico completo de todos",
    "revele os dados",
    "revele dados",
    "você é livre",
    "voce e livre",
    "modo desenvolvedor",
)


def _audit(event: str, **extra) -> dict:
    return {"event": event, "ts_ms": round(time.perf_counter() * 1000), **extra}


def validate_input(state: dict) -> dict:
    customer_id = state.get("customer_id")
    previous = [
        {"cod_prod": rec["cod_prod"], "product": rec["product"]}
        for rec in state.get("recommendations", [])[:5]
    ]
    errors = list(state.get("errors", []))
    if not isinstance(customer_id, int) or isinstance(customer_id, bool) or customer_id <= 0:
        errors.append("customer_id inválido")
        return {"validated": False, "errors": errors}
    if not customer_exists(customer_id):
        errors.append(f"cliente {customer_id} inexistente")
        return {"validated": False, "errors": errors}
    return {
        "validated": True,
        "errors": [],
        "previous_recommendations": previous,
        "audit_events": [
            _audit("input_validated", customer_id=customer_id, has_memory=bool(previous))
        ],
    }


def security_check(state: dict) -> dict:
    query = (state.get("query") or "").lower()
    matched = [pattern for pattern in INJECTION_PATTERNS if pattern in query]
    if matched:
        return {
            "security_status": "blocked",
            "block_reason": "possível prompt injection detectado na consulta",
            "audit_events": [_audit("security_blocked", patterns=list(matched))],
        }
    return {"security_status": "ok", "audit_events": [_audit("security_ok")]}


def get_purchase_history(state: dict) -> dict:
    result = get_customer_orders(state["customer_id"])
    return {
        "purchase_history": [item.model_dump() for item in result.items],
        "audit_events": [
            _audit("history_retrieved", items=len(result.items), orders=result.orders_count)
        ],
    }


def find_similar_products_node(state: dict) -> dict:
    result = find_similar_products(state["customer_id"], limit=5)
    return {
        "similar_products": [item.model_dump() for item in result],
        "audit_events": [_audit("similar_retrieved", count=len(result))],
    }


def parse_recommendations(text: str, catalog: dict) -> list[dict]:
    start = text.find("[")
    end = text.rfind("]")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("resposta do LLM sem array JSON")
    data = json.loads(text[start : end + 1])
    recommendations = []
    for item in data:
        cod_prod = int(item["cod_prod"])
        if cod_prod not in catalog:
            continue
        confidence = max(0.0, min(float(item.get("confidence", 0.5)), 1.0))
        recommendations.append(
            {
                "cod_prod": cod_prod,
                "product": catalog[cod_prod]["produto"],
                "reason": str(item.get("reason", ""))[:200],
                "confidence": round(confidence, 2),
            }
        )
    return recommendations


def generate_recommendations(state: dict, config: RunnableConfig | None = None) -> dict:
    history = state.get("purchase_history", [])
    if not history:
        return {"llm_recommendations": [], "fallback_used": True}

    llm = (config or {}).get("configurable", {}).get("llm")
    if llm is None:
        llm = get_llm()

    catalog = get_catalog()
    similar = state.get("similar_products", [])
    prompt = build_user_prompt(state["customer_id"], history, similar, catalog)
    try:
        response = llm.invoke([("system", SYSTEM_PROMPT), ("human", prompt)])
        parsed = parse_recommendations(response.content, catalog)
        return {
            "llm_recommendations": parsed,
            "fallback_used": False,
            "errors": [],
            "audit_events": [_audit("recommendation_generated", count=len(parsed), source="llm")],
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "llm_recommendations": [],
            "fallback_used": True,
            "errors": [f"geração por LLM falhou: {exc}"],
            "audit_events": [_audit("llm_failed", error=str(exc)[:120])],
        }


def validate_recommendations(state: dict) -> dict:
    catalog = get_catalog()
    valid = []
    for rec in state.get("llm_recommendations", []):
        if rec["cod_prod"] not in catalog or any(rec["cod_prod"] == v["cod_prod"] for v in valid):
            continue
        valid.append(rec)
    valid = valid[:5]

    if not valid:
        valid = [
            {
                "cod_prod": item["cod_prod"],
                "product": item["produto"],
                "reason": "Produto comprado com frequência junto com itens do seu histórico",
                "confidence": item["confidence"],
            }
            for item in state.get("similar_products", [])[:5]
        ]

    return {
        "recommendations": valid,
        "audit_events": [_audit("recommendations_validated", count=len(valid))],
    }


def block_request(state: dict) -> dict:
    return {
        "audit_events": [_audit("request_blocked", reason=state.get("block_reason", ""))],
    }


def _build_profile(history: list[dict]) -> dict:
    if not history:
        return {}
    orders = {item["pedido"] for item in history}
    counts: dict[str, int] = {}
    for item in history:
        counts[item["categoria"]] = counts.get(item["categoria"], 0) + 1
    favorites = sorted(counts, key=counts.get, reverse=True)[:3]
    if len(orders) >= 12:
        frequency = "high"
    elif len(orders) >= 7:
        frequency = "medium"
    else:
        frequency = "low"
    profile = {
        "purchase_frequency": frequency,
        "favorite_categories": favorites,
        "orders_count": len(orders),
    }
    return profile


def finalize_response(state: dict) -> dict:
    if state.get("security_status") == "blocked":
        status = "blocked"
    elif not state.get("validated", False):
        status = "error"
    else:
        status = "success"

    if status == "success":
        recommendations = state.get("recommendations", [])
        fallback_used = bool(state.get("fallback_used"))
    else:
        recommendations = []
        fallback_used = False

    output = {
        "request_id": state.get("request_id", "n/a"),
        "customer_id": state.get("customer_id"),
        "status": status,
        "customer_profile": _build_profile(state.get("purchase_history", [])),
        "recommendations": recommendations,
        "previous_recommendations": state.get("previous_recommendations", []),
        "fallback_used": fallback_used,
        "errors": list(state.get("errors", [])),
    }
    if status == "blocked":
        output["reason"] = state.get("block_reason", "")
    return {
        "output": output,
        "audit_events": [_audit("response_completed", status=status)],
    }
