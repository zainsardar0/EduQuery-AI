"""Local question routing and governed semantic SQL for EduQuery Wren."""

from dataclasses import dataclass
import csv
from functools import lru_cache
import json
import os
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Tuple


LIVE_CAMPUSES = frozenset({
    "ATKB", "ATKG", "CTNB", "CTNG", "DGKB", "DGKG", "HSPB", "HSPG",
    "MNKB", "MNKG", "MNWB", "MNWG", "RJNB", "RJNG", "RYKB", "RYKG",
    "TNSB", "TNSG", "VEHB", "VEHG",
})
SUPPORTED_INTENTS = frozenset({
    "student_roster", "individual_student", "individual_results", "student_attendance",
    "weak_students", "top_students", "attendance_summary", "attendance_absence_list",
    "teacher_performance", "class_performance", "subject_performance", "school_performance",
})
CLIENT_FAMILY_INTENTS = {
    "STUDENTS_ROLL": "catalog_board_enrollment",
    "MARKS": "catalog_board_marks",
    "PRAC": "catalog_practical_marks",
    "TR2_THEORY": "catalog_theory_teacher_results",
    "TR2_PRAC": "catalog_practical_teacher_results",
    "TR_ALL": "catalog_combined_teacher_results",
    "ALL_COMBINED": "catalog_teacher_career",
    "HOF_FRMT": "catalog_head_office_results",
    "INTERNAL_EXAM_GROUP_WISE_PERFORMANCE_VIEW": "catalog_internal_teacher_results",
    "STUDENT_RESULT_TOTAL": "catalog_annual_student_results",
    "STUDENT_RESULT_TOTAL_INTERNAL": "catalog_internal_student_results",
    "VTEACHER_SUM_PER": "catalog_teacher_overall",
}
CATALOG_SPECS = {
    "STUDENTS_ROLL": ("board_enrollment", ("campus", "student_name", "father_name", "student_reference", "roll_number", "class_level", "section", "school_year", "group_name", "category"), None),
    "MARKS": ("board_marks", ("roll_number", "class_level", "school_year", "exam_type", "subject", "obtained_marks", "total_marks", "percentage", "grade", "result_status"), "percentage"),
    "PRAC": ("practical_marks", ("roll_number", "class_level", "school_year", "exam_type", "subject", "obtained_marks", "total_marks", "percentage", "grade", "result_status"), "percentage"),
    "TR2_THEORY": ("theory_teacher_results", ("campus", "teacher_id", "teacher_name", "subject", "class_level", "section", "school_year", "exam_type", "strength", "appeared", "passed", "pass_percentage", "class_average"), "pass_percentage"),
    "TR2_PRAC": ("practical_teacher_results", ("campus", "teacher_id", "teacher_name", "subject", "class_level", "section", "school_year", "exam_type", "strength", "appeared", "passed", "pass_percentage", "class_average"), "pass_percentage"),
    "TR_ALL": ("teacher_results", ("campus", "teacher_id", "teacher_name", "subject", "class_level", "section", "school_year", "exam_type", "strength", "appeared", "passed", "pass_percentage", "class_average"), "pass_percentage"),
    "ALL_COMBINED": ("teacher_career", ("campus", "teacher_id", "teacher_name", "subject", "class_level", "section", "school_year", "category", "appeared", "passed", "pass_percentage", "class_average", "above_70", "below_70", "position", "total_positions", "workload"), "position"),
    "HOF_FRMT": ("head_office_results", ("campus", "teacher_id", "teacher_name", "subject", "school_year", "class_section", "appeared", "pass_percentage", "board_pass_percentage", "position", "total_positions", "workload", "class_average", "above_70_count", "below_70_count"), "pass_percentage"),
    "INTERNAL_EXAM_GROUP_WISE_PERFORMANCE_VIEW": ("internal_teacher_results", ("campus", "exam_type", "teacher_id", "teacher_name", "school_year", "class_level", "section", "subject", "group_name", "appeared", "absent", "passed", "class_percentage", "class_average", "below_70", "above_70"), "class_percentage"),
    "STUDENT_RESULT_TOTAL": ("annual_student_results", ("campus", "student_name", "father_name", "student_reference", "roll_number", "class_level", "section", "school_year", "group_name", "subject", "obtained_marks", "total_marks", "percentage", "result_status"), "percentage"),
    "STUDENT_RESULT_TOTAL_INTERNAL": ("student_result_card", ("campus", "student_name", "student_reference", "roll_number", "class_level", "section", "school_year", "house", "exam_type", "subject", "obtained_marks", "total_marks", "percentage", "grade", "result_status"), "percentage"),
    "VTEACHER_SUM_PER": ("teacher_board_middle", ("campus", "teacher_id", "teacher_name", "category", "subject", "sum_obtained", "sum_total", "percentage"), "percentage"),
}
SQL_CONTROL_WORD = re.compile(
    r"\b(?:alter|create|delete|drop|exec(?:ute)?|grant|insert|merge|truncate|update)\b",
    re.IGNORECASE,
)
DIRECT_SQL_PATTERN = re.compile(
    r"(?:;|--|/\*|\bselect\s+.+\s+from\b|\bunion\s+select\b|"
    r"\binformation_schema\b|\bsys\.|\bmaster\.\.)",
    re.IGNORECASE | re.DOTALL,
)
ROLL_PATTERN = re.compile(
    r"\broll\s*(?:(?:no|number)\s*[:=#-]?\s*|[#:=]\s*)([A-Z0-9/-]*\d[A-Z0-9/-]*)\b",
    re.IGNORECASE,
)
NAME_PATTERNS = (
    re.compile(r"\bstudent\s+named\s+([A-Za-z][A-Za-z .'-]{1,80})", re.IGNORECASE),
    re.compile(r"\b(?:marks|result|record|attendance|profile)\s+(?:for|of)\s+([A-Za-z][A-Za-z .'-]{1,80})", re.IGNORECASE),
)
SUBJECTS = (
    "computer science", "general science", "pakistan studies", "islamic education",
    "translation of the holy quran", "mathematics", "chemistry", "physics", "biology",
    "english", "urdu", "islamiyat", "social studies", "arts",
)
ACADEMIC_TERMS = frozenset({
    "student", "students", "school", "campus", "class", "section", "teacher", "subject",
    "result", "results", "marks", "grade", "pass", "fail", "weak", "top", "best",
    "attendance", "absent", "absence", "absences", "absentees", "present", "house", "roll", "performance",
})
REMOTE_SAFE_CONCEPTS = ACADEMIC_TERMS | frozenset({
    "across", "average", "averages", "below", "best", "boys", "compare", "count",
    "failing", "girls", "highest", "lowest", "many", "overall", "rate", "rates",
    "recent", "struggling", "summary", "under",
})


