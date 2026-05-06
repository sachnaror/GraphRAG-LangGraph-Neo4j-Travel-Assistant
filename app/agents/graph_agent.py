from app.mocks.mock_external_api import get_flights
from app.graph.neo4j_client import Neo4jClient
from app.graph.models import FlightNode, GraphRouteOption


def get_routes(request: dict) -> list[dict]:
    """Return direct and one-layover flight options from mock graph data."""
    neo4j_options = _get_neo4j_routes(request)
    if neo4j_options:
        return neo4j_options

    from_city = request.get("from") or request.get("from_city")
    to_city = request.get("to") or request.get("to_city")

    if not from_city or not to_city:
        return []

    flights = [FlightNode.from_dict(flight) for flight in get_flights()]
    direct_options = [
        GraphRouteOption.from_flights([flight]).to_dict()
        for flight in flights
        if flight.from_city == from_city and flight.to_city == to_city
    ]

    layover_options = []
    outbound = [flight for flight in flights if flight.from_city == from_city]
    inbound = [flight for flight in flights if flight.to_city == to_city]
    for first_leg in outbound:
        for second_leg in inbound:
            if first_leg.to_city == second_leg.from_city:
                layover_options.append(GraphRouteOption.from_flights([first_leg, second_leg]).to_dict())

    return direct_options + layover_options


def _get_neo4j_routes(request: dict) -> list[dict]:
    try:
        records = Neo4jClient.from_settings().get_route_records(request)
    except Exception:
        return []

    # The local JSON fallback is the canonical runnable path today. This hook
    # keeps the agent ready for Neo4j path-to-flight mapping when graph data is
    # ingested with flight properties.
    return [
        GraphRouteOption.from_dict(record["option"]).to_dict()
        for record in records
        if isinstance(record.get("option"), dict)
    ]
