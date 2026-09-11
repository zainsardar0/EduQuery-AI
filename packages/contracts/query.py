from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field


class DataType(str, Enum):
    STRING = "string"
    NUMBER = "number"
    PERCENTAGE = "percentage"
    DATE = "date"
    BOOLEAN = "boolean"


class ExamType(str, Enum):
    MID_DEC = "MID_DEC"
    ANNUAL = "ANNUAL"
    MOCK = "MOCK"


class ChartType(str, Enum):
    BAR = "bar"
    LINE = "line"
    PIE = "pie"
    KPI_CARD = "kpi_card"
    TABLE_ONLY = "table_only"


class QueryFilters(BaseModel):
    campus_code: Optional[str] = Field(
        default=None,
        description="Optional campus filter code or 'ALL'",
        examples=["MNWB", "ALL"]
    )
    academic_year: Optional[int] = Field(
        default=None,
        ge=22,
        le=26,
        description="Academic year in 2-digit format",
        examples=[26]
    )
    class_level: Optional[int] = Field(
        default=None,
        ge=1,
        le=12,
        description="Grade level (1 to 12)",
        examples=[10]
    )
    exam_type: Optional[ExamType] = Field(
        default=None,
        description="Exam category type filter",
        examples=[ExamType.MID_DEC]
    )


class RequestMetadata(BaseModel):
    client_timestamp: Optional[str] = Field(default=None, examples=["2026-08-03T12:00:00Z"])
    ui_version: Optional[str] = Field(default="1.0.0-mvp", examples=["1.0.0-mvp"])


class QueryRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="Natural language query prompt submitted by the user",
        examples=["Show pass percentage by subject for class 10 in MNWB for 2026."]
    )
    filters: Optional[QueryFilters] = Field(default=None, description="Optional UI-selected filter constraints")
    request_metadata: Optional[RequestMetadata] = Field(default=None, description="Client runtime metadata")


class TableColumn(BaseModel):
    key: str = Field(..., examples=["SUBJECTNAME"])
    label: str = Field(..., examples=["Subject"])
    data_type: DataType = Field(..., examples=[DataType.PERCENTAGE])


class QueryResultTable(BaseModel):
    columns: List[TableColumn] = Field(..., description="Typed column metadata array")
    rows: List[Dict[str, Optional[Union[str, int, float, bool]]]] = Field(
        ...,
        description="Sanitized data row records"
    )
    total_rows: int = Field(..., ge=0, examples=[2])


class ChartConfig(BaseModel):
    chart_type: ChartType = Field(..., examples=[ChartType.BAR])
    title: str = Field(..., examples=["Class 10 Pass Rate by Subject — MNWB (2026)"])
    x_axis_key: str = Field(..., examples=["SUBJECTNAME"])
    y_axis_keys: List[str] = Field(..., examples=[["PASS_PERCENTAGE"]])
    color_palette: Optional[List[str]] = Field(default_factory=lambda: ["#1E40AF", "#3B82F6"])


class EvidenceMetadata(BaseModel):
    intent_category: str = Field(..., examples=["Class/Section Aggregates"])
    tables_queried: List[str] = Field(..., examples=[["vw_CONSOLIDATED_ACCURATE"]])
    campus_applied: str = Field(..., examples=["MNWB"])
    execution_time_ms: float = Field(..., examples=[142.5])
    rag_sources_used: List[str] = Field(..., examples=[["master_schema.md#vw_CONSOLIDATED_ACCURATE"]])


class QueryResponse(BaseModel):
    success: bool = Field(default=True, description="Always true for successful responses")
    answer: str = Field(..., description="Formatted natural language summary answering the prompt")
    data_table: Optional[QueryResultTable] = Field(default=None, description="Tabular dataset for rendering UI data grids if applicable")
    chart_config: Optional[ChartConfig] = Field(default=None, description="Recommended visualization properties if applicable")
    evidence: EvidenceMetadata = Field(..., description="Query provenance & compliance metadata")
    request_id: str = Field(..., description="Unique correlation request UUID")
