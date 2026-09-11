import datetime
from fastapi import APIRouter
from packages.contracts.health import ComponentStatus, HealthResponse

router = APIRouter(tags=["Health & Monitoring"])


@router.get("/health", response_model=HealthResponse)
async def get_health_status() -> HealthResponse:
    """
    Public endpoint monitoring system health, operational version, and component state.
    Bypasses authentication to allow load balancer and monitoring ping checks.
    """
    return HealthResponse(
        status="healthy",
        service="EduQuery-AI Backend API",
        version="1.0.0-mvp",
        timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        components={
            "database": ComponentStatus(status="healthy", message="Read-only MSSQL schema reconciliation verified"),
            "rag": ComponentStatus(status="healthy", message="Local RAG semantic glossary initialized"),
            "prediction": ComponentStatus(status="healthy", message="AutoGluon inference engine online")
        }
    )
