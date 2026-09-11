import time
import uuid
from typing import Union

from fastapi import APIRouter, Depends
from fastapi.concurrency import run_in_threadpool

from packages.contracts.schemas.auth import AuthContext
from packages.contracts.schemas.query import QueryRefusal, QueryRequest, QueryResponse
from services.api.audit.logger import AuditLogger
from services.api.auth.dependencies import require_auth
from services.api.db.interface import DataAdapter
from services.api.db.provider import get_data_adapter
from services.api.db.sqlserver_adapter import LiveDatabaseUnavailable
from services.api.privacy.openrouter_client import ModelUnavailableError, OpenRouterClient
from services.query.wren_engine import PlanError, QueryPlan, WrenEngine
from services.query.wren_semantic import SemanticPlanningError, WREN_VERSION, plan_semantic_sql

router = APIRouter(prefix="/api/v1/query", tags=["Query Engine"])
audit_logger = AuditLogger()
wren_engine = WrenEngine()


def _audit(
    query_id: str,
    auth: AuthContext,
    elapsed_ms: int,
    outcome: str,
    *,
    sql_generated: bool,
    external: bool,
    reason_code: str | None = None,
) -> None:
    audit_logger.log_event(
        request_id=query_id,
        user_id=auth.user_id,
        access_scope=auth.access_scope,
        prompt_family="query",
        sql_generated=sql_generated,
        validation_result="PASS" if outcome == "success" else "REJECTED",
        external_call_made=external,
        execution_time_ms=elapsed_ms,
        outcome=outcome,
        reason_code=reason_code,
    )


def _refusal(
    query_id: str,
    code: str,
    message: str,
    auth: AuthContext,
    elapsed_ms: int,
    external: bool = False,
) -> QueryRefusal:
    _audit(
        query_id, auth, elapsed_ms, "refused",
        sql_generated=False, external=external, reason_code=code,
    )
    return QueryRefusal(query_id=query_id, reason_code=code, safe_message=message)


def _scope(plan: QueryPlan) -> str:
    return "all campuses" if plan.campus == "ALL" else f"campus {plan.campus}"


def _summary(plan: QueryPlan, rows: list[dict]) -> str:
    scope = _scope(plan)
    if not rows:
        return f"No live records matched this {plan.intent.replace('_', ' ')} query for {scope}."
    if plan.catalog_family:
        filters = []
        if plan.class_level is not None:
            filters.append(f"Class {plan.class_level}")
        if plan.section:
            filters.append(f"Section {plan.section}")
        if plan.year is not None:
            filters.append(f"year {plan.year}")
        if plan.subject:
            filters.append(plan.subject.title())
        if plan.exam_type:
            filters.append(plan.exam_type.title())
        filter_text = ", ".join(filters) if filters else "the requested scope"
        if "matching_count" in rows[0]:
            return (
                f"The verified {plan.catalog_family} source contains {rows[0].get('matching_count') or 0} matching record(s) for {filter_text}. "
                "The count was calculated locally from the read-only database; no external model received the prompt or result."
            )
        if "average_value" in rows[0]:
            value = rows[0].get("average_value")
            shown = f"{float(value):.1f}" if value is not None else "no numeric value"
            return (
                f"The calculated average for {filter_text} is {shown} from the verified {plan.catalog_family} source. "
                "This explanation is generated locally from the returned aggregate and the requested filters."
            )
        cap = f" Results are capped at {plan.limit} rows." if len(rows) >= plan.limit else ""
        return (
            f"The read-only database returned {len(rows)} matching row(s) from the verified {plan.catalog_family} source for {filter_text}.{cap} "
            "The table below is the supporting evidence; no external model received the prompt or result."
        )
    if plan.intent == "weak_students":
        values = [float(row["percentage"]) for row in rows if row.get("percentage") is not None]
        lowest = min(values) if values else None
        detail = f" The lowest returned result is {lowest:.1f}%." if lowest is not None else ""
        return f"I found {len(rows)} student result(s) below {plan.threshold:g}% across {scope}, ordered from lowest first.{detail}"
    if plan.intent == "top_students":
        values = [float(row["percentage"]) for row in rows if row.get("percentage") is not None]
        highest = max(values) if values else None
        detail = f" The highest returned result is {highest:.1f}%." if highest is not None else ""
        return f"I found the top {len(rows)} matching student result(s) across {scope}.{detail}"
    if plan.intent == "attendance_summary":
        present = sum(int(row.get("present_count") or 0) for row in rows)
        absent = sum(int(row.get("absent_count") or 0) for row in rows)
        return f"Attendance across {scope} contains {present} present and {absent} absent records in {len(rows)} house group(s)."
    if plan.intent in {"school_performance", "class_performance", "subject_performance"}:
        values = [float(row["average_pass_percentage"]) for row in rows if row.get("average_pass_percentage") is not None]
        average = sum(values) / len(values) if values else None
        detail = f" The mean pass percentage across returned groups is {average:.1f}%." if average is not None else ""
        return f"The live comparison returned {len(rows)} group(s) for {scope}.{detail}"
    if plan.intent == "attendance_absence_list":
        return f"I found {len(rows)} recent absence record(s) for {scope}."
    if plan.intent == "student_attendance":
        return f"I found {len(rows)} attendance event(s) for the identified student in the local database."
    if plan.intent == "individual_results":
        return f"I found {len(rows)} subject result row(s) for the identified student in the local database."
    if plan.intent == "individual_student":
        return f"I found {len(rows)} enrollment record(s) for the identified student in the local database."
    if plan.intent == "student_roster":
        return f"The live roster returned {len(rows)} student record(s) for {scope}; display is capped at {plan.limit}."
    return f"The live database returned {len(rows)} {plan.intent.replace('_', ' ')} record(s) for {scope}."


