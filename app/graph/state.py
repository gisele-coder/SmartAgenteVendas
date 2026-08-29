import operator
from typing import Annotated, TypedDict


class RecommendationState(TypedDict, total=False):
    request_id: str
    customer_id: int
    query: str
    validated: bool
    security_status: str
    block_reason: str
    purchase_history: list[dict]
    similar_products: list[dict]
    previous_recommendations: list[dict]
    llm_recommendations: list[dict]
    recommendations: list[dict]
    fallback_used: bool
    errors: list[str]
    output: dict
    audit_events: Annotated[list[dict], operator.add]
