import argparse
import sys
from pathlib import Path
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.config import get_settings
from app.graph.models import AirportNode, FlightNode, RouteEdge, UserNode, parse_graph_dataset
from app.utils.helpers import load_json
from app.utils.logger import app_logger


GRAPH_DATA_DIR = ROOT_DIR / "data" / "graph_data"


def load_graph_dataset(data_dir: Path = GRAPH_DATA_DIR) -> dict[str, list[dict[str, Any]]]:
    dataset = {
        "airports": load_json(data_dir / "airports.json").get("airports", []),
        "routes": load_json(data_dir / "routes.json").get("routes", []),
        "flights": load_json(data_dir / "flights.json").get("flights", []),
        "users": load_json(data_dir / "users.json").get("users", []),
    }
    validate_dataset(dataset)
    return dataset


def validate_dataset(dataset: dict[str, list[dict[str, Any]]]) -> None:
    required = {
        "airports": ["code", "city"],
        "routes": ["from", "to"],
        "flights": ["flight_no", "from", "to", "price", "duration_minutes"],
        "users": ["user_id", "name"],
    }

    errors = []
    for group, fields in required.items():
        for index, item in enumerate(dataset.get(group, [])):
            missing = [field for field in fields if field not in item]
            if missing:
                errors.append(f"{group}[{index}] missing: {', '.join(missing)}")

    if errors:
        raise ValueError("; ".join(errors))

    parse_graph_dataset(dataset)


def summarize_dataset(dataset: dict[str, list[dict[str, Any]]]) -> dict[str, int]:
    return {key: len(value) for key, value in dataset.items()}


def ingest_dataset(dataset: dict[str, list[dict[str, Any]]]) -> None:
    settings = get_settings()
    if not (settings.neo4j_uri and settings.neo4j_username and settings.neo4j_password):
        raise RuntimeError("Neo4j credentials are missing. Fill NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD in .env.")

    try:
        from neo4j import GraphDatabase
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Neo4j Python driver is not installed in the active environment. "
            f"Active Python: {sys.executable}. "
            f"Run: {sys.executable} -m pip install neo4j==5.20.0 "
            f"or {sys.executable} -m pip install -r requirements.txt"
        ) from exc

    with GraphDatabase.driver(
        settings.neo4j_uri,
        auth=(settings.neo4j_username, settings.neo4j_password),
    ) as driver:
        with driver.session() as session:
            session.execute_write(_clear_graph)
            parsed = parse_graph_dataset(dataset)
            session.execute_write(_ingest_airports, parsed["airports"])
            session.execute_write(_ingest_routes, parsed["routes"])
            session.execute_write(_ingest_flights, parsed["flights"])
            session.execute_write(_ingest_users, parsed["users"])


def _clear_graph(tx) -> None:
    tx.run("MATCH (n) DETACH DELETE n")


def _ingest_airports(tx, airports: list[AirportNode]) -> None:
    for airport in airports:
        tx.run(
            """
            MERGE (a:Airport {code: $code})
            SET a.city = $city,
                a.country = $country,
                a.timezone = $timezone,
                a.lat = $lat,
                a.lon = $lon
            """,
            airport.to_neo4j_properties(),
        )


def _ingest_routes(tx, routes: list[RouteEdge]) -> None:
    for route in routes:
        tx.run(
            """
            MATCH (origin:Airport {city: $from_city})
            MATCH (destination:Airport {city: $to_city})
            MERGE (origin)-[r:ROUTE_TO]->(destination)
            SET r.distance_km = $distance_km,
                r.avg_duration = $avg_duration,
                r.popularity_score = $popularity_score
            """,
            route.to_neo4j_parameters(),
        )


def _ingest_flights(tx, flights: list[FlightNode]) -> None:
    for flight in flights:
        properties = flight.to_neo4j_properties()
        tx.run(
            """
            MATCH (origin:Airport {city: $from_city})
            MATCH (destination:Airport {city: $to_city})
            MERGE (f:Flight {flight_no: $flight_no})
            SET f += $properties
            MERGE (origin)-[:HAS_FLIGHT]->(f)
            MERGE (f)-[:ARRIVES_AT]->(destination)
            MERGE (origin)-[:FLIGHT_TO {flight_no: $flight_no}]->(destination)
            """,
            {
                "from_city": flight.from_city,
                "to_city": flight.to_city,
                "flight_no": flight.flight_no,
                "properties": properties,
            },
        )


def _ingest_users(tx, users: list[UserNode]) -> None:
    for user in users:
        tx.run(
            """
            MERGE (u:User {user_id: $user_id})
            SET u += $properties
            """,
            {"user_id": user.user_id, "properties": user.to_neo4j_properties()},
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate or ingest graph JSON into Neo4j.")
    parser.add_argument("--write", action="store_true", help="Write data into Neo4j. Defaults to dry-run validation.")
    args = parser.parse_args()

    dataset = load_graph_dataset()
    summary = summarize_dataset(dataset)
    app_logger.info(f"Graph dataset validated: {summary}")

    if args.write:
        ingest_dataset(dataset)
        app_logger.info("Graph data ingested into Neo4j.")
    else:
        app_logger.info("Dry run complete. Use --write to ingest into Neo4j.")


if __name__ == "__main__":
    main()
