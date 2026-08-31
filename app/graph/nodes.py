import json
import time

from langchain_core.runnables import RunnableConfig

from app.graph.prompts import SYSTEM_PROMPT, build_user_prompt
from app.llm import get_llm
from app.observability.logging_config import log_flow
from app.security.guard import analyze_query
from app.tools.loader import get_catalog
from app.tools.orders import customer_exists, get_customer_orders
from app.tools.similar import find_similar_products


def _audit(state: dict, event: str, **extra) -> dict:
    return {
        "event": event,
        "request_id": state.get("request_id", "n/a"),
        "ts_ms": round(time.perf_counter() * 1000),
        **extra,
    }


def validate_input(state: dict) -> dict:
    t0 = time.perf_counter()
    request_id = state.get("request_id", "n/a")
    customer_id = state.get("customer_id")
    previous = [
        {"cod_prod": rec["cod_prod"], "product": rec["product"]}
        for rec in state.get("recommendations", [])[:5]
    ]
    errors: list[str] = []
    if not isinstance(customer_id, int) or isinstance(customer_id, bool) or customer_id <= 0:
        errors.append("customer_id inválido")
        log_flow(request_id, "validate_input", _lat(t0), validated=False, reason="id inválido")
        return {"validated": False, "errors": errors}
    if not customer_exists(customer_id):
        errors.append(f"cliente {customer_id} inexistente")
        log_flow(request_id, "validate_input", _lat(t0), validated=False, reason="inexistente")
        return {"validated": False, "errors": errors}

    raw_seeds = state.get("seed_products") or []
    valid_seeds: list[int] = []
    catalog = get_catalog()
    for cod in raw_seeds:
        if not isinstance(cod, int) or isinstance(cod, bool):
            errors.append(f"código de produto inválido: {cod!r}")
            continue
        if cod not in catalog:
            errors.append(f"produto {cod} fora do catálogo (filtrado)")
            continue
        if cod not in valid_seeds:
            valid_seeds.append(cod)

    if raw_seeds and not valid_seeds:
        log_flow(
            request_id,
            "validate_input",
            _lat(t0),
            validated=False,
            reason="nenhum seed válido",
        )
        return {
            "validated": False,
            "errors": errors + ["nenhum produto válido em seed_products"],
            "seed_products": [],
        }

    log_flow(
        request_id,
        "validate_input",
        _lat(t0),
        validated=True,
        has_memory=bool(previous),
        seed_count=len(valid_seeds),
    )
    return {
        "validated": True,
        "errors": errors,
        "previous_recommendations": previous,
        "seed_products": valid_seeds,
        "audit_events": [
            _audit(state, "input_validated", customer_id=customer_id, has_memory=bool(previous))
        ],
    }


def security_check(state: dict) -> dict:
    t0 = time.perf_counter()
    request_id = state.get("request_id", "n/a")
    analysis = analyze_query(state.get("query") or "")
    if not analysis["safe"]:
        kind = analysis["kind"]
        reason = (
            "possível prompt injection detectado na consulta"
            if kind == "injection"
            else "ação destrutiva/não autorizada (limite de autonomia)"
        )
        log_flow(request_id, "security_check", _lat(t0), blocked=True, kind=kind)
        return {
            "security_status": "blocked",
            "block_reason": reason,
            "audit_events": [
                _audit(state, "security_blocked", kind=kind, patterns=analysis["patterns"][:3])
            ],
        }
    log_flow(request_id, "security_check", _lat(t0), blocked=False)
    return {"security_status": "ok", "audit_events": [_audit(state, "security_ok")]}


def get_purchase_history(state: dict) -> dict:
    t0 = time.perf_counter()
    result = get_customer_orders(state["customer_id"])
    latency = _lat(t0)
    log_flow(
        state.get("request_id", "n/a"),
        "get_purchase_history",
        latency,
        items=len(result.items),
        orders=result.orders_count,
    )
    return {
        "purchase_history": [item.model_dump() for item in result.items],
        "history_ms": latency,
        "audit_events": [
            _audit(state, "history_retrieved", items=len(result.items), orders=result.orders_count)
        ],
    }


def find_similar_products_node(state: dict) -> dict:
    t0 = time.perf_counter()
    seeds = state.get("seed_products") or []
    result = find_similar_products(state["customer_id"], limit=5, seed_products=seeds)
    latency = _lat(t0)
    log_flow(
        state.get("request_id", "n/a"),
        "find_similar_products",
        latency,
        count=len(result),
        seed=bool(seeds),
    )
    return {
        "similar_products": [item.model_dump() for item in result],
        "similar_ms": latency,
        "audit_events": [_audit(state, "similar_retrieved", count=len(result), seed=bool(seeds))],
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
    t0 = time.perf_counter()
    request_id = state.get("request_id", "n/a")
    history = state.get("purchase_history", [])
    if not history:
        return {"llm_recommendations": [], "fallback_used": True}

    llm = (config or {}).get("configurable", {}).get("llm")
    if llm is None:
        llm = get_llm()

    catalog = get_catalog()
    similar = state.get("similar_products", [])
    seeds = state.get("seed_products") or []
    prior_errors = list(state.get("errors", []))
    prompt = build_user_prompt(state["customer_id"], history, similar, catalog, seed_products=seeds)
    try:
        response = llm.invoke([("system", SYSTEM_PROMPT), ("human", prompt)])
        parsed = parse_recommendations(response.content, catalog)
        log_flow(request_id, "generate_recommendations", _lat(t0), source="llm", count=len(parsed))
        return {
            "llm_recommendations": parsed,
            "fallback_used": False,
            "errors": prior_errors,
            "audit_events": [
                _audit(state, "recommendation_generated", count=len(parsed), source="llm")
            ],
        }
    except Exception as exc:  # noqa: BLE001
        log_flow(
            request_id,
            "generate_recommendations",
            _lat(t0),
            source="fallback",
            error=str(exc)[:80],
        )
        return {
            "llm_recommendations": [],
            "fallback_used": True,
            "errors": prior_errors + [f"geração por LLM falhou: {exc}"],
            "audit_events": [_audit(state, "llm_failed", error=str(exc)[:120])],
        }


def validate_recommendations(state: dict) -> dict:
    t0 = time.perf_counter()
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

    log_flow(state.get("request_id", "n/a"), "validate_recommendations", _lat(t0), count=len(valid))
    return {
        "recommendations": valid,
        "audit_events": [_audit(state, "recommendations_validated", count=len(valid))],
    }


def block_request(state: dict) -> dict:
    t0 = time.perf_counter()
    log_flow(state.get("request_id", "n/a"), "block_request", _lat(t0))
    return {
        "audit_events": [
            _audit(state, "request_blocked", reason=state.get("block_reason", ""))
        ],
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
    t0 = time.perf_counter()
    request_id = state.get("request_id", "n/a")
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
        "request_id": request_id,
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
    log_flow(request_id, "finalize_response", _lat(t0), status=status)
    return {
        "output": output,
        "audit_events": [_audit(state, "response_completed", status=status)],
    }


def _lat(t0: float) -> float:
    return round((time.perf_counter() - t0) * 1000, 1)