def _text_response(query_id: str, message: str, auth: AuthContext, elapsed_ms: int) -> QueryResponse:
    _audit(query_id, auth, elapsed_ms, "success", sql_generated=False, external=False)
    return QueryResponse(
        query_id=query_id,
        generated_sql=None,
        columns=[],
        rows=[],
        row_count=0,
        explanation=message,
        execution_time_ms=elapsed_ms,
        data_source="none",
        model_used=None,
        planner_source="local",
        semantic_layer=WREN_VERSION,
        answer_mode="local_privacy_safe",
        semantic_intent="conversation",
    )


@router.post("/execute", response_model=Union[QueryResponse, QueryRefusal])
async def execute_query(
    body: QueryRequest,
    auth: AuthContext = Depends(require_auth),
    db_adapter: DataAdapter = Depends(get_data_adapter),
):
    """Interpret locally when possible, plan through Wren MDL, then query read-only SQL Server."""
    started = time.perf_counter()
    query_id = str(uuid.uuid4())

    if not wren_engine.is_safe_question(body.prompt):
        return _refusal(
            query_id, "NON_SELECT_SQL",
            "Only governed academic questions are accepted; SQL commands are not accepted.",
            auth, int((time.perf_counter() - started) * 1000),
        )

    decision = wren_engine.interpret_local(body.prompt)
    if decision.kind == "conversation":
        return _text_response(
            query_id, decision.message or "Ask an academic analytics question.", auth,
            int((time.perf_counter() - started) * 1000),
        )
    if decision.kind == "out_of_scope":
        return _refusal(
            query_id, "OUT_OF_SCOPE", decision.message or "That question is outside EduQuery's scope.",
            auth, int((time.perf_counter() - started) * 1000),
        )
    if decision.kind == "unsupported":
        return _refusal(
            query_id, "GOVERNED_CAPABILITY_REQUIRED",
            decision.message or "This request needs a verified semantic contract before it can run safely.",
            auth, int((time.perf_counter() - started) * 1000),
        )

    plan = decision.plan
    planner_source = "local"
    model_used = None
    external = False
    if plan is None:
        if not wren_engine.can_send_to_remote_planner(body.prompt):
            return _refusal(
                query_id, "LOCAL_IDENTITY_PARSE_FAILED",
                "The student identifier could not be parsed safely. Use 'student named ...' or 'roll number ...'.",
                auth, int((time.perf_counter() - started) * 1000),
            )
        planner = OpenRouterClient()
        external_attempted = planner.is_configured
        try:
            raw_plan = await planner.plan_query(
                prompt=wren_engine.remote_planner_prompt(body.prompt),
                system_prompt=wren_engine.system_prompt,
                schema=wren_engine.response_schema,
            )
            external = external_attempted
            plan = wren_engine.validate_plan(raw_plan)
            planner_source = "external"
            model_used = "openai/gpt-5.6-luna-pro"
        except PlanError:
            return _refusal(
                query_id, "UNSUPPORTED_SEMANTIC_PLAN",
                "The question could not be mapped to the governed Wren semantic model.",
                auth, int((time.perf_counter() - started) * 1000), True,
            )
        except ModelUnavailableError:
            return _refusal(
                query_id, "MODEL_DISABLED",
                "This wording needs the optional external planner, which is currently disabled. Rephrase using a student, result, attendance, teacher, class, subject, or campus comparison.",
                auth, int((time.perf_counter() - started) * 1000), external_attempted,
            )

    try:
        semantic_sql, params = wren_engine.compile(plan)
        physical_sql = plan_semantic_sql(semantic_sql)
    except (PlanError, SemanticPlanningError):
        return _refusal(
            query_id, "WREN_SEMANTIC_REJECTED",
            "Wren rejected the semantic query before database execution.",
            auth, int((time.perf_counter() - started) * 1000), external,
        )

    try:
        rows = await run_in_threadpool(db_adapter.execute_query, physical_sql, params)
    except LiveDatabaseUnavailable:
        return _refusal(
            query_id, "LIVE_DATABASE_UNAVAILABLE",
            "The local read-only academic database is unavailable.",
            auth, int((time.perf_counter() - started) * 1000), external,
        )

    elapsed_ms = int((time.perf_counter() - started) * 1000)
    _audit(query_id, auth, elapsed_ms, "success", sql_generated=True, external=external)
    return QueryResponse(
        query_id=query_id,
        generated_sql=physical_sql,
        columns=list(rows[0].keys()) if rows else [],
        rows=rows,
        row_count=len(rows),
        explanation=_summary(plan, rows) if body.include_explanation else None,
        execution_time_ms=elapsed_ms,
        data_source="live_sqlserver_readonly",
        model_used=model_used,
        planner_source=planner_source,
        semantic_layer=WREN_VERSION,
        answer_mode="local_privacy_safe",
        semantic_intent=plan.intent,
    )
