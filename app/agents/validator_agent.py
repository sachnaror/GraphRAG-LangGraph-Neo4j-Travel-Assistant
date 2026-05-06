from app.services.validation_service import validate_flight_options


def validate_options(options: list[dict], request: dict) -> list[dict]:
    valid, _ = validate_flight_options(options, request)
    return valid
