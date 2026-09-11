from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field


class PolicyRequest(BaseModel):
    issue_description: str = Field(..., min_length=1, max_length=2000, description="Administrative or academic policy query")
    category_filter: Optional[str] = Field(None, description="Optional verified-corpus category filter (admission, leave, attendance, grading, general)")


class PolicyResponse(BaseModel):
    status: Literal["found", "not_found", "error"] = Field(..., description="RAG search status")
    policy_id: str = Field(..., description="Unique search execution UUID")
    relevant_sections: List[Dict[str, Any]] = Field(default_factory=list, description="Retrieved policy document excerpts with sources")
    explanation: str = Field(..., description="Synthesized administrative policy response")
    retrieval_mode: str = Field("local_hybrid_reranked", description="Local retrieval pipeline")
    provenance_verified: bool = Field(False, description="Whether source and model evidence passed verification")
    release_eligible: bool = Field(False, description="Named domain-review release gate")
    disclaimer: str = Field(
        "Final administrative decisions remain with authorized human officers.",
        description="Mandatory advisory policy disclaimer"
    )
