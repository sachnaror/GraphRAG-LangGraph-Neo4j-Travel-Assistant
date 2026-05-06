from app.agents.graph_agent import get_routes
from app.agents.orchestrator import TravelAgentOrchestrator
from app.graph.models import FlightNode, GraphRouteOption
from app.retrieval.retriever import get_document_retriever


def test_graph_agent_builds_direct_and_layover_options():
    routes = get_routes({"from": "Delhi", "to": "Mumbai"})

    flight_numbers = {route["flight_no"] for route in routes}
    assert "FL101" in flight_numbers
    assert "FL102+FL105" in flight_numbers


def test_retriever_returns_document_context():
    results = get_document_retriever().retrieve("business refundable flight reliability", top_k=2)

    assert results
    assert results[0].text


def test_orchestrator_exposes_graph_rag_state():
    state = TravelAgentOrchestrator().run_state(
        {"from": "Delhi", "to": "Mumbai", "priority": "business"}
    )

    assert state["route_options"]
    assert state["context"]
    assert state["ranked_options"]


def test_graph_models_build_route_option_from_flights():
    first = FlightNode.from_dict(
        {
            "flight_no": "A1",
            "airline": "Air One",
            "from": "Delhi",
            "to": "Bangalore",
            "price": 1000,
            "duration_minutes": 90,
            "rating": 4.0,
            "on_time_performance": 0.9,
        }
    )
    second = FlightNode.from_dict(
        {
            "flight_no": "A2",
            "airline": "Air Two",
            "from": "Bangalore",
            "to": "Mumbai",
            "price": 2000,
            "duration_minutes": 120,
            "rating": 4.4,
            "on_time_performance": 0.8,
        }
    )

    option = GraphRouteOption.from_flights([first, second])

    assert option.flight_no == "A1+A2"
    assert option.price == 3000
    assert option.duration_minutes == 210
    assert option.layovers == ["Bangalore"]
