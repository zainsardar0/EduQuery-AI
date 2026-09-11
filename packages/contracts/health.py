from typing import Dict, Optional
from pydantic import BaseModel, Field


class ComponentStatus(BaseModel):
    status: str = Field(..., description="Component status ('healthy', 'degraded', 'unreachable', etc.)")
    message: Optional[str] = Field(default=None, description="Detailed component message or latency metric")


class HealthResponse(BaseModel):
    status: str = Field(..., description="Overall service status ('healthy', 'degraded', 'unhealthy')")
    service: str = Field(default="EduQuery-AI Backend API", description="Service name")
    version: str = Field(default="1.0.0-mvp", description="Service release version")
    timestamp: str = Field(..., description="ISO-8601 UTC timestamp")
    components: Dict[str, ComponentStatus] = Field(
        default_factory=dict,
        description="Individual component health assessments (database, RAG, ML inference)"
    )
