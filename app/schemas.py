from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    customer_id: int = Field(..., ge=1, description="Identificador do cliente")
    query: str = Field(
        "",
        max_length=500,
        description="Solicitação opcional em linguagem natural",
    )


class Recommendation(BaseModel):
    cod_prod: int
    product: str
    reason: str
    confidence: float = Field(..., ge=0, le=1)


class RecommendationResponse(BaseModel):
    request_id: str
    customer_id: int
    status: str = Field(..., description="success | blocked | error")
    customer_profile: dict = Field(default_factory=dict)
    recommendations: list[Recommendation] = Field(default_factory=list)
    previous_recommendations: list[dict] = Field(default_factory=list)
    fallback_used: bool = False
    errors: list[str] = Field(default_factory=list)
    reason: str | None = Field(None, description="Motivo do bloqueio, quando status=blocked")
