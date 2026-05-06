import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "api_mock"


def _load_json(file_name: str) -> dict:
    with (DATA_DIR / file_name).open("r", encoding="utf-8") as file:
        return json.load(file)


def get_flights(request: dict | None = None) -> list[dict]:
    flights = _load_json("flights.json").get("flights", [])
    if not request:
        return flights

    from_city = request.get("from") or request.get("from_city")
    to_city = request.get("to") or request.get("to_city")

    if from_city and to_city:
        return [
            flight
            for flight in flights
            if flight.get("from") == from_city and flight.get("to") == to_city
        ]
    if from_city:
        return [flight for flight in flights if flight.get("from") == from_city]
    if to_city:
        return [flight for flight in flights if flight.get("to") == to_city]
    return flights


def get_users() -> list[dict]:
    return _load_json("users.json").get("users", [])


def get_user(user_id: str | None) -> dict | None:
    if not user_id:
        return None
    return next((user for user in get_users() if user.get("user_id") == user_id), None)
