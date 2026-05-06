from app.schemas.travel import TravelResponse
from app.workflows.graph_rag_flow import GraphRAGState, run_graph_rag_flow
from app.workflows.travel_workflow import run_travel_workflow


class TravelAgentOrchestrator:
    def run(self, request: dict) -> TravelResponse:
        return run_travel_workflow(request)

    def run_state(self, request: dict) -> GraphRAGState:
        return run_graph_rag_flow(request)


def plan_trip_with_agents(request: dict) -> TravelResponse:
    return TravelAgentOrchestrator().run(request)
