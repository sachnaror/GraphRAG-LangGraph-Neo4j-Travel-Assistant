from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AirportNode:
    code: str
    city: str
    country: str = "India"
    timezone: str | None = None
    lat: float | None = None
    lon: float | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AirportNode":
        return cls(
            code=data["code"],
            city=data["city"],
            country=data.get("country", "India"),
            timezone=data.get("timezone"),
            lat=data.get("lat"),
            lon=data.get("lon"),
        )

    def to_neo4j_properties(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "city": self.city,
            "country": self.country,
            "timezone": self.timezone,
            "lat": self.lat,
            "lon": self.lon,
        }


@dataclass(frozen=True)
class RouteEdge:
    from_city: str
    to_city: str
    distance_km: int | None = None
    avg_duration: int | None = None
    popularity_score: float | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RouteEdge":
        return cls(
            from_city=data["from"],
            to_city=data["to"],
            distance_km=data.get("distance_km"),
            avg_duration=data.get("avg_duration"),
            popularity_score=data.get("popularity_score"),
        )

    def to_neo4j_parameters(self) -> dict[str, Any]:
        return {
            "from_city": self.from_city,
            "to_city": self.to_city,
            "distance_km": self.distance_km,
            "avg_duration": self.avg_duration,
            "popularity_score": self.popularity_score,
        }


@dataclass(frozen=True)
class FareRules:
    refundable: bool = False
    change_fee: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "FareRules":
        payload = data or {}
        return cls(
            refundable=bool(payload.get("refundable", False)),
            change_fee=int(payload.get("change_fee", 0)),
        )

    def to_dict(self) -> dict[str, Any]:
        return {"refundable": self.refundable, "change_fee": self.change_fee}


@dataclass(frozen=True)
class BaggagePolicy:
    cabin: str | None = None
    check_in: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "BaggagePolicy":
        payload = data or {}
        return cls(cabin=payload.get("cabin"), check_in=payload.get("check_in"))

    def to_dict(self) -> dict[str, Any]:
        return {"cabin": self.cabin, "check_in": self.check_in}


@dataclass(frozen=True)
class FlightNode:
    flight_no: str
    airline: str
    from_city: str
    to_city: str
    price: float
    duration_minutes: int
    currency: str = "INR"
    rating: float | None = None
    on_time_performance: float | None = None
    is_direct: bool = True
    layovers: list[str] = field(default_factory=list)
    seat_class: list[str] = field(default_factory=lambda: ["Economy"])
    available_seats: dict[str, int] = field(default_factory=dict)
    fare_rules: FareRules = field(default_factory=FareRules)
    baggage: BaggagePolicy = field(default_factory=BaggagePolicy)
    amenities: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FlightNode":
        return cls(
            flight_no=data["flight_no"],
            airline=data.get("airline", "Unknown"),
            from_city=data.get("from") or data.get("from_city"),
            to_city=data.get("to") or data.get("to_city"),
            price=float(data.get("price", 0)),
            duration_minutes=int(data.get("duration_minutes", 0)),
            currency=data.get("currency", "INR"),
            rating=data.get("rating"),
            on_time_performance=data.get("on_time_performance"),
            is_direct=bool(data.get("is_direct", True)),
            layovers=list(data.get("layovers", [])),
            seat_class=list(data.get("seat_class", ["Economy"])),
            available_seats=dict(data.get("available_seats", {})),
            fare_rules=FareRules.from_dict(data.get("fare_rules")),
            baggage=BaggagePolicy.from_dict(data.get("baggage")),
            amenities=list(data.get("amenities", [])),
        )

    def to_segment_dict(self) -> dict[str, Any]:
        return {
            "flight_no": self.flight_no,
            "airline": self.airline,
            "from": self.from_city,
            "to": self.to_city,
            "price": self.price,
            "duration_minutes": self.duration_minutes,
            "rating": self.rating,
            "on_time_performance": self.on_time_performance,
            "seat_class": self.seat_class,
            "available_seats": self.available_seats,
            "fare_rules": self.fare_rules.to_dict(),
            "baggage": self.baggage.to_dict(),
            "amenities": self.amenities,
        }

    def to_neo4j_properties(self) -> dict[str, Any]:
        return {
            "flight_no": self.flight_no,
            "airline": self.airline,
            "from": self.from_city,
            "to": self.to_city,
            "price": self.price,
            "currency": self.currency,
            "duration_minutes": self.duration_minutes,
            "rating": self.rating,
            "on_time_performance": self.on_time_performance,
            "is_direct": self.is_direct,
            "layovers": self.layovers,
            "seat_class": self.seat_class,
            "available_economy": self.available_seats.get("Economy", 0),
            "available_business": self.available_seats.get("Business", 0),
            "refundable": self.fare_rules.refundable,
            "change_fee": self.fare_rules.change_fee,
            "cabin_baggage": self.baggage.cabin,
            "check_in_baggage": self.baggage.check_in,
            "amenities": self.amenities,
        }


