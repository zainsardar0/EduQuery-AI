import datetime
import uuid
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from packages.contracts.auth import AuthContext
from packages.contracts.error import ErrorCode, ErrorResponse
from packages.contracts.prediction import (
    MANDATORY_DISCLAIMER,
    ConfidenceInterval,
    ImpactDirection,
    ModelMetadata,
    PredictionRequest,
    PredictionResponse,
    RiskTier,
    ShapExplanation,
)
from services.api.app.adapters.database import db_adapter
from services.api.app.services.audit import audit_service

router = APIRouter(prefix="/api/v1", tags=["Prediction Engine"])


@router.post("/prediction", response_model=PredictionResponse)
async def process_prediction(request: Request, pred_req: PredictionRequest):
    """
    Process academic risk prediction and feature attribution request.
    Enforces server-side campus authorization and redacted audit logging.
    """
    user: AuthContext = getattr(request.state, "user", None)
    if not user:
        err = ErrorResponse(
            success=False,
            error_code=ErrorCode.AUTH_UNAUTHENTICATED,
            message="Authentication required.",
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            request_id=str(uuid.uuid4())
        )
        return JSONResponse(status_code=401, content=err.model_dump())

    requested_campus = (pred_req.campus_code or user.campus_scope[0]).upper()

    # Security check: Cross-Campus Prevention
    if requested_campus not in user.campus_scope:
        err = ErrorResponse(
            success=False,
            error_code=ErrorCode.CROSS_CAMPUS_ACCESS_DENIED,
            message=f"Access denied. Campus code '{requested_campus}' is outside your authorized campus_scope.",
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            request_id=str(uuid.uuid4())
        )
        audit_service.log_event(
            user_id=user.user_id,
            role=user.role.value,
            campus_applied=requested_campus,
            intent_category="Unauthorized Prediction Attempt",
            tables_queried=[],
            execution_time_ms=0.0,
            success=False,
            error_code=ErrorCode.CROSS_CAMPUS_ACCESS_DENIED.value
        )
        return JSONResponse(status_code=403, content=err.model_dump())

    # Get prediction payload
    pred_data, fallback_used, exec_ms = db_adapter.get_prediction(
        target_id=pred_req.target_id,
        campus_code=requested_campus
    )

    model_meta = ModelMetadata(
        model_name=pred_data["model_name"],
        model_version=pred_data["model_version"],
        mlflow_run_id=pred_data["mlflow_run_id"],
        evaluated_at=pred_data["evaluated_at"]
    )

    confidence = ConfidenceInterval(
        lower_bound=pred_data["confidence_lower"],
        upper_bound=pred_data["confidence_upper"]
    )

    raw_shaps = pred_data.get("feature_attributions") or pred_data.get("shap_attributions", [])
    shaps = []
    for f in raw_shaps:
        feat_name = f.get("feature_name") or f.get("feature") or "unknown_feature"
        disp_name = f.get("display_name") or feat_name.replace("_", " ").title()
        shap_val = float(f.get("shap_value") or f.get("attribution_score") or 0.0)
        direction_str = str(f.get("impact_direction", ""))
        if "DECREASE" in direction_str.upper() or shap_val < 0:
            dir_enum = ImpactDirection.DECREASES_RISK
        else:
            dir_enum = ImpactDirection.INCREASES_RISK
            
        shaps.append(
            ShapExplanation(
                feature_name=feat_name,
                display_name=disp_name,
                shap_value=shap_val,
                impact_direction=dir_enum,
                value_observed=f.get("value_observed")
            )
        )

    req_id = str(uuid.uuid4())

    audit_service.log_event(
        user_id=user.user_id,
        role=user.role.value,
        campus_applied=requested_campus,
        intent_category="Student Performance Risk Prediction",
        tables_queried=["MARKS", "STUDENTS_ROLL_PROFILE"],
        execution_time_ms=exec_ms,
        success=True,
        fallback_used=fallback_used
    )

    return PredictionResponse(
        success=True,
        target_id=pred_req.target_id,
        risk_level=RiskTier(pred_data["risk_level"]),
        predicted_score=pred_data["predicted_score"],
        confidence_interval=confidence,
        model_metadata=model_meta,
        feature_attributions=shaps,
        disclaimer=MANDATORY_DISCLAIMER,
        request_id=req_id
    )


@router.post("/prediction/teacher")
async def process_teacher_prediction(request: Request):
    """
    Process teacher credibility, value-added score, and next-year class average forecast.
    """
    user: AuthContext = getattr(request.state, "user", None)
    if not user:
        return JSONResponse(status_code=401, content={"success": False, "message": "Authentication required."})

    body = await request.json()
    eid = str(body.get("eid", "1042"))
    campus_code = (body.get("campus_code") or user.campus_scope[0]).upper()

    pred_data, fallback_used, exec_ms = db_adapter.get_teacher_prediction(eid=eid, campus_code=campus_code)
    audit_service.log_event(
        user_id=user.user_id,
        role=user.role.value,
        campus_applied=campus_code,
        intent_category="Teacher Performance Forecast",
        tables_queried=["TR_ALL", "HOF"],
        execution_time_ms=exec_ms,
        success=True,
        fallback_used=fallback_used
    )
    return {"success": True, "data": pred_data, "request_id": str(uuid.uuid4())}


@router.post("/prediction/subject")
async def process_subject_prediction(request: Request):
    """
    Process subject bottleneck risk and board alignment gap forecast.
    """
    user: AuthContext = getattr(request.state, "user", None)
    if not user:
        return JSONResponse(status_code=401, content={"success": False, "message": "Authentication required."})

    body = await request.json()
    subject = str(body.get("subject", "MATHEMATICS"))
    class_grade = int(body.get("class_grade", 9))
    campus_code = (body.get("campus_code") or user.campus_scope[0]).upper()

    pred_data, fallback_used, exec_ms = db_adapter.get_subject_prediction(
        subject=subject, class_grade=class_grade, campus_code=campus_code
    )
    audit_service.log_event(
        user_id=user.user_id,
        role=user.role.value,
        campus_applied=campus_code,
        intent_category="Subject Bottleneck Risk Forecast",
        tables_queried=["Marks_Internal", "BOARD_PER"],
        execution_time_ms=exec_ms,
        success=True,
        fallback_used=fallback_used
    )
    return {"success": True, "data": pred_data, "request_id": str(uuid.uuid4())}


@router.post("/prediction/campus")
async def process_campus_prediction(request: Request):
    """
    Process campus aggregate GPA, gazette pass rate, and reputation rank forecast.
    """
    user: AuthContext = getattr(request.state, "user", None)
    if not user:
        return JSONResponse(status_code=401, content={"success": False, "message": "Authentication required."})

    body = await request.json()
    campus_code = (body.get("campus_code") or user.campus_scope[0]).upper()

    pred_data, fallback_used, exec_ms = db_adapter.get_campus_prediction(campus_code=campus_code)
    audit_service.log_event(
        user_id=user.user_id,
        role=user.role.value,
        campus_applied=campus_code,
        intent_category="Campus Aggregate Reputation Forecast",
        tables_queried=["MARKS", "GZT_STRENGTH"],
        execution_time_ms=exec_ms,
        success=True,
        fallback_used=fallback_used
    )
    return {"success": True, "data": pred_data, "request_id": str(uuid.uuid4())}
