try:
    flights = graph_agent.get_routes(request)
except Exception:
    # fallback
    flights = mock_external_api.get_flights(request)
