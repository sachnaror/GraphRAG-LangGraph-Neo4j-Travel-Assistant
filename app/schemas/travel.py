from pydantic import BaseModel
from typing import List, Optional


class Flight(BaseModel):
    flight_no: str
    from_city: str
    to_city: str
    price: float
    duration_minutes: int
    rating: Optional[float] = None
    on_time_performance: Optional[float] = None


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
