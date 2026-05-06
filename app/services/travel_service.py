from app.agents.orchestrator import plan_trip_with_agents
from app.schemas.travel import TravelResponse


def plan_trip(request: dict) -> TravelResponse:
    return plan_trip_with_agents(request)
