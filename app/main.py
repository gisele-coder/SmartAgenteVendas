from typing import Annotated
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException
from langchain_openai import ChatOpenAI

from app.config import settings
from app.graph.builder import run_recommendation
from app.llm import get_llm
from app.observability.logging_config import setup_logging
from app.observability.metrics import snapshot
from app.schemas import RecommendationRequest, RecommendationResponse

setup_logging()

app = FastAPI(
    title="SmartOrder AI",
    description="Agente Inteligente de Pedidos e Recomendações",
    version="0.3.0",
)


def get_llm_service():
    return get_llm()


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "smartorder-ai", "model": settings.llm_model}


@app.get("/metrics")
def metrics() -> dict:
    return snapshot()


@app.post("/recomendacoes", response_model=RecommendationResponse)
def recommend(
    request: RecommendationRequest,
    llm: Annotated[ChatOpenAI, Depends(get_llm_service)],
) -> RecommendationResponse:
    request_id = uuid4().hex[:12]
    try:
        output = run_recommendation(
            {
                "request_id": request_id,
                "customer_id": request.customer_id,
                "query": request.query,
                "seed_products": request.seed_products,
            },
            llm=llm,
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="erro interno do agente") from exc
    return RecommendationResponse(**output)