@dataclass(frozen=True)
class UserNode:
    user_id: str
    name: str
    travel_type: str | None = None
    budget_sensitive: bool = False
    preferred_airlines: list[str] = field(default_factory=list)
    seat_preference: str | None = None
    priority: str = "balanced"
    loyalty_member: bool = False

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "UserNode":
        return cls(
            user_id=data["user_id"],
            name=data["name"],
            travel_type=data.get("travel_type"),
            budget_sensitive=bool(data.get("budget_sensitive", False)),
            preferred_airlines=list(data.get("preferred_airlines", [])),
            seat_preference=data.get("seat_preference"),
            priority=data.get("priority", "balanced"),
            loyalty_member=bool(data.get("loyalty_member", False)),
        )

    def to_neo4j_properties(self) -> dict[str, Any]:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "travel_type": self.travel_type,
            "budget_sensitive": self.budget_sensitive,
            "preferred_airlines": self.preferred_airlines,
            "seat_preference": self.seat_preference,
            "priority": self.priority,
            "loyalty_member": self.loyalty_member,
        }


@dataclass(frozen=True)
class GraphRouteOption:
    flight_no: str
    from_city: str
    to_city: str
    price: float
    duration_minutes: int
    rating: float | None
    on_time_performance: float | None
    airline: str
    is_direct: bool
    layovers: list[str]
    segments: list[dict[str, Any]]

    @classmethod
    def from_flights(cls, flights: list[FlightNode]) -> "GraphRouteOption":
        first = flights[0]
        last = flights[-1]
        ratings = [flight.rating for flight in flights if flight.rating is not None]
        on_time = 1.0
        for flight in flights:
            on_time *= flight.on_time_performance or 1.0

        return cls(
            flight_no="+".join(flight.flight_no for flight in flights),
            from_city=first.from_city,
            to_city=last.to_city,
            price=sum(flight.price for flight in flights),
            duration_minutes=sum(flight.duration_minutes for flight in flights),
            rating=round(sum(ratings) / len(ratings), 2) if ratings else None,
            on_time_performance=round(on_time, 3),
            airline=" + ".join(flight.airline for flight in flights),
            is_direct=len(flights) == 1 and not first.layovers,
            layovers=[flight.to_city for flight in flights[:-1]],
            segments=[flight.to_segment_dict() for flight in flights],
        )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "GraphRouteOption":
        return cls(
            flight_no=data["flight_no"],
            from_city=data["from_city"],
            to_city=data["to_city"],
            price=float(data["price"]),
            duration_minutes=int(data["duration_minutes"]),
            rating=data.get("rating"),
            on_time_performance=data.get("on_time_performance"),
            airline=data.get("airline", "Unknown"),
            is_direct=bool(data.get("is_direct", False)),
            layovers=list(data.get("layovers", [])),
            segments=list(data.get("segments", [])),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "flight_no": self.flight_no,
            "from_city": self.from_city,
            "to_city": self.to_city,
            "price": self.price,
            "duration_minutes": self.duration_minutes,
            "rating": self.rating,
            "on_time_performance": self.on_time_performance,
            "airline": self.airline,
            "is_direct": self.is_direct,
            "layovers": self.layovers,
            "segments": self.segments,
        }


def parse_graph_dataset(dataset: dict[str, list[dict[str, Any]]]) -> dict[str, list]:
    return {
        "airports": [AirportNode.from_dict(item) for item in dataset.get("airports", [])],
        "routes": [RouteEdge.from_dict(item) for item in dataset.get("routes", [])],
        "flights": [FlightNode.from_dict(item) for item in dataset.get("flights", [])],
        "users": [UserNode.from_dict(item) for item in dataset.get("users", [])],
    }
