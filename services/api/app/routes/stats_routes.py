from fastapi import APIRouter
from services.api.app.adapters.database import db_adapter

router = APIRouter(prefix="/api/v1/analytics", tags=["Live Analytics & Dashboard"])


@router.get("/stats")
async def get_live_stats():
    """
    Returns live statistics from the Daanish schools production SQL Server database,
    including student counts, campus breakdown, and teacher summaries.
    """
    return db_adapter.get_live_dashboard_stats()
