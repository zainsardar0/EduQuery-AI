from functools import lru_cache

from services.api.config import get_settings
from services.api.db.interface import DataAdapter
from services.api.db.sqlserver_adapter import SQLServerAdapter


@lru_cache
def get_data_adapter() -> DataAdapter:
    """Use the live SQL Server only; never silently fall back to seed data."""
    if get_settings().data_backend.lower() != "sqlserver":
        raise RuntimeError("EduQuery Wren requires DATA_BACKEND=sqlserver; seeded fallback is disabled.")
    return SQLServerAdapter()
