from dataclasses import dataclass, field

from app.utils.helpers import normalize_city


@dataclass
class ValidationResult:
    is_valid: bool
    errors: list[str] = field(default_factory=list)


def validate_travel_request(request: dict) -> ValidationResult:
    errors = []
    from_city = normalize_city(request.get("from") or request.get("from_city"))
    to_city = normalize_city(request.get("to") or request.get("to_city"))

    if not from_city:
        errors.append("Origin city is required.")
    if not to_city:
        errors.append("Destination city is required.")
    if from_city and to_city and from_city == to_city:
        errors.append("Origin and destination must be different.")

    priority = request.get("priority") or request.get("type") or "balanced"
    allowed_priorities = {"balanced", "price", "cheapest", "time", "fastest", "business", "comfort"}
    if priority not in allowed_priorities:
        errors.append(f"Unsupported priority '{priority}'.")

    seat_class = request.get("seat_class")
    if seat_class and seat_class not in {"Economy", "Business"}:
        errors.append("seat_class must be Economy or Business.")

    return ValidationResult(is_valid=not errors, errors=errors)


def validate_flight_options(options: list[dict], request: dict) -> tuple[list[dict], list[str]]:
    seat_class = request.get("seat_class")
    require_refundable = bool(request.get("refundable_only"))
    valid = []
    rejections = []

    for option in options:
        segments = option.get("segments", [])
        flight_no = option.get("flight_no", "unknown")
        if not segments:
            rejections.append(f"{flight_no}: no segments available")
            continue
        if seat_class and any(seat_class not in segment.get("seat_class", []) for segment in segments):
            rejections.append(f"{flight_no}: requested seat class unavailable")
            continue
        if require_refundable and any(not segment.get("fare_rules", {}).get("refundable") for segment in segments):
            rejections.append(f"{flight_no}: non-refundable segment present")
            continue
        if any(
            "available_seats" in segment
            and segment.get("available_seats", {}).get(seat_class or "Economy", 0) <= 0
            for segment in segments
        ):
            rejections.append(f"{flight_no}: no seats available")
            continue
        valid.append(option)

    return valid, rejections
