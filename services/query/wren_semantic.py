"""In-process Wren MDL planning; database execution stays in the local adapter."""

import base64
from functools import lru_cache
from importlib.metadata import version
from pathlib import Path

from wren.config import WrenConfig
from wren.engine import WrenEngine as CoreWrenEngine
from wren.model.error import WrenError

from services.api.config import get_settings
from services.query.database_contract import route_sql_to_contract

WREN_VERSION = f"wrenai-{version('wrenai')}"


class SemanticPlanningError(ValueError):
    """The semantic query failed Wren's strict MDL planning policy."""


@lru_cache
def _engine() -> CoreWrenEngine:
    manifest_path = Path(__file__).resolve().parent / "wren_project" / "target" / "mdl.json"
    if not manifest_path.is_file():
        raise SemanticPlanningError("Wren MDL build output is missing.")
    manifest = base64.b64encode(manifest_path.read_bytes()).decode("ascii")
    return CoreWrenEngine(
        manifest_str=manifest,
        data_source="mssql",
        connection_info={},
        config=WrenConfig(strict_mode=True),
    )


def plan_semantic_sql(sql: str) -> str:
    try:
        planned = _engine().dry_plan(sql)
        return route_sql_to_contract(planned, get_settings().sqlserver_contract_mode)
    except (OSError, ValueError, WrenError) as exc:
        raise SemanticPlanningError("Wren rejected the semantic query.") from exc


def semantic_layer_ready() -> bool:
    """Prove the built MDL can be loaded by the pinned strict Wren runtime."""
    try:
        _engine()
        return True
    except (OSError, ValueError, WrenError, SemanticPlanningError):
        return False
