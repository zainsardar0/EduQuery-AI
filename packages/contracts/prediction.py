from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, Field


class TargetType(str, Enum):
    STUDENT = "student"
    CLASS_SECTION = "class_section"
    CAMPUS_COHORT = "campus_cohort"


class PredictionHorizon(str, Enum):
    NEXT_EXAM = "next_exam"
    ANNUAL_BOARD = "annual_board"
    GRADUATION_RISK = "graduation_risk"


class RiskTier(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ImpactDirection(str, Enum):
    INCREASES_RISK = "INCREASES_RISK"
    DECREASES_RISK = "DECREASES_RISK"


class PredictionRequest(BaseModel):
    target_type: TargetType = Field(..., description="Granularity level", examples=[TargetType.STUDENT])
    target_id: str = Field(..., description="Target entity identifier", examples=["SYN_1001"])
    campus_code: Optional[str] = Field(default=None, pattern=r"^[A-Z]{4}$", examples=["MNWB"])
    academic_year: Optional[int] = Field(default=None, ge=22, le=26, examples=[26])
    prediction_horizon: PredictionHorizon = Field(
        default=PredictionHorizon.ANNUAL_BOARD,
        examples=[PredictionHorizon.ANNUAL_BOARD]
    )


class ConfidenceInterval(BaseModel):
    lower_bound: float = Field(..., examples=[38.0])
    upper_bound: float = Field(..., examples=[47.0])


class ModelMetadata(BaseModel):
    model_name: str = Field(..., examples=["AutoGluon_WeightedEnsemble_L2"])
    model_version: str = Field(..., examples=["1.0.0-temporal-split"])
    mlflow_run_id: str = Field(..., examples=["run_20260803_autogluon_01"])
    evaluated_at: str = Field(..., examples=["2026-08-03T12:00:00Z"])


class ShapExplanation(BaseModel):
    feature_name: str = Field(..., examples=["mid_dec_math_marks"])
    display_name: str = Field(..., examples=["Mid-Dec Math Marks"])
    shap_value: float = Field(..., examples=[-12.4])
    impact_direction: ImpactDirection = Field(..., examples=[ImpactDirection.INCREASES_RISK])
    value_observed: Optional[Union[str, float, int]] = Field(default=None, examples=[28.0])


MANDATORY_DISCLAIMER = (
    "ADVISORY NOTICE: Model predictions and SHAP attributions are decision-support indicators "
    "intended to assist educators and academic counselors. They do not constitute final academic "
    "determinations, disciplinary decisions, or automated grading actions."
)


class PredictionResponse(BaseModel):
    success: bool = Field(default=True)
    target_id: str = Field(..., examples=["SYN_1001"])
    risk_level: RiskTier = Field(..., examples=[RiskTier.HIGH])
    predicted_score: float = Field(..., ge=0.0, le=100.0, examples=[42.5])
    confidence_interval: Optional[ConfidenceInterval] = Field(default=None)
    model_metadata: ModelMetadata = Field(...)
    feature_attributions: List[ShapExplanation] = Field(...)
    disclaimer: str = Field(
        default=MANDATORY_DISCLAIMER,
        description="Mandatory institutional advisory disclaimer text"
    )
    request_id: str = Field(..., examples=["c3b2a109-8765-4321-fedc-ba9876543210"])
