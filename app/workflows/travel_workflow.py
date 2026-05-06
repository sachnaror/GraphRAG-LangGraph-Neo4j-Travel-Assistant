from app.schemas.travel import Flight, TravelResponse
from app.workflows.graph_rag_flow import run_graph_rag_flow


def run_travel_workflow(request: dict) -> TravelResponse:
    state = run_graph_rag_flow(request)
    ranked_options = state.get("ranked_options", [])

    if not ranked_options:
        raise ValueError("No valid flight options found for the requested route.")

    best = ranked_options[0]
    alternatives = ranked_options[1:4]

    return TravelResponse(
        best_flight=_to_flight(best),
        alternatives=[_to_flight(option) for option in alternatives],
        comparison=state.get("comparison", []),
        explanation=state.get("explanation", ""),
        retrieved_context=state.get("context", []),
    )


def _to_flight(option: dict) -> Flight:
    return Flight(
        flight_no=option["flight_no"],
        from_city=option["from_city"],
        to_city=option["to_city"],
        price=option["price"],
        duration_minutes=option["duration_minutes"],
        rating=option.get("rating"),
        on_time_performance=option.get("on_time_performance"),
        airline=option.get("airline"),
        is_direct=option.get("is_direct"),
        layovers=option.get("layovers", []),
    )
