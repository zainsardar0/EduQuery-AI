from typing import Any, Dict, Literal
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    student_features: Dict[str, Any] = Field(..., description="Anonymized student feature set")
    target: Literal["dropout_risk", "academic_risk"] = Field(..., description="Prediction target objective")


class PredictionResponse(BaseModel):
    status: Literal["success", "error"] = Field("success", description="Prediction outcome status")
    prediction_id: str = Field(..., description="Unique prediction execution UUID")
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Risk probability score (0.0 to 1.0)")
    risk_label: Literal["low", "medium", "high"] = Field(..., description="Categorical risk rating")
    mlflow_run_id: str = Field(..., description="Versioned MLflow model run tracking ID")
    shap_values: Dict[str, float] = Field(default_factory=dict, description="SHAP feature attribution scores")
    disclaimer: str = Field(
        "Predictions are advisory only. Final administrative decisions remain with authorized human officers.",
        description="Mandatory advisory governance disclaimer"
    )
