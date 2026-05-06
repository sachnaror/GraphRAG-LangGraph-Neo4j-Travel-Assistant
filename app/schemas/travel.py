from typing import Any, List, Literal, Optional

from pydantic import BaseModel, Field, model_validator


Priority = Literal["balanced", "price", "cheapest", "time", "fastest", "business", "comfort"]
SeatClass = Literal["Economy", "Business"]


class TravelRequest(BaseModel):
    from_city: str = Field(alias="from", min_length=1)
    to_city: str = Field(alias="to", min_length=1)
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    priority: Priority = "balanced"
    seat_class: Optional[SeatClass] = None
    refundable_only: bool = False

    model_config = {"populate_by_name": True}

    @model_validator(mode="before")
    @classmethod
    def normalize_legacy_fields(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        normalized = dict(data)
        if "type" in normalized and "priority" not in normalized:
            normalized["priority"] = normalized["type"]
        if "from_city" in normalized and "from" not in normalized:
            normalized["from"] = normalized["from_city"]
        if "to_city" in normalized and "to" not in normalized:
            normalized["to"] = normalized["to_city"]
        return normalized

    def to_service_dict(self) -> dict:
        return self.model_dump(by_alias=True)


class Flight(BaseModel):
    flight_no: str
    from_city: str
    to_city: str
    price: float
    duration_minutes: int
    rating: Optional[float] = None
    on_time_performance: Optional[float] = None
    airline: Optional[str] = None
    is_direct: Optional[bool] = None
    layovers: List[str] = Field(default_factory=list)


class FlightScore(BaseModel):
    flight_no: str
    score: float
    reason: str


class ComparisonItem(BaseModel):
    flight_no: str
    price: float
    duration_minutes: int
    rating: Optional[float]
    score: float
    highlight: str   # e.g. "Cheapest", "Fastest", "Best Rated"


class TravelResponse(BaseModel):
    best_flight: Flight
    alternatives: List[Flight]
    comparison: List[ComparisonItem]
    explanation: str
    retrieved_context: List[str] = Field(default_factory=list)
