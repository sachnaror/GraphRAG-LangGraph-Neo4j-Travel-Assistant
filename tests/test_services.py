from app.services.travel_service import plan_trip


def test_plan_trip_returns_best_flight_for_delhi_mumbai():
    response = plan_trip({"from": "Delhi", "to": "Mumbai", "user_id": "U1", "priority": "time"})

    assert response.best_flight.from_city == "Delhi"
    assert response.best_flight.to_city == "Mumbai"
    assert response.best_flight.flight_no
    assert response.comparison
    assert response.explanation
    assert response.retrieved_context


def test_plan_trip_raises_when_route_not_found():
    try:
        plan_trip({"from": "Nowhere", "to": "Mumbai"})
    except ValueError as exc:
        assert "No valid flight options" in str(exc)
    else:
        raise AssertionError("Expected ValueError for unknown route")


def test_plan_trip_uses_mock_api_when_graph_agent_fails(monkeypatch):
    from app.agents import graph_agent

    def raise_graph_error(request):
        raise RuntimeError("graph unavailable")

    monkeypatch.setattr(graph_agent, "get_routes", raise_graph_error)

    try:
        plan_trip({"from": "Delhi", "to": "Mumbai", "priority": "time"})
    except RuntimeError as exc:
        assert "graph unavailable" in str(exc)
    else:
        raise AssertionError("Expected graph agent error to surface through workflow")


def test_plan_trip_records_session_memory():
    from app.memory.session_store import session_store

    session_store.clear("test-session")
    response = plan_trip(
        {
            "from": "Delhi",
            "to": "Mumbai",
            "priority": "time",
            "session_id": "test-session",
        }
    )

    events = session_store.get("test-session")
    assert response.best_flight.flight_no
    assert events
    assert events[-1]["payload"]["best_flight"] == response.best_flight.flight_no
