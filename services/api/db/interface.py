from typing import Any, Dict, List, Optional, Protocol, Sequence, runtime_checkable


@runtime_checkable
class DataAdapter(Protocol):
    def execute_query(self, sql: str, params: Optional[Sequence[Any]] = None) -> List[Dict[str, Any]]:
        ...

    def healthcheck(self) -> bool:
        ...
