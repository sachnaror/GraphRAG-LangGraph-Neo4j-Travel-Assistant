from fastapi import APIRouter

from app.observability.metrics import metrics


router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/metrics")
def metrics_snapshot() -> dict:
    return metrics.snapshot()