class PlanError(ValueError):
    pass


@dataclass(frozen=True)
class QueryPlan:
    intent: str
    campus: str = "ALL"
    class_level: Optional[int] = None
    section: Optional[str] = None
    year: Optional[int] = None
    subject: Optional[str] = None
    house: Optional[str] = None
    student_name: Optional[str] = None
    roll_number: Optional[str] = None
    student_reference: Optional[str] = None
    teacher_id: Optional[int] = None
    exam_type: Optional[str] = None
    category: Optional[str] = None
    group_name: Optional[str] = None
    catalog_family: Optional[str] = None
    operation: str = "detail"
    metric: Optional[str] = None
    distinct_field: Optional[str] = None
    descending: bool = False
    threshold: float = 40.0
    limit: int = 25


@dataclass(frozen=True)
class LocalDecision:
    kind: str
    plan: Optional[QueryPlan] = None
    message: Optional[str] = None


class WrenEngine:
    """Route common human questions locally and compile semantic-model SQL."""

    system_prompt = """Classify an English school analytics question against the EduQuery Wren model.
Return JSON only. Select one intent from: student_roster, weak_students, top_students,
attendance_summary, attendance_absence_list, teacher_performance, class_performance,
subject_performance, school_performance. Do not write SQL. Default campus to ALL unless
the question explicitly names one of the supplied campus codes. Use filters only when explicit.
A weak student is below 40 percent unless the user supplies another threshold. Personal student
identifiers are handled locally and will never be sent to you."""

    response_schema: Dict[str, Any] = {
        "name": "eduquery_semantic_plan",
        "strict": True,
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "intent": {"type": "string", "enum": sorted(SUPPORTED_INTENTS - {"individual_student", "individual_results", "student_attendance"})},
                "campus": {"type": ["string", "null"]},
                "class_level": {"type": ["integer", "null"]},
                "section": {"type": ["string", "null"]},
                "year": {"type": ["integer", "null"]},
                "subject": {"type": ["string", "null"]},
                "house": {"type": ["string", "null"]},
                "threshold": {"type": ["number", "null"]},
                "limit": {"type": ["integer", "null"]},
            },
            "required": ["intent", "campus", "class_level", "section", "year", "subject", "house", "threshold", "limit"],
        },
    }

    @staticmethod
    def is_safe_question(prompt: str) -> bool:
        return not bool(SQL_CONTROL_WORD.search(prompt) or DIRECT_SQL_PATTERN.search(prompt))

    @staticmethod
    @lru_cache(maxsize=1)
    def _gold_catalog() -> Dict[str, str]:
        path = Path(os.getenv("GOLD_PROMPT_CATALOG_PATH", "data/gold_prompts/EduQuery_Gold_Prompts.csv"))
        if not path.is_file():
            return {}
        with path.open(encoding="utf-8-sig", newline="") as handle:
            return {
                " ".join(row["Prompt"].strip().split()).casefold(): row["Table/Family"].split(" / ", 1)[0]
                for row in csv.DictReader(handle)
            }

    def _catalog_decision(self, text: str) -> Optional[LocalDecision]:
        lowered = text.lower()
        if "predict" in lowered and ("exceed" in lowered or "mock" in lowered or "annual" in lowered or "cross-table" in lowered):
            return LocalDecision(
                "unsupported",
                message="This request needs a verified cross-table metric or prediction contract before it can run safely.",
            )
        if re.search(r"\bhow many students are enrolled\b", lowered) or re.search(r"\benrolled in class\b", lowered):
            filters = self._catalog_filters(text)
            return LocalDecision(
                "query",
                QueryPlan(intent="student_roster", catalog_family="STUDENTS_ROLL", **filters),
            )
        family = self._gold_catalog().get(text.casefold())
        if family is None:
            return None
        normalized_family = family.upper()
        if normalized_family == "CROSS-TABLE":
            return LocalDecision(
                "unsupported",
                message="This request needs a verified cross-table metric or prediction contract before it can run safely.",
            )
        if normalized_family == "SCHOOL_IND_POS_SUB":
            return LocalDecision(
                "unsupported",
                message="The supplied School_Ind_Pos_SUB view is school-level aggregate data and cannot answer student merit-list questions.",
            )
        intent = CLIENT_FAMILY_INTENTS.get(normalized_family)
        if intent is None:
            return LocalDecision("unsupported", message="This Daanish prompt family is not yet in the governed Wren model.")
        filters = self._catalog_filters(text)
        return LocalDecision(
            "query",
            QueryPlan(intent=intent, catalog_family=normalized_family, **filters),
        )

    def can_send_to_remote_planner(self, prompt: str) -> bool:
        name, roll = self._student_identity(prompt)
        if name and re.match(r"^(?:ALL|BOARD|CLASS|EID|GROUP|INTERNAL|MIDTERM|MOCK|MONTHLY|SECTION|YEAR)\b", name):
            name = None
        return name is None and roll is None

    def remote_planner_prompt(self, prompt: str) -> str:
        """Return only locally recognized concepts; raw/unknown tokens never leave the institution."""
        lowered = prompt.lower()
        concepts = sorted({
            concept
            for concept in REMOTE_SAFE_CONCEPTS
            if re.search(rf"\b{re.escape(concept)}\b", lowered)
        })
        filters = self._common_filters(prompt)
        return json.dumps(
            {"recognized_concepts": concepts, "locally_extracted_filters": filters},
            sort_keys=True,
        )

    def interpret_local(self, prompt: str) -> LocalDecision:
        text = " ".join(prompt.strip().split())
        lowered = text.lower().strip(" .!?")
        if re.fullmatch(r"(?:hi|hello|hey|how are you|good (?:morning|afternoon|evening))", lowered):
            return LocalDecision(
                "conversation",
                message="I am ready. Ask me about students, results, attendance, teachers, classes, subjects, or campus performance.",
            )
        if re.search(r"\b(?:what can you do|help me|show capabilities)\b", lowered):
            return LocalDecision(
                "conversation",
                message="I can query the local Daanish School database across all campuses and return a concise answer with supporting rows when useful.",
            )

        catalog_decision = self._catalog_decision(text)
        if catalog_decision is not None:
            return catalog_decision

        name, roll = self._student_identity(text)
        common = self._common_filters(text)
        if name or roll:
            if re.search(r"\battendance|absen(?:t|ce)|present\b", lowered):
                intent = "student_attendance"
            elif re.search(r"\bmarks?|results?|grades?|percentage|score\b", lowered):
                intent = "individual_results"
            else:
                intent = "individual_student"
            return LocalDecision("query", QueryPlan(intent=intent, student_name=name, roll_number=roll, **common))

        words = set(re.findall(r"[a-z]+", lowered))
        if not words.intersection(ACADEMIC_TERMS):
            return LocalDecision("out_of_scope", message="That is outside EduQuery's governed school analytics scope.")

        if (
            re.search(r"\b(?:weak|struggling|low[- ]performing|at risk|(?:below|under|less than)\s+\d{1,3}\s*%?|failing)\b", lowered)
            and re.search(r"\b(?:student|students|results|marks)\b", lowered)
        ):
            intent = "weak_students"
        elif re.search(r"\b(?:top|best|highest|high[- ]performing)\b", lowered) and re.search(r"\bstudents?|results?|marks?\b", lowered):
            intent = "top_students"
        elif re.search(r"\b(?:absent|absence|absences|absentees)\b", lowered):
            intent = "attendance_absence_list"
        elif "attendance" in lowered or "present" in lowered:
            intent = "attendance_summary"
        elif "teacher" in lowered:
            intent = "teacher_performance"
        elif "subject" in lowered or any(subject in lowered for subject in SUBJECTS):
            intent = "subject_performance"
        elif re.search(r"\b(?:roster|enrol(?:lment|led)?|list\s+(?:the\s+)?students?|show\s+(?:\d+\s+)?(?:the\s+)?students?)\b", lowered):
            intent = "student_roster"
        elif "class" in lowered or "section" in lowered or re.search(r"\bgrade\s+(?:level|\d{1,2})\b", lowered):
            intent = "class_performance"
        elif re.search(r"\b(?:compare|performance|summary|average|pass rate)\b", lowered) and re.search(r"\b(?:school|schools|campus|campuses)\b", lowered):
            intent = "school_performance"
        elif re.search(r"\b(?:student|students|roster|enrol(?:lment|led)?)\b", lowered):
            intent = "student_roster"
        else:
            return LocalDecision("provider_required")

        threshold_match = re.search(r"\b(?:below|under|less than)\s+(\d{1,3})(?:\s*%)?", lowered)
        threshold = float(threshold_match.group(1)) if threshold_match else 40.0
        return LocalDecision("query", QueryPlan(intent=intent, threshold=threshold, **common))

    def validate_plan(self, raw: Dict[str, Any]) -> QueryPlan:
        if not isinstance(raw, dict) or raw.get("intent") not in SUPPORTED_INTENTS:
            raise PlanError("The model selected an unsupported analytics intent.")
        requested = str(raw.get("campus") or "ALL").upper()
        if requested not in LIVE_CAMPUSES and requested != "ALL":
            raise PlanError("The model selected an unknown campus code.")

        def optional_int(name: str, lower: int, upper: int) -> Optional[int]:
            value = raw.get(name)
            if value is None:
                return None
            if isinstance(value, bool) or not isinstance(value, int) or not lower <= value <= upper:
                raise PlanError(f"{name} is outside the approved range.")
            return value

        limit = raw.get("limit") or 25
        threshold = raw.get("threshold") if raw.get("threshold") is not None else 40.0
        if isinstance(limit, bool) or not isinstance(limit, int):
            raise PlanError("limit is invalid.")
        if isinstance(threshold, bool) or not isinstance(threshold, (int, float)) or not 0 <= threshold <= 100:
            raise PlanError("threshold is invalid.")
        return QueryPlan(
            intent=raw["intent"], campus=requested,
            class_level=optional_int("class_level", 1, 12),
            section=self._safe_word(raw.get("section"), 20),
            year=optional_int("year", 22, 99),
            subject=self._safe_word(raw.get("subject"), 80),
            house=self._safe_word(raw.get("house"), 80),
            threshold=float(threshold), limit=max(1, min(limit, 100)),
        )

    @staticmethod
    def _safe_word(value: Any, maximum: int) -> Optional[str]:
        if value is None:
            return None
        text = str(value).strip().upper()
        if not re.fullmatch(rf"[A-Z][A-Z0-9 .&'-]{{0,{maximum - 1}}}", text):
            raise PlanError("A filter contains unsupported characters.")
        return text

    def _common_filters(self, prompt: str) -> Dict[str, Any]:
        upper = prompt.upper()
        campus = next((code for code in LIVE_CAMPUSES if re.search(rf"\b{code}\b", upper)), "ALL")
        class_match = re.search(r"\b(?:class|grade)\s*[-:]?\s*(1[0-2]|[1-9])\b", prompt, re.IGNORECASE)
        section_match = re.search(r"\bsection\s*[-:]?\s*([A-Z0-9]{1,3})\b", prompt, re.IGNORECASE)
        year_match = re.search(r"\b(?:year|session)\s*(?:20)?(2[2-9]|[3-9]\d)\b", prompt, re.IGNORECASE)
        house_match = re.search(r"\bhouse\s*[-:]?\s*([A-Za-z][A-Za-z0-9 .&'-]{0,79})", prompt, re.IGNORECASE)
        subject = next((value.upper() for value in SUBJECTS if value in prompt.lower()), None)
        limit_match = re.search(r"\b(?:top|show|list|return)\s+(\d{1,3})\b", prompt, re.IGNORECASE)
        return {
            "campus": campus,
            "class_level": int(class_match.group(1)) if class_match else None,
            "section": section_match.group(1).upper() if section_match else None,
            "year": int(year_match.group(1)) if year_match else None,
            "subject": subject,
            "house": house_match.group(1).strip().upper() if house_match else None,
            "limit": max(1, min(int(limit_match.group(1)), 100)) if limit_match else 25,
        }

    def _catalog_filters(self, prompt: str) -> Dict[str, Any]:
        lowered = prompt.lower()
        common = self._common_filters(prompt)
        name, roll = self._student_identity(prompt)
        if name and re.match(r"^(?:ALL|BOARD|CLASS|EID|GROUP|INTERNAL|MIDTERM|MOCK|MONTHLY|SECTION|YEAR)\b", name):
            name = None
        sms_match = re.search(r"\bSMS(?:\s*(?:number|no))?\s*[:=#-]?\s*(\d+)\b", prompt, re.IGNORECASE)
        eid_match = re.search(r"\bEID\s*[:=#-]?\s*(\d+)\b", prompt, re.IGNORECASE)
        exam = next(
            (value for value in ("ANNUAL", "MIDTERM", "MOCK", "MONTHLY", "CLASS TEST") if value.lower() in lowered),
            None,
        )
        category_match = re.search(r"\bcategory\s+([A-Za-z][A-Za-z ]{0,20})", prompt, re.IGNORECASE)
        category = category_match.group(1).strip().upper() if category_match else None
        if category:
            category = re.split(r"\s+(?:in|for|school|class|teachers?|results?|only)\b", category, maxsplit=1)[0]
        elif "board_career" in lowered:
            category = "BOARD_CAREER"
        elif "middle_career" in lowered:
            category = "MIDDLE_CAREER"
        elif "all sec cat" in lowered:
            category = "ALL SEC CAT"
        group_name = next((value for value in ("SCIENCE", "ARTS") if re.search(rf"\b{value}\b", prompt, re.IGNORECASE)), None)
        metric = self._catalog_metric(lowered)
        operation = "detail"
        if re.search(r"\b(?:how many|count)\b", lowered):
            operation = "count"
        elif re.search(r"\b(?:average|avg|mean)\b", lowered):
            operation = "average"
        elif re.search(r"\b(?:rank|top|highest|lowest|best|worst|position)\b", lowered):
            operation = "rank"
        distinct_field = None
        for phrase, field in (
            ("years available", "school_year"), ("exam types", "exam_type"),
            ("subjects available", "subject"), ("all subjects", "subject"),
            ("all schools", "campus"), ("all sections", "section"),
            ("unique groups", "group_name"),
        ):
            if phrase in lowered:
                operation, distinct_field = "distinct", field
                break
        threshold_match = re.search(r"\b(?:below|under|less than|above|over|greater than)\s+(\d{1,3})(?:\s*%)?", lowered)
        descending = not bool(re.search(r"\b(?:lowest|worst|below|under|less than)\b", lowered))
        return {
            **common,
            "student_name": name,
            "roll_number": roll,
            "student_reference": sms_match.group(1) if sms_match else None,
            "teacher_id": int(eid_match.group(1)) if eid_match else None,
            "exam_type": exam,
            "category": category,
            "group_name": group_name,
            "operation": operation,
            "metric": metric,
            "distinct_field": distinct_field,
            "descending": descending,
            "threshold": float(threshold_match.group(1)) if threshold_match else 40.0,
        }

    @staticmethod
    def _catalog_metric(lowered: str) -> Optional[str]:
        for pattern, metric in (
            (r"class\s*(?:average|avg)", "class_average"),
            (r"pass\s*(?:percentage|%)", "pass_percentage"),
            (r"overall\s*(?:percentage|%)", "percentage"),
            (r"\bpercentage\b|\b%\b", "percentage"),
            (r"\bappeared\b", "appeared"), (r"\bpassed\b", "passed"),
            (r"\bstrength\b", "strength"), (r"\babsent", "absent"),
            (r"below[- ]?70", "below_70"), (r"above[- ]?70", "above_70"),
            (r"\bwork\s*load\b|\bwl\b", "workload"),
            (r"\bposition\b", "position"),
            (r"obtained", "obtained_marks"),
        ):
            if re.search(pattern, lowered):
                return metric
        return None

    @staticmethod
    def _student_identity(prompt: str) -> Tuple[Optional[str], Optional[str]]:
        roll_match = ROLL_PATTERN.search(prompt)
        roll = roll_match.group(1).upper() if roll_match else None
        name = None
        for pattern in NAME_PATTERNS:
            match = pattern.search(prompt)
            if not match:
                continue
            candidate = re.split(
                r"\b(?:in|from|at|with|roll|class|grade|campus|school|year|section)\b",
                match.group(1), maxsplit=1, flags=re.IGNORECASE,
            )[0].strip(" .,'\"")
            rejected = {"results", "marks", "attendance", "profile", "all", *LIVE_CAMPUSES}
            if candidate.upper() not in rejected and candidate.lower() not in rejected and len(candidate) >= 2:
                name = candidate.upper()
                break
        return name, roll

    def compile(self, plan: QueryPlan) -> Tuple[str, List[Any]]:
        if plan.catalog_family:
            return self._compile_catalog(plan)
        if plan.intent not in SUPPORTED_INTENTS:
            raise PlanError("Unsupported semantic intent.")
        return getattr(self, f"_compile_{plan.intent}")(plan)

    def _compile_catalog(self, plan: QueryPlan) -> Tuple[str, List[Any]]:
        try:
            model, columns, default_metric = CATALOG_SPECS[plan.catalog_family or ""]
        except KeyError as exc:
            raise PlanError("Unsupported client catalog family.") from exc
        available = set(columns)
        clauses: List[str] = []
        params: List[Any] = []
        for field, value in (
            ("campus", None if plan.campus == "ALL" else plan.campus),
            ("class_level", plan.class_level), ("section", plan.section),
            ("school_year", plan.year), ("subject", plan.subject),
            ("roll_number", plan.roll_number), ("student_reference", plan.student_reference),
            ("teacher_id", plan.teacher_id), ("exam_type", plan.exam_type),
            ("category", plan.category), ("group_name", plan.group_name),
        ):
            if value is not None and field in available:
                clauses.append(f"{field} = ?")
                params.append(str(value) if plan.catalog_family == "ALL_COMBINED" and field in {"teacher_id", "class_level", "school_year"} else value)
        if plan.student_name and "student_name" in available:
            clauses.append("UPPER(student_name) = ?")
            params.append(plan.student_name)
        where = self._where(clauses)
        metric = plan.metric if plan.metric in available else default_metric
        numeric_metric = f"TRY_CAST({metric} AS float)" if metric and plan.catalog_family in {"ALL_COMBINED", "HOF_FRMT"} else metric
        if plan.operation == "distinct" and plan.distinct_field in available:
            return (f"SELECT DISTINCT {plan.distinct_field} FROM {model} WHERE {where} ORDER BY {plan.distinct_field}", params)
        if plan.operation == "count":
            if metric in {"appeared", "passed", "absent", "strength", "above_70", "below_70"}:
                return (f"SELECT SUM({numeric_metric}) AS matching_count FROM {model} WHERE {where}", params)
            return (f"SELECT COUNT(*) AS matching_count FROM {model} WHERE {where}", params)
        if plan.operation == "average" and metric:
            return (f"SELECT AVG({numeric_metric}) AS average_value FROM {model} WHERE {where}", params)
        selected = ", ".join(columns)
        order = ""
        if plan.operation == "rank" and metric:
            direction = "DESC" if plan.descending else "ASC"
            order = f" ORDER BY {numeric_metric} {direction}"
        return (f"SELECT TOP {plan.limit} {selected} FROM {model} WHERE {where}{order}", params)

    @staticmethod
    def _where(clauses: List[str]) -> str:
        return " AND ".join(clauses) if clauses else "1 = 1"

    @staticmethod
    def _append_common(plan: QueryPlan, clauses: List[str], params: List[Any], alias: str = "") -> None:
        prefix = f"{alias}." if alias else ""
        if plan.campus != "ALL":
            clauses.append(f"{prefix}campus = ?")
            params.append(plan.campus)
        if plan.class_level is not None:
            clauses.append(f"{prefix}class_level = ?")
            params.append(plan.class_level)
        if plan.section:
            clauses.append(f"{prefix}section = ?")
            params.append(plan.section)
        if plan.year is not None:
            clauses.append(f"{prefix}school_year = ?")
            params.append(plan.year)

    @staticmethod
    def _append_identity(plan: QueryPlan, clauses: List[str], params: List[Any], alias: str = "") -> None:
        prefix = f"{alias}." if alias else ""
        if plan.roll_number:
            clauses.append(f"{prefix}roll_number = ?")
            params.append(plan.roll_number)
        if plan.student_name:
            clauses.append(f"UPPER({prefix}student_name) = ?")
            params.append(plan.student_name)

    def _compile_student_roster(self, plan: QueryPlan) -> Tuple[str, List[Any]]:
        clauses: List[str] = []
        params: List[Any] = []
        self._append_common(plan, clauses, params)
        if plan.house:
            clauses.append("house = ?")
            params.append(plan.house)
        return (f"SELECT TOP {plan.limit} campus, class_level, section, house, roll_number, student_name FROM student_enrollment WHERE {self._where(clauses)} ORDER BY campus, class_level, section, roll_number", params)

    def _compile_individual_student(self, plan: QueryPlan) -> Tuple[str, List[Any]]:
        clauses: List[str] = []
        params: List[Any] = []
        self._append_common(plan, clauses, params)
        self._append_identity(plan, clauses, params)
        return (f"SELECT TOP {plan.limit} campus, class_level, section, house, school_year, roll_number, student_name FROM student_enrollment WHERE {self._where(clauses)} ORDER BY school_year DESC, campus", params)

    def _compile_individual_results(self, plan: QueryPlan) -> Tuple[str, List[Any]]:
        clauses: List[str] = []
        params: List[Any] = []
        self._append_common(plan, clauses, params)
        self._append_identity(plan, clauses, params)
        if plan.subject:
            clauses.append("subject = ?")
            params.append(plan.subject)
        return (f"SELECT TOP {plan.limit} campus, roll_number, student_name, class_level, section, school_year, exam_type, subject, total_marks, obtained_marks, percentage, grade, result_status FROM student_result_card WHERE {self._where(clauses)} ORDER BY school_year DESC, exam_type, subject", params)

    def _compile_student_attendance(self, plan: QueryPlan) -> Tuple[str, List[Any]]:
        clauses: List[str] = []
        params: List[Any] = []
        self._append_common(plan, clauses, params, "s")
        self._append_identity(plan, clauses, params, "s")
        return (f"SELECT DISTINCT TOP {plan.limit} a.campus, s.roll_number, s.student_name, a.house, a.attendance_date, a.status FROM house_attendance AS a JOIN student_enrollment AS s ON a.campus = s.campus AND a.student_reference = s.student_reference WHERE {self._where(clauses)} ORDER BY a.attendance_date DESC", params)

    def _compile_weak_students(self, plan: QueryPlan) -> Tuple[str, List[Any]]:
        clauses = ["source_subject = ?", "percentage < ?"]
        params: List[Any] = [plan.subject or "TOTAL", plan.threshold]
        self._append_common(plan, clauses, params)
        return (f"SELECT TOP {plan.limit} campus, class_level, section, roll_number, student_name, percentage, final_status FROM consolidated_results WHERE {self._where(clauses)} ORDER BY percentage ASC, campus, class_level, section", params)

    def _compile_top_students(self, plan: QueryPlan) -> Tuple[str, List[Any]]:
        clauses: List[str] = ["source_subject = ?"]
        params: List[Any] = [plan.subject or "TOTAL"]
        self._append_common(plan, clauses, params)
        return (f"SELECT TOP {plan.limit} campus, class_level, section, roll_number, student_name, percentage, final_status FROM consolidated_results WHERE {self._where(clauses)} ORDER BY percentage DESC, campus, class_level, section", params)

    def _compile_attendance_summary(self, plan: QueryPlan) -> Tuple[str, List[Any]]:
        clauses: List[str] = []
        params: List[Any] = []
        if plan.campus != "ALL":
            clauses.append("campus = ?")
            params.append(plan.campus)
        if plan.house:
            clauses.append("house = ?")
            params.append(plan.house)
        return ("SELECT campus, house, COUNT(*) AS attendance_records, SUM(CASE WHEN UPPER(status) = 'PRESENT' THEN 1 ELSE 0 END) AS present_count, SUM(CASE WHEN UPPER(status) = 'ABSENT' THEN 1 ELSE 0 END) AS absent_count, MAX(attendance_date) AS latest_attendance_date FROM house_attendance WHERE " + self._where(clauses) + " GROUP BY campus, house ORDER BY campus, house", params)

    def _compile_attendance_absence_list(self, plan: QueryPlan) -> Tuple[str, List[Any]]:
        clauses = ["UPPER(status) = 'ABSENT'"]
        params: List[Any] = []
        if plan.campus != "ALL":
            clauses.append("campus = ?")
            params.append(plan.campus)
        if plan.house:
            clauses.append("house = ?")
            params.append(plan.house)
        return (f"SELECT TOP {plan.limit} campus, house, student_reference, attendance_date, status FROM house_attendance WHERE {self._where(clauses)} ORDER BY attendance_date DESC", params)

    def _compile_teacher_performance(self, plan: QueryPlan) -> Tuple[str, List[Any]]:
        clauses: List[str] = []
        params: List[Any] = []
        self._append_common(plan, clauses, params)
        if plan.subject:
            clauses.append("subject = ?")
            params.append(plan.subject)
        return (f"SELECT TOP {plan.limit} campus, teacher_name, subject, class_level, section, strength, passed, pass_percentage, class_average FROM teacher_results WHERE {self._where(clauses)} ORDER BY pass_percentage DESC, class_average DESC", params)

    def _compile_class_performance(self, plan: QueryPlan) -> Tuple[str, List[Any]]:
        clauses: List[str] = []
        params: List[Any] = []
        self._append_common(plan, clauses, params)
        if plan.subject:
            clauses.append("subject = ?")
            params.append(plan.subject)
        return ("SELECT campus, class_level, section, COUNT(*) AS subject_records, AVG(pass_percentage) AS average_pass_percentage, AVG(class_average) AS average_marks FROM teacher_results WHERE " + self._where(clauses) + " GROUP BY campus, class_level, section ORDER BY average_pass_percentage ASC, average_marks ASC", params)

    def _compile_subject_performance(self, plan: QueryPlan) -> Tuple[str, List[Any]]:
        clauses: List[str] = []
        params: List[Any] = []
        self._append_common(plan, clauses, params)
        if plan.subject:
            clauses.append("subject = ?")
            params.append(plan.subject)
        return ("SELECT campus, subject, COUNT(*) AS class_records, AVG(pass_percentage) AS average_pass_percentage, AVG(class_average) AS average_marks FROM teacher_results WHERE " + self._where(clauses) + " GROUP BY campus, subject ORDER BY average_pass_percentage ASC, average_marks ASC", params)

    def _compile_school_performance(self, plan: QueryPlan) -> Tuple[str, List[Any]]:
        clauses: List[str] = []
        params: List[Any] = []
        if plan.campus != "ALL":
            clauses.append("campus = ?")
            params.append(plan.campus)
        if plan.year is not None:
            clauses.append("school_year = ?")
            params.append(plan.year)
        return ("SELECT campus, COUNT(*) AS class_subject_records, AVG(pass_percentage) AS average_pass_percentage, AVG(class_average) AS average_marks FROM teacher_results WHERE " + self._where(clauses) + " GROUP BY campus ORDER BY average_pass_percentage DESC, average_marks DESC", params)
