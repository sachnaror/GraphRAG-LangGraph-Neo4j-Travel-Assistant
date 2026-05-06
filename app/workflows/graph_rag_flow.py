from typing import TypedDict
from time import perf_counter

from app.agents import graph_agent, planner_agent, rag_agent, validator_agent
from app.llm.client import generate_explanation
from app.memory.session_store import session_store
from app.observability.metrics import metrics
from app.services.comparison_service import build_comparison
from app.services.scoring_service import score_options
from app.services.validation_service import validate_travel_request


class GraphRAGState(TypedDict, total=False):
    request: dict
    route_options: list[dict]
    context: list[str]
    planned_options: list[dict]
    valid_options: list[dict]
    ranked_options: list[dict]
    comparison: list[dict]
    explanation: str


def run_graph_rag_flow(request: dict) -> GraphRAGState:
    start = perf_counter()
    metrics.increment("travel_workflow.requests")
    request_validation = validate_travel_request(request)
    if not request_validation.is_valid:
        metrics.increment("travel_workflow.validation_errors")
        raise ValueError("; ".join(request_validation.errors))

    priority = request.get("priority") or request.get("type") or "balanced"
    state: GraphRAGState = {"request": request}

    state["route_options"] = graph_agent.get_routes(request)
    state["context"] = rag_agent.retrieve_context(request)
    state["planned_options"] = planner_agent.build_options(
        state["route_options"],
        request,
        state["context"],
    )
    state["valid_options"] = validator_agent.validate_options(state["planned_options"], request)
    state["ranked_options"] = score_options(state["valid_options"], priority)

    if state["ranked_options"]:
        best = state["ranked_options"][0]
        alternatives = state["ranked_options"][1:4]
        state["comparison"] = build_comparison(state["ranked_options"][:4])
        state["explanation"] = generate_explanation(
            best,
            alternatives,
            state["comparison"],
            priority,
            state["context"],
        )
    else:
        state["comparison"] = []
        state["explanation"] = ""

    session_id = request.get("session_id")
    if session_id:
        session_store.append(
            session_id,
            "travel_plan",
            {
                "request": request,
                "best_flight": state["ranked_options"][0]["flight_no"] if state["ranked_options"] else None,
            },
        )

    metrics.observe("travel_workflow.duration_seconds", perf_counter() - start)
    return state
