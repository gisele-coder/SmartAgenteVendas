from functools import lru_cache

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from app.graph.nodes import (
    block_request,
    finalize_response,
    find_similar_products_node,
    generate_recommendations,
    get_purchase_history,
    security_check,
    validate_input,
    validate_recommendations,
)
from app.graph.state import RecommendationState
from app.security.audit import write_audit


def route_after_validation(state: dict) -> str:
    return "security_check" if state.get("validated") else "finalize_response"


def route_after_security(state: dict) -> list[str]:
    if state.get("security_status") == "blocked":
        return ["block_request"]
    return ["get_purchase_history", "find_similar_products"]


@lru_cache(maxsize=1)
def build_graph():
    graph = StateGraph(RecommendationState)

    graph.add_node("validate_input", validate_input)
    graph.add_node("security_check", security_check)
    graph.add_node("get_purchase_history", get_purchase_history)
    graph.add_node("find_similar_products", find_similar_products_node)
    graph.add_node("generate_recommendations", generate_recommendations)
    graph.add_node("validate_recommendations", validate_recommendations)
    graph.add_node("block_request", block_request)
    graph.add_node("finalize_response", finalize_response)

    graph.add_edge(START, "validate_input")
    graph.add_conditional_edges(
        "validate_input",
        route_after_validation,
        {"security_check": "security_check", "finalize_response": "finalize_response"},
    )
    graph.add_conditional_edges("security_check", route_after_security)
    graph.add_edge("get_purchase_history", "generate_recommendations")
    graph.add_edge("find_similar_products", "generate_recommendations")
    graph.add_edge("generate_recommendations", "validate_recommendations")
    graph.add_edge("validate_recommendations", "finalize_response")
    graph.add_edge("block_request", "finalize_response")
    graph.add_edge("finalize_response", END)

    return graph.compile(checkpointer=MemorySaver())


def run_recommendation(request: dict, llm=None) -> dict:
    configurable: dict = {"thread_id": f"customer-{request.get('customer_id')}"}
    if llm is not None:
        configurable["llm"] = llm
    result = build_graph().invoke(request, config={"configurable": configurable})
    output = result["output"]
    request_id = output.get("request_id", "n/a")
    events = [
        event
        for event in result.get("audit_events", [])
        if event.get("request_id") == request_id
    ]
    write_audit(request_id, events)
    return output
