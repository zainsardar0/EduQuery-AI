from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=1000, description="Natural language academic query")
    include_explanation: bool = Field(True, description="Whether to return NL explanation")


class QueryResponse(BaseModel):
    status: Literal["success"] = Field("success", description="Status code")
    query_id: str = Field(..., description="Unique query execution UUID")
    generated_sql: Optional[str] = Field(None, description="Validated SELECT query executed")
    columns: List[str] = Field(default_factory=list, description="Result column names")
    rows: List[Dict[str, Any]] = Field(default_factory=list, description="Result set rows")
    row_count: int = Field(0, description="Number of rows returned")
    explanation: Optional[str] = Field(None, description="Natural language explanation of results")
    data_source: str = Field("live_sqlserver", description="Authoritative data source used for this response")
    model_used: Optional[str] = Field(None, description="Planner model used; never contains a secret")
    planner_source: str = Field("local", description="local or external natural-language planner")
    semantic_layer: str = Field("wrenai", description="Semantic planning engine and runtime version")
    answer_mode: str = Field("local_privacy_safe", description="How the natural-language answer was produced")
    semantic_intent: Optional[str] = Field(None, description="Approved semantic intent selected for the query")
    execution_time_ms: int = Field(..., description="Query execution duration in milliseconds")


class QueryRefusal(BaseModel):
    status: Literal["refused"] = Field("refused", description="Refusal status")
    query_id: str = Field(..., description="Unique query execution UUID")
    reason_code: str = Field(..., description="Machine code e.g. CROSS_CAMPUS_ACCESS, NON_SELECT_SQL, UNKNOWN_OBJECT")
    safe_message: str = Field(..., description="User-safe refusal message")
