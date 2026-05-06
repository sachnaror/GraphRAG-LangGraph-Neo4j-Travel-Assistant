from fastapi import APIRouter, HTTPException

from app.schemas.travel import TravelRequest, TravelResponse
from app.services.travel_service import plan_trip


router = APIRouter(tags=["travel"])


@router.post("/plan-trip", response_model=TravelResponse)
def create_trip_plan(request: TravelRequest) -> TravelResponse:
    try:
        return plan_trip(request.to_service_dict())
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
