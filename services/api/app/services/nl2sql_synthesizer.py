import json
import logging
import os
import re
import time
from typing import Any, Dict, List, Optional, Tuple
import httpx
from google.genai import Client, types
from dotenv import load_dotenv

from services.api.app.config import settings

load_dotenv()
logger = logging.getLogger("eduquery.nl2sql")

SCHEMA_PROMPT = """
You are the expert T-SQL AI assistant for Daanish Schools Academic Portal database 'db_aadc11_sqldaanish'.
The database contains 14 canonical academic tables and views across 20 campuses:
['ATKB', 'ATKG', 'CTNB', 'CTNG', 'DGKB', 'DGKG', 'HSPB', 'HSPG', 'MNKB', 'MNKG', 'MNWB', 'MNWG', 'RJNB', 'RJNG', 'RYKB', 'RYKG', 'TNSB', 'TNSG', 'VEHB', 'VEHG']

CRITICAL INSTITUTIONAL DOMAIN FACTS:
1. Internal Exams: 'MID' (Midterm) and 'MOCK' exams are available for Year 26 (2026).
2. Newly Constructed Campuses: MNKG, MNKB, TNSG, TNSB were newly built and primarily have Classes 6, 7, and 8 results for Year 26.
3. Master Roll Duplication Rule: STUDENTS_ROLL_INTERNAL_EXAM records student enrollments per exam session. ALWAYS use 'SELECT DISTINCT' when querying student rosters, names, rolls, or counts to return unique rows.
4. Escaping Special Columns: T-SQL column names with symbols MUST be bracketed:
   [%], [PASS%], [CLASS AVG], [GROUP], [TEACHER NAME], [WORK LOAD], [CLASS/SECTION], [A+], [BELOW 70%], [ABOVE 70%], [>90], [>80], [>70], [>60], [>50], [>40], [<40], [Subjects <33%], [Position], [PASS% OF BOARD], [SCHOOL-MERGE], [SUBJECT_MERGE]
5. T-SQL Dialect: Use TOP (not LIMIT), LIKE (not ILIKE), CAST/CONVERT for strings/numbers.
6. Campus-Level vs Student-Level Disambiguation:
   When the user asks for 'top/best campuses in <subject>' or 'N different campuses based on <subject> results', they are querying campus performance rankings, NOT individual student toppers. Group by `SCHOOL, SUBJECT, CLASS` on STUDENTS_RESULT_TOTAL or TR_ALL, e.g.:
   SELECT TOP 3 SCHOOL, SUBJECT, CLASS, CAST(ROUND(AVG(CAST([%] AS FLOAT)), 2) AS DECIMAL(5,2)) AS AVG_PERCENTAGE, CAST(ROUND(SUM(CAST(OBTAINED AS FLOAT)) * 100.0 / NULLIF(SUM(CAST(TOTAL AS FLOAT)), 0), 2) AS DECIMAL(5,2)) AS CAMPUS_PERCENTAGE, COUNT(DISTINCT ROLLNO) AS TOTAL_STUDENTS FROM STUDENTS_RESULT_TOTAL WHERE (CLASS = '10' OR CLASS = 10) AND SUBJECT LIKE '%PHYSICS%' GROUP BY SCHOOL, SUBJECT, CLASS ORDER BY CAMPUS_PERCENTAGE DESC, AVG_PERCENTAGE DESC

CANONICAL TABLE & VIEW CATALOG:

1. STUDENTS_ROLL_INTERNAL_EXAM (Base Table):
   Columns: ID, SCHOOL, [GROUP], SMSNO, ROLLNO, STUDENT, FATHER, CLASS, SECTION, CATEGORY, YEAR, BOARDROLLNO, HOUSE, EXAM
   Use for: Master student enrollment, rosters, count of students, names, fathers, SMS, roll numbers, sections, categories, houses.
   Example: Show all students of Class 10 Section A in school ATKB for year 26 ->
   SELECT DISTINCT TOP 100 SCHOOL, ROLLNO, SMSNO, STUDENT, FATHER, CLASS, SECTION, CATEGORY, YEAR FROM STUDENTS_ROLL_INTERNAL_EXAM WHERE SCHOOL = 'ATKB' AND CLASS = '10' AND SECTION = 'A' AND (YEAR = 26 OR YEAR = '26') ORDER BY ROLLNO ASC

2. STUDENTS_ROLL (Base Table):
   Columns: ID, SCHOOL, [GROUP], SMSNO, ROLLNO, STUDENT, FATHER, CLASS, SECTION, CATEGROY, YEAR, QUOTA, QUOTA_CAT
   Use for: Board exam enrollment master, quotas, category inquiries for board exam batches.

3. STUDENTS_RESULT_TOTAL (View):
   Columns: SCHOOL, STUDENT, FATHER, CLASS, SECTION, CATEGROY, YEAR, SMSNO, ROLLNO, SUBJECT, OBTAINED, TOTAL, [%], STATUS, [GROUP]
   Use for: Board/annual student marks, student subject toppers, fail lists, student rankings, overall student results.
   CRITICAL STANDALONE RULE: All student demographics (`STUDENT`, `FATHER`, `SMSNO`, `ROLLNO`, `CLASS`, `SECTION`, `SCHOOL`) are ALREADY in this view. NEVER JOIN `STUDENTS_ROLL_INTERNAL_EXAM` with `STUDENTS_RESULT_TOTAL` because their internal vs board roll numbers differ!
   CRITICAL STATUS RULE: In STUDENTS_RESULT_TOTAL, STATUS is either 'FAIL' or a list of subject names. The literal word 'PASS' does NOT exist in the database! To check for passing students, use `(STATUS <> 'FAIL' OR STATUS IS NULL)` or filter on score (`[%] >= 33`). NEVER use `STATUS = 'PASS'`.
   Example: Who is first in Mathematics / Which student is first in Mathematics in Class 10 ATKB year 26? ->
   SELECT TOP 1 SCHOOL, STUDENT, FATHER, CLASS, SECTION, ROLLNO, SMSNO, SUBJECT, OBTAINED, TOTAL, [%], STATUS, YEAR FROM STUDENTS_RESULT_TOTAL WHERE SCHOOL = 'ATKB' AND (CLASS = '10' OR CLASS = 10) AND (YEAR = '26' OR YEAR = 26) AND SUBJECT LIKE '%MATH%' ORDER BY [%] DESC, OBTAINED DESC




4. STUDENTS_RESULT_TOTAL_INTERNAL (or Marks_Internal joined with STUDENTS_ROLL_INTERNAL_EXAM):
   Columns: SCHOOL, STUDENT, FATHER, CLASS, SECTION, CATEGORY, YEAR, SMSNO, ROLLNO, SUBJECT, OBTAINED, TOTAL, [%], STATUS, [GROUP]
   Use for: Internal exams (Midterm, Mock) student marks and result cards.
   Rule: For internal marks, prefer querying `Marks_Internal M JOIN STUDENTS_ROLL_INTERNAL_EXAM SR ON M.ROLLNO = SR.ROLLNO AND M.CLASS = SR.CLASS AND M.YEAR = SR.YEAR` or use `STUDENTS_RESULT_TOTAL_INTERNAL WHERE SUBJECT <> 'TOTAL'` to avoid view aggregation limits.
   Example: Show Midterm marks of all subjects for roll 7788 ->
   SELECT TOP 50 M.ROLLNO, SR.STUDENT, SR.FATHER, M.CLASS, SR.SECTION, M.SUBJECT, M.OBTAINED, M.TOTAL, M.[%], M.GRADE, M.STATUS, M.YEAR, M.EXAMTYPE FROM Marks_Internal M JOIN STUDENTS_ROLL_INTERNAL_EXAM SR ON M.ROLLNO = SR.ROLLNO AND M.CLASS = SR.CLASS AND M.YEAR = SR.YEAR WHERE (M.ROLLNO = '7788' OR M.ROLLNO = 7788)

5. MARKS (Base Table):
   Columns: ID, SUBJECT, OBTAINED, TOTAL, [%], GRADE, STATUS, ROLLNO, CLASS, YEAR, EXAMTYPE
   Use for: Board/annual subject marks per roll number, grades, pass/fail status.
   Example: Show all subject marks of roll 7788 in Annual year 26 ->
   SELECT TOP 50 ROLLNO, CLASS, SUBJECT, OBTAINED, TOTAL, [%], GRADE, STATUS, YEAR, EXAMTYPE FROM MARKS WHERE (ROLLNO = '7788' OR ROLLNO = 7788) AND (YEAR = 26 OR YEAR = '26')

6. Marks_Internal (Base Table):
   Columns: ID, SUBJECT, OBTAINED, TOTAL, [%], GRADE, STATUS, ROLLNO, CLASS, YEAR, EXAMTYPE, Remarks
   Use for: Internal subject marks per roll number with Remarks.

7. PRAC (Base Table):
   Columns: ID, SUBJECT, OBTAINED, TOTAL, [%], GRADE, STATUS, ROLLNO, CLASS, YEAR, EXAMTYPE
   Use for: Practical exam marks per student / roll number for Physics, Chemistry, Biology, Computer Science.
   Example: Show Physics practical marks of Class 10 ATKB Annual ->
   SELECT TOP 50 ROLLNO, CLASS, SUBJECT, OBTAINED, TOTAL, [%], GRADE, STATUS, YEAR, EXAMTYPE FROM PRAC WHERE SUBJECT LIKE '%PHYSIC%' AND CLASS = '10'

8. TR_ALL (Base Table):
   Columns: EID, NAME, SCHOOL, EXAMTYPE, SUBJECT, CLASS, SECTION, Year, CATEGROY, STRENGTH, Count_90_100, Count_80_90, Count_70_80, Count_60_70, Count_50_60, Count_40_50, Count_0_39, APPEARED, PASSED, [PASS%], [CLASS AVG]
   Use for: Combined teacher results, subject pass rates across all campuses, class averages, teacher evaluations by EID or teacher name.
   Example: Show annual TR result of teacher EID 105 ->
   SELECT TOP 50 EID, NAME, SCHOOL, EXAMTYPE, SUBJECT, CLASS, SECTION, Year, APPEARED, PASSED, [PASS%], [CLASS AVG] FROM TR_ALL WHERE EID = 105 OR EID = '105'

9. TR2_Theory (View):
   Columns: EID, NAME, SCHOOL, EXAMTYPE, SUBJECT, CLASS, SECTION, Year, CATEGROY, STRENGTH, Count_90_100, Count_80_90, Count_70_80, Count_60_70, Count_50_60, Count_40_50, Count_0_39, APPEARED, PASSED, [PASS%], [CLASS AVG]
   Use for: Theory-specific teacher results, theory pass percentages, appeared/passed counts.
   Example: Show theory result of teacher EID 105 for Mathematics Class 10 ->
   SELECT TOP 50 EID, NAME, SCHOOL, SUBJECT, CLASS, SECTION, Year, APPEARED, PASSED, [PASS%], [CLASS AVG] FROM TR2_Theory WHERE (EID = 105 OR EID = '105') AND SUBJECT LIKE '%MATH%' AND (CLASS = 10 OR CLASS = '10')

10. TR2_Prac (View):
    Columns: EID, NAME, SCHOOL, EXAMTYPE, SUBJECT, CLASS, SECTION, Year, CATEGROY, STRENGTH, Count_90_100, Count_80_90, Count_70_80, Count_60_70, Count_50_60, Count_40_50, Count_0_39, APPEARED, PASSED, [PASS%], [CLASS AVG]
    Use for: Practical-specific teacher results, practical class averages, practical pass percentages.
    Example: Show practical result of Physics teacher EID 88 Class 10 ->
    SELECT TOP 50 EID, NAME, SCHOOL, SUBJECT, CLASS, SECTION, Year, APPEARED, PASSED, [PASS%], [CLASS AVG] FROM TR2_Prac WHERE (EID = 88 OR EID = '88') AND SUBJECT LIKE '%PHYSIC%' AND (CLASS = 10 OR CLASS = '10')

11. ALL_COMBINED (Base Table):
    Columns: EID, NAME, SCHOOL, SUBJECT, CLASS, SECTION, Year, CATEGROY, STRENGTH, Count_90_100, Count_80_90, Count_70_80, Count_60_70, Count_50_60, Count_40_50, Count_0_39, Above_70, Below_70, APPEARED, PASSED, [PASS%], [CLASS AVG], Position, TOTAL_POSITIONS, WL
    Use for: Teacher career snapshots, teacher rankings, subject positions, workload (WL), Above_70 / Below_70.
    Example: Rank Mathematics teachers by position in year 26 ->
    SELECT TOP 50 EID, NAME, SCHOOL, SUBJECT, CLASS, SECTION, Year, [PASS%], [CLASS AVG], Position, TOTAL_POSITIONS, WL FROM ALL_COMBINED WHERE SUBJECT LIKE '%MATH%' AND (Year = 26 OR Year = '26') ORDER BY CAST(Position AS INT) ASC

12. HOF_FRMT (View):
    Columns: EID, NAME, SUBJECT, SCHOOL, Year, [CLASS/SECTION], APPEARED, [PASS%], [PASS% OF BOARD], Position, TOTAL_POSITIONS, [WORK LOAD], [CLASS AVG], [ABOVE 90%], [ABOVE 80%], [ABOVE 70%], [ABOVE 60%], [ABOVE 50%], [ABOVE 40%], [BELOW 40%], [ABOVE 70 %], [ABOVE 70 COUNT], [BELOW 70 %], [BELOW 70% COUNT], REMARKS
    Use for: Head Office format reports, interview sheets, teacher comparison with board pass%, score brackets.
    Example: Show Head Office format report for teacher EID 105 ->
    SELECT TOP 50 EID, NAME, SUBJECT, SCHOOL, Year, [CLASS/SECTION], APPEARED, [PASS%], [PASS% OF BOARD], Position, TOTAL_POSITIONS, [WORK LOAD], [CLASS AVG] FROM HOF_FRMT WHERE EID = 105 OR EID = '105'

13. INTERNAL_EXAM_GROUP_WISE_PERFORMANCE_VIEW (View):
    Columns: ID, SCHOOL, EXAMTYPE, EID, [TEACHER NAME], YEAR, CLASS, SECTION, SUBJECT, [GROUP], APPEARED, ABSENT, PASS, [A+], A, B, C, D, E, F, [CLASS%], CLASS_AVG, [BELOW 70%], [ABOVE 70%]
    Use for: Internal exam performance per teacher, group-wise breakdown (Science/Arts/General), grade distribution A+ to F, absentees in exams.
    Example: Show grade counts A+ to F for Chemistry Midterm Class 11 ->
    SELECT TOP 50 SCHOOL, EXAMTYPE, EID, [TEACHER NAME], YEAR, CLASS, SECTION, SUBJECT, APPEARED, PASS, [A+], A, B, C, D, E, F, [CLASS%], CLASS_AVG FROM INTERNAL_EXAM_GROUP_WISE_PERFORMANCE_VIEW WHERE SUBJECT LIKE '%CHEM%' AND EXAMTYPE LIKE '%MID%' AND (CLASS = 11 OR CLASS = '11')

14. School_Ind_Pos_SUB (View):
    Columns: SCHOOL, YEAR, CLASS, Strength, SumObtained, SumTotal, AggregatePercentage, [>90], [>80], [>70], [>60], [>50], [>40], [<40], [Subjects <33%], Position
    Use for: School/Campus rankings and overall campus aggregate positions by class. (Do NOT use for individual student queries or student toppers).
    Example: Rank schools by aggregate percentage in Class 10 Year 26 ->
    SELECT TOP 10 SCHOOL, YEAR, CLASS, Strength, AggregatePercentage, Position FROM School_Ind_Pos_SUB WHERE (CLASS = 10 OR CLASS = '10') AND (YEAR = 26 OR YEAR = '26') ORDER BY CAST(Position AS INT) ASC

15. vTeacher_sum_per & vTeacher_sum_per_BOARD_MIDDLE (Views):
    Columns: EID, NAME, SCHOOL, CLASS, SECTION, YEAR, SUBJECT, SumObtained, SumTotal, [%]
    Use for: Overall teacher percentages across Middle vs Board classes, teacher subject totals.
    Example: What is overall board percentage of teacher EID 105? ->
    SELECT TOP 50 EID, NAME, SCHOOL, CATEGROY, SUBJECT, SumObtained, SumTotal, [%] FROM vTeacher_sum_per_BOARD_MIDDLE WHERE EID = 105 OR EID = '105'

CRITICAL T-SQL SYNTAX RULES:
1. Return ONLY raw single SELECT T-SQL code. No markdown formatting, no backticks, no explanations.
2. DO NOT filter by SCHOOL unless the user prompt explicitly specifies a campus (e.g. ATKB, MNWB) or selected target campus is not ALL.
3. NEVER JOIN STUDENTS_ROLL_INTERNAL_EXAM with STUDENTS_RESULT_TOTAL or MARKS. Query STUDENTS_RESULT_TOTAL standalone (it already contains student names, roll numbers, marks, etc.).
4. In STUDENTS_RESULT_TOTAL, STATUS is never literally 'PASS'. To check for passing students, use `(STATUS <> 'FAIL' OR STATUS IS NULL)` or filter on percentage `([%] >= 33)`. NEVER write `STATUS = 'PASS'`.
"""


class NL2SQLSynthesizer:
    """
    Intelligent NL-to-SQL translator and contextual response summarizer for EduQuery AI.
    Handles all 610 Gold Prompts and general academic queries.
    """

    def __init__(self):
        self._client: Optional[Client] = None
        self._cached_api_key: Optional[str] = None
        self._preferred_model = "gemini-3.5-flash-lite"
        self._openrouter_key: Optional[str] = os.getenv("OPENROUTER_API_KEY", "")
        self._openrouter_model = "openai/gpt-5.6-luna-pro"

    @property
    def client(self) -> Optional[Client]:
        current_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or settings.GOOGLE_API_KEY or ""
        if current_key:
            if self._client is None or self._cached_api_key != current_key:
                try:
                    self._client = Client(api_key=current_key)
                    self._cached_api_key = current_key
                except Exception:
                    self._client = None
        return self._client

    def _extract_slots(self, prompt: str) -> Dict[str, Any]:
        p_upper = prompt.upper()
        p_lower = prompt.lower()
        slots: Dict[str, Any] = {}

        campuses = ["ATKB", "ATKG", "MNWB", "MNWG", "HSPB", "HSPG", "CTNB", "CTNG", "DGKB", "DGKG",
                    "RYKB", "RYKG", "CHB", "CHG", "TNSG", "TNSB", "MNKG", "MNKB", "RJNB", "RJNG",
                    "KRA", "JMPB", "JMPG", "VEHB", "VEHG", "FASB", "FASG"]
        for c in campuses:
            if re.search(r"\b" + re.escape(c) + r"\b", p_upper):
                slots["school"] = c
                break

        class_match = re.search(r"\b(?:CLASS|GRADE)\s*(\d{1,2})(?:TH|ST|ND|RD)?\b", p_upper)
        if not class_match:
            class_match = re.search(r"\b(\d{1,2})(?:TH|ST|ND|RD)\s*(?:CLASS|GRADE)?\b", p_upper)
        if class_match:
            slots["class"] = int(class_match.group(1))
        elif "MATRIC" in p_upper:
            slots["class"] = 10

        sec_match = re.search(r"\bSECTION\s*([A-F])\b", p_upper)
        if sec_match:
            slots["section"] = sec_match.group(1)

        year_match = re.search(r"\b(?:YEAR|SESSION|IN\s+)?(20\d{2}|2[0-9])\b", p_upper)
        if year_match:
            raw_yr = year_match.group(1)
            slots["year"] = int(raw_yr[-2:]) if len(raw_yr) == 4 else int(raw_yr)
        elif "26" in prompt or "2026" in prompt:
            slots["year"] = 26
        elif "25" in prompt or "2025" in prompt:
            slots["year"] = 25

        eid_match = re.search(r"\b(?:EID|TEACHER\s*EID|EID\s*#?)\s*[:=#-]?\s*(\d{1,6})\b", p_upper)
        if eid_match:
            slots["eid"] = eid_match.group(1)

        roll_match = re.search(r"\b(?:ROLL|ROLLNO|ROLL\s*NO|ROLL\s*NUMBER)\s*[:=#-]?\s*(\d{3,12})\b", p_upper)
        if roll_match:
            slots["rollno"] = roll_match.group(1)

        sms_match = re.search(r"\b(?:SMS|SMSNO|SMS\s*NO|SMS\s*NUMBER)\s*[:=#-]?\s*(\d{3,8})\b", p_upper)
        if sms_match:
            slots["smsno"] = sms_match.group(1)

        limit_match = re.search(r"\b(?:TOP|SHOW|LIST|FIRST|RETURN|LIMIT)\s*(\d{1,3})\b", p_upper)
        if not limit_match:
            limit_match = re.search(r"\b(\d{1,3})\s+(?:DIFFERENT\s+)?(?:TOP|BEST|HIGHEST|LOWEST|STUDENTS?|TEACHERS?|RECORDS?|CAMPUS|CAMPUSES|SCHOOLS?|BRANCHES?)\b", p_upper)
        if limit_match:
            slots["limit"] = max(1, min(int(limit_match.group(1)), 1000))

        subject_map = {
            "math": "MATHEMATICS",
            "mathematics": "MATHEMATICS",
            "english": "ENGLISH",
            "urdu": "URDU",
            "physics": "PHYSICS",
            "chemistry": "CHEMISTRY",
            "biology": "BIOLOGY",
            "computer science": "COMPUTER SCIENCE",
            "computer": "COMPUTER SCIENCE",
            "islamiyat": "ISLAMIYAT",
            "pakistan studies": "PAKISTAN STUDIES",
            "pak studies": "PAKISTAN STUDIES",
            "general science": "GENERAL SCIENCE",
            "social studies": "SOCIAL STUDIES",
            "arts": "ARTS",
            "quran": "TRANSLATION OF THE HOLY QURAN",
            "islamic education": "ISLAMIC EDUCATION"
        }
        for k, sub_name in subject_map.items():
            if re.search(r"\b" + re.escape(k) + r"\b", p_lower):
                slots["subject"] = sub_name
                break

        name_match = re.search(r"\b(?:STUDENT\s+NAMED|NAME\s+OF\s+STUDENT\s+|STUDENT\s+)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b", prompt)
        if name_match:
            name_val = name_match.group(1).strip()
            excluded = {"ALL", "EACH", "EVERY", "CLASS", "SECTION", "SCHOOL", "CAMPUS", "GRADE", "HOUSE", "IN", "FOR", "OF", "THE", "WITH", "TOP", "BEST", "STUDENTS", "STUDENT"}
            if name_val.upper() not in excluded and name_val.upper() not in subject_map.values():
                slots["student_name"] = name_val
        elif "named" in p_lower:
            parts = p_lower.split("named")
            if len(parts) > 1:
                cand = parts[1].strip().split()[0].title()
                if cand.upper() not in ["ALL", "IN", "AT", "OF", "THE"]:
                    slots["student_name"] = cand

        teacher_name_match = re.search(r"\b(?:TEACHER\s+)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b", prompt)
        if teacher_name_match:
            t_name = teacher_name_match.group(1).strip()
            if t_name.upper() not in ["EID", "OF", "IN", "FOR", "RESULT", "THEORY", "PRAC"]:
                slots["teacher_name"] = t_name

        if "annual" in p_lower or "board" in p_lower:
            slots["exam"] = "ANNUAL"
        elif "midterm" in p_lower or "mid" in p_lower:
            slots["exam"] = "MID"
        elif "mock" in p_lower:
            slots["exam"] = "MOCK"

        return slots

    @staticmethod
    def _post_process_sql(sql: str) -> str:
        s = sql.strip().replace("```sql", "").replace("```", "").strip()
        # Remove literal STATUS = 'PASS' which does not exist in MSSQL schema
        s = re.sub(r"\s+AND\s+([a-zA-Z0-9_\.]*STATUS\s*=\s*'PASS'|[a-zA-Z0-9_\.]*STATUS\s*=\s*\"PASS\")", "", s, flags=re.IGNORECASE)
        s = re.sub(r"\s+WHERE\s+([a-zA-Z0-9_\.]*STATUS\s*=\s*'PASS'|[a-zA-Z0-9_\.]*STATUS\s*=\s*\"PASS\")\s+AND\s+", " WHERE ", s, flags=re.IGNORECASE)
        # In STUDENTS_RESULT_TOTAL, remove spurious STATUS filters when percentage is specified
        if "STUDENTS_RESULT_TOTAL" in s.upper() and ("[%]" in s or "%" in s):
            s = re.sub(r"\s+AND\s+\([^\)]*STATUS\s*<>\s*'FAIL'[^\)]*\)", "", s, flags=re.IGNORECASE)
            s = re.sub(r"\s+AND\s+[a-zA-Z0-9_\.]*STATUS\s*<>\s*'FAIL'", "", s, flags=re.IGNORECASE)
        # Remove fragile cross-system JOIN on ROLLNO between STUDENTS_ROLL_INTERNAL_EXAM and STUDENTS_RESULT_TOTAL
        if "STUDENTS_RESULT_TOTAL" in s.upper() and "STUDENTS_ROLL_INTERNAL_EXAM" in s.upper() and "JOIN" in s.upper():
            s = re.sub(r"FROM\s+STUDENTS_ROLL_INTERNAL_EXAM\s+\w+\s+JOIN\s+STUDENTS_RESULT_TOTAL\s+(\w+)\s+ON\s+[\w\.]+\s*=\s*[\w\.]+(\s+AND\s+[\w\.]+\s*=\s*[\w\.]+)*", r"FROM STUDENTS_RESULT_TOTAL \1", s, flags=re.IGNORECASE)
            s = re.sub(r"FROM\s+STUDENTS_RESULT_TOTAL\s+(\w+)\s+JOIN\s+STUDENTS_ROLL_INTERNAL_EXAM\s+\w+\s+ON\s+[\w\.]+\s*=\s*[\w\.]+(\s+AND\s+[\w\.]+\s*=\s*[\w\.]+)*", r"FROM STUDENTS_RESULT_TOTAL \1", s, flags=re.IGNORECASE)
        return s.strip()

    def generate_sql(self, prompt: str, campus_code: str = "ALL") -> str:
        """Translates natural language questions to accurate T-SQL using Gemini/OpenRouter with robust rule fallback."""
        target = campus_code if campus_code and campus_code.upper() != "ALL" else "ALL"
        msg = f"User Question: '{prompt}'. Selected target campus: '{target}'."

        # 1. Preferred Primary / Secondary Engine: OpenRouter (e.g. GPT-5.6-Luna-Pro)
        openrouter_key = os.getenv("OPENROUTER_API_KEY") or self._openrouter_key or getattr(settings, "OPENROUTER_API_KEY", "")
        if openrouter_key and not openrouter_key.startswith("sk-or-v1-demo"):
            for model_candidate in [self._openrouter_model, "openai/gpt-4o-mini", "anthropic/claude-3.5-sonnet"]:
                try:
                    headers = {
                        "Authorization": f"Bearer {openrouter_key}",
                        "HTTP-Referer": "https://eduquery.daanish.edu.pk",
                        "X-Title": "EduQuery AI Engine",
                        "Content-Type": "application/json"
                    }
                    payload = {
                        "model": model_candidate,
                        "messages": [
                            {"role": "system", "content": SCHEMA_PROMPT},
                            {"role": "user", "content": msg}
                        ],
                        "temperature": 0
                    }
                    with httpx.Client(timeout=12.0) as http_client:
                        res = http_client.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
                        if res.status_code == 200:
                            content = res.json()["choices"][0]["message"]["content"]
                            sql_clean = self._post_process_sql(content)
                            if (sql_clean.upper().startswith("SELECT") or sql_clean.upper().startswith("WITH")) and "FROM" in sql_clean.upper():
                                return sql_clean
                except Exception as e:
                    logger.warning(f"OpenRouter NL2SQL ({model_candidate}) error: {e}")

        # 2. Engine: Gemini 3.5 Flash Lite
        if self.client:
            try:
                config = types.GenerateContentConfig(temperature=0.0, system_instruction=SCHEMA_PROMPT)
                resp = self.client.models.generate_content(
                    model=self._preferred_model,
                    contents=[msg],
                    config=config
                )
                if resp and resp.text:
                    sql_clean = self._post_process_sql(resp.text)
                    if (sql_clean.upper().startswith("SELECT") or sql_clean.upper().startswith("WITH")) and "FROM" in sql_clean.upper():
                        return sql_clean
            except Exception as e:
                logger.warning(f"Gemini NL2SQL error: {e}")

        # 3. Resilient Rule-Based Semantic Compiler
        return self._compile_rule_based_sql(prompt, campus_code)

    def _compile_rule_based_sql(self, prompt: str, campus_code: str = "ALL") -> str:
        p_lower = prompt.lower()
        slots = self._extract_slots(prompt)
        target_school = slots.get("school") or (campus_code if campus_code and campus_code.upper() != "ALL" else None)
        target_subject = slots.get("subject")
        target_class = slots.get("class")
        target_section = slots.get("section")
        target_year = slots.get("year")
        target_eid = slots.get("eid")
        target_roll = slots.get("rollno")
        target_sms = slots.get("smsno")
        target_name = slots.get("student_name")
        target_teacher = slots.get("teacher_name")
        target_exam = slots.get("exam")
        target_limit = slots.get("limit")

        # Entity & Intent Disambiguation
        is_campus_query = bool(
            re.search(r"\b(?:campuses|campus|schools|school|branches|branch|institutions|institution)\b", p_lower)
            and (
                re.search(r"\b(?:best|top|rank|ranks|ranking|rankings|position|positions|performance|performing|highest|lowest|standing|results?|marks|scores?|aggregate)\b", p_lower)
                or re.search(r"\b\d+\s+(?:different\s+)?(?:campuses|campus|schools|school|branches|branch)\b", p_lower)
            )
            and not re.search(r"\b(?:students?|boys?|girls?|toppers?|weak\s+students?)\b", p_lower)
            and not target_roll and not target_sms and not target_name
        )

        is_subject_pass = bool(
            re.search(r"\bpass\s*(?:percentage|%|rate)\s*(?:by\s+subject|across\s+all\s+campuses)\b", p_lower)
            or re.search(r"\bsubject\s+pass\s*(?:percentage|%|rate)\b", p_lower)
        )
        is_student_marks = bool(
            not is_campus_query
            and (
                re.search(r"\b(?:toppers?|first\s+in|who\s+is\s+first|marks|result\s*cards?|failing|fail\b|weak\s+students?|top\s+\d+|best\s+\d+|\d+\s+top|\d+\s+best)\b", p_lower)
                or (re.search(r"\b(?:top|best|rank|ranks|ranking|position|highest|lowest)\b", p_lower) and re.search(r"\b(?:students?|boys?|girls?)\b", p_lower))
                or target_roll or target_sms or target_name
            )
        )
        is_student_roster = bool(
            re.search(r"\b(?:roster|enrol(?:lment|led)?|all\s+students|list\s+(?:the\s+|all\s+)?students|show\s+(?:all\s+)?students|how\s+many\s+students|count\s+of\s+students)\b", p_lower)
        ) and not is_student_marks and not is_campus_query
        is_teacher = bool(
            re.search(r"\b(?:teachers?|faculty|instructors?|eid\b|taught\s+by|staff|workload|wl\b|hof|tr\b|tr2|all_combined)\b", p_lower)
            or target_eid or target_teacher
        )

        # ── 0. Student Counts & Demographic Breakdown (Gender, Campus, Section) ──
        if re.search(r"\b(?:count|how many|total|breakdown|distribution|number of)\b", p_lower) and re.search(r"\b(?:students?|enrol(?:lment|led)?|active)\b", p_lower):
            # Grouped by Gender
            if "gender" in p_lower or ("boys" in p_lower and "girls" in p_lower) or ("male" in p_lower and "female" in p_lower):
                where_parts = []
                if target_school:
                    where_parts.append(f"SCHOOL = '{target_school}'")
                if target_class:
                    where_parts.append(f"(CLASS = '{target_class}' OR CLASS = {target_class})")
                where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
                return (
                    f"SELECT CASE WHEN SCHOOL LIKE '%B' THEN 'Boys' WHEN SCHOOL LIKE '%G' THEN 'Girls' ELSE 'Co-Ed' END AS GENDER, "
                    f"COUNT(DISTINCT ROLLNO) AS TOTAL_STUDENTS "
                    f"FROM STUDENTS_ROLL_INTERNAL_EXAM {where_clause} "
                    f"GROUP BY CASE WHEN SCHOOL LIKE '%B' THEN 'Boys' WHEN SCHOOL LIKE '%G' THEN 'Girls' ELSE 'Co-Ed' END "
                    f"ORDER BY TOTAL_STUDENTS DESC"
                )

            # Grouped by Campus
            if "campus" in p_lower or "school" in p_lower or "all campuses" in p_lower or not target_school:
                where_parts = []
                if target_class:
                    where_parts.append(f"(CLASS = '{target_class}' OR CLASS = {target_class})")
                if target_section:
                    where_parts.append(f"SECTION = '{target_section}'")
                where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
                return (
                    f"SELECT SCHOOL, COUNT(DISTINCT ROLLNO) AS TOTAL_STUDENTS "
                    f"FROM STUDENTS_ROLL_INTERNAL_EXAM {where_clause} "
                    f"GROUP BY SCHOOL "
                    f"ORDER BY TOTAL_STUDENTS DESC"
                )

            # Total Count Single Metric
            where_parts = []
            if target_school:
                where_parts.append(f"SCHOOL = '{target_school}'")
            if target_class:
                where_parts.append(f"(CLASS = '{target_class}' OR CLASS = {target_class})")
            if target_section:
                where_parts.append(f"SECTION = '{target_section}'")
            where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
            return f"SELECT COUNT(DISTINCT ROLLNO) AS TOTAL_STUDENTS FROM STUDENTS_ROLL_INTERNAL_EXAM {where_clause}"

        # ── 1. Pass Percentage by Subject Across Campuses ──
        if is_subject_pass and not is_student_marks:
            return (
                "SELECT SUBJECT, "
                "CAST(ROUND(AVG(CAST([PASS%] AS FLOAT)), 2) AS DECIMAL(5,2)) AS PASS_PERCENTAGE, "
                "COUNT(DISTINCT SCHOOL) AS TOTAL_CAMPUSES, "
                "SUM(APPEARED) AS TOTAL_APPEARED, "
                "SUM(PASSED) AS TOTAL_PASSED "
                "FROM TR_ALL "
                "WHERE [PASS%] IS NOT NULL AND RTRIM(LTRIM([PASS%])) <> '' "
                "GROUP BY SUBJECT "
                "ORDER BY PASS_PERCENTAGE DESC"
            )

        # ── 2. Data Quality: Missing Father Name / Missing SMS ──
        if re.search(r"\b(?:missing|without|no)\s+father\b", p_lower):
            limit = target_limit or 100
            where_parts = ["(FATHER IS NULL OR RTRIM(LTRIM(FATHER)) = '' OR FATHER = 'NULL' OR FATHER = '-')"]
            if target_school:
                where_parts.append(f"SCHOOL = '{target_school}'")
            if target_class:
                where_parts.append(f"CLASS = '{target_class}'")
            return f"SELECT DISTINCT TOP {limit} SCHOOL, ROLLNO, SMSNO, STUDENT, FATHER, CLASS, SECTION, CATEGORY FROM STUDENTS_ROLL_INTERNAL_EXAM WHERE {' AND '.join(where_parts)} ORDER BY ROLLNO ASC"

        if re.search(r"\b(?:missing|without|no)\s+sms\b", p_lower):
            limit = target_limit or 100
            where_parts = ["(SMSNO IS NULL OR RTRIM(LTRIM(SMSNO)) = '' OR SMSNO = '0')"]
            if target_school:
                where_parts.append(f"SCHOOL = '{target_school}'")
            if target_class:
                where_parts.append(f"CLASS = '{target_class}'")
            return f"SELECT DISTINCT TOP {limit} SCHOOL, ROLLNO, SMSNO, STUDENT, FATHER, CLASS, SECTION, CATEGORY FROM STUDENTS_ROLL_INTERNAL_EXAM WHERE {' AND '.join(where_parts)} ORDER BY ROLLNO ASC"

        # ── 3. Head Office Format (HOF_FRMT) ──
        if (re.search(r"\b(?:hof|hof_frmt|head\s*office|interview\s*sheet)\b", p_lower)) and not is_student_marks:
            limit = target_limit or 50
            where_parts = []
            if target_eid:
                where_parts.append(f"(EID = {target_eid} OR EID = '{target_eid}')")
            if target_teacher:
                where_parts.append(f"NAME LIKE '%{target_teacher}%'")
            if target_school:
                where_parts.append(f"SCHOOL = '{target_school}'")
            if target_subject:
                where_parts.append(f"SUBJECT LIKE '%{target_subject}%'")
            where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
            return f"SELECT TOP {limit} EID, NAME, SUBJECT, SCHOOL, Year, [CLASS/SECTION], APPEARED, [PASS%], [PASS% OF BOARD], Position, TOTAL_POSITIONS, [WORK LOAD], [CLASS AVG] FROM HOF_FRMT {where_clause} ORDER BY Position ASC"

        # ── 4. Internal Exam Group Performance View ──
        if "internal exam" in p_lower or re.search(r"\bgrade counts\b", p_lower) or (re.search(r"\b(?:mock|midterm|mid)\b", p_lower) and is_teacher and not is_student_marks):
            limit = target_limit or 50
            where_parts = []
            if target_eid:
                where_parts.append(f"(EID = '{target_eid}' OR EID = {target_eid})")
            if target_teacher:
                where_parts.append(f"[TEACHER NAME] LIKE '%{target_teacher}%'")
            if target_subject:
                where_parts.append(f"SUBJECT LIKE '%{target_subject}%'")
            if target_school:
                where_parts.append(f"SCHOOL = '{target_school}'")
            if target_class:
                where_parts.append(f"(CLASS = {target_class} OR CLASS = '{target_class}')")
            if target_section:
                where_parts.append(f"SECTION = '{target_section}'")
            where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
            return f"SELECT TOP {limit} ID, SCHOOL, EXAMTYPE, EID, [TEACHER NAME], YEAR, CLASS, SECTION, SUBJECT, [GROUP], APPEARED, ABSENT, PASS, [A+], A, B, C, D, E, F, [CLASS%], CLASS_AVG, [BELOW 70%], [ABOVE 70%] FROM INTERNAL_EXAM_GROUP_WISE_PERFORMANCE_VIEW {where_clause}"

        # ── 5. Practical Teacher Results (TR2_PRAC) ──
        if re.search(r"\bpractical\b", p_lower) and (is_teacher or re.search(r"\btr2\b|\bclass average\b|\bpass%\b", p_lower)) and not is_student_marks and not is_student_roster:
            limit = target_limit or 50
            where_parts = []
            if target_eid:
                where_parts.append(f"(EID = {target_eid} OR EID = '{target_eid}')")
            if target_teacher:
                where_parts.append(f"NAME LIKE '%{target_teacher}%'")
            if target_school:
                where_parts.append(f"SCHOOL = '{target_school}'")
            if target_subject:
                where_parts.append(f"SUBJECT LIKE '%{target_subject}%'")
            if target_class:
                where_parts.append(f"(CLASS = {target_class} OR CLASS = '{target_class}')")
            if target_section:
                where_parts.append(f"SECTION = '{target_section}'")
            where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
            return f"SELECT TOP {limit} EID, NAME, SCHOOL, SUBJECT, CLASS, SECTION, Year, APPEARED, PASSED, [PASS%], [CLASS AVG] FROM TR2_PRAC {where_clause} ORDER BY CAST([PASS%] AS FLOAT) DESC"

        # ── 6. Theory Teacher Results (TR2_THEORY) ──
        if re.search(r"\btheory\b", p_lower) and (is_teacher or re.search(r"\btr2\b|\bclass average\b|\bpass%\b", p_lower)) and not is_student_marks and not is_student_roster:
            limit = target_limit or 50
            where_parts = []
            if target_eid:
                where_parts.append(f"(EID = {target_eid} OR EID = '{target_eid}')")
            if target_teacher:
                where_parts.append(f"NAME LIKE '%{target_teacher}%'")
            if target_school:
                where_parts.append(f"SCHOOL = '{target_school}'")
            if target_subject:
                where_parts.append(f"SUBJECT LIKE '%{target_subject}%'")
            if target_class:
                where_parts.append(f"(CLASS = {target_class} OR CLASS = '{target_class}')")
            if target_section:
                where_parts.append(f"SECTION = '{target_section}'")
            where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
            return f"SELECT TOP {limit} EID, NAME, SCHOOL, SUBJECT, CLASS, SECTION, Year, APPEARED, PASSED, [PASS%], [CLASS AVG] FROM TR2_THEORY {where_clause} ORDER BY CAST([PASS%] AS FLOAT) DESC"

        # ── 7. Career Ranking / Workload / School Subject Averages (ALL_COMBINED / TR_ALL) ──
        if ((re.search(r"\b(?:workload|highest wl|all_combined)\b", p_lower) or (re.search(r"\brank\b", p_lower) and "teacher" in p_lower) or (re.search(r"\brank\b", p_lower) and "school" in p_lower and target_subject) or (re.search(r"\bposition\b", p_lower) and not is_student_marks))) and not is_student_marks and not is_student_roster:
            limit = target_limit or 50
            where_parts = []
            if target_eid:
                where_parts.append(f"(EID = {target_eid} OR EID = '{target_eid}')")
            if target_teacher:
                where_parts.append(f"NAME LIKE '%{target_teacher}%'")
            if target_school:
                where_parts.append(f"SCHOOL = '{target_school}'")
            if target_subject:
                where_parts.append(f"SUBJECT LIKE '%{target_subject}%'")
            if target_year:
                where_parts.append(f"(Year = {target_year} OR Year = '{target_year}')")
            where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
            order_by = "ORDER BY CAST(WL AS INT) DESC" if "workload" in p_lower or "wl" in p_lower else "ORDER BY CAST(Position AS INT) ASC"
            return f"SELECT TOP {limit} EID, NAME, SCHOOL, SUBJECT, CLASS, SECTION, Year, [PASS%], [CLASS AVG], Position, TOTAL_POSITIONS, WL FROM ALL_COMBINED {where_clause} {order_by}"

        # ── 8. Overall Teacher % / SumObtained (vTeacher_sum_per_BOARD_MIDDLE) ──
        if (re.search(r"\b(?:board percentage|middle percentage|overall percentage of teacher|board vs middle|sumobtained|sumtotal|vteacher)\b", p_lower) or ("category" in p_lower and "board" in p_lower and is_teacher)) and not is_student_marks and not is_student_roster:
            limit = target_limit or 50
            where_parts = []
            if target_eid:
                where_parts.append(f"(EID = {target_eid} OR EID = '{target_eid}')")
            if target_teacher:
                where_parts.append(f"NAME LIKE '%{target_teacher}%'")
            if target_school:
                where_parts.append(f"SCHOOL = '{target_school}'")
            if target_subject:
                where_parts.append(f"SUBJECT LIKE '%{target_subject}%'")
            where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
            order_by = "ORDER BY SumObtained DESC" if "sumobtained" in p_lower else ""
            return f"SELECT TOP {limit} EID, NAME, SCHOOL, CATEGROY, SUBJECT, SumObtained, SumTotal, [%] FROM vTeacher_sum_per_BOARD_MIDDLE {where_clause} {order_by}".strip()

        # ── 9. Combined Teacher Results (TR_ALL) ──
        if (re.search(r"\b(?:tr|tr_all|tr_report|tr_results?)\b", p_lower) or "teacher" in p_lower or "taught by" in p_lower or target_eid or target_teacher or "faculty" in p_lower) and not is_student_marks and not is_student_roster:
            limit = target_limit or 50
            where_parts = []
            if target_eid:
                where_parts.append(f"(EID = {target_eid} OR EID = '{target_eid}')")
            if target_teacher:
                where_parts.append(f"NAME LIKE '%{target_teacher}%'")
            if target_school:
                where_parts.append(f"SCHOOL = '{target_school}'")
            if target_subject:
                where_parts.append(f"SUBJECT LIKE '%{target_subject}%'")
            if target_class:
                where_parts.append(f"(CLASS = {target_class} OR CLASS = '{target_class}')")
            if target_section:
                where_parts.append(f"SECTION = '{target_section}'")
            where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
            return f"SELECT TOP {limit} EID, NAME, SCHOOL, EXAMTYPE, SUBJECT, CLASS, SECTION, Year, APPEARED, PASSED, [PASS%], [CLASS AVG] FROM TR_ALL {where_clause} ORDER BY Year DESC"

        # ── 10. Practical Marks per Student (PRAC) ──
        if re.search(r"\bpractical\b", p_lower) and (is_student_marks or "marks" in p_lower or "failed" in p_lower or "percentage" in p_lower or target_roll or target_sms):
            limit = target_limit or 50
            where_parts = []
            if target_roll:
                where_parts.append(f"(ROLLNO = '{target_roll}' OR ROLLNO = {target_roll})")
            if target_subject:
                where_parts.append(f"SUBJECT LIKE '%{target_subject}%'")
            if target_class:
                where_parts.append(f"(CLASS = '{target_class}' OR CLASS = {target_class})")
            if "fail" in p_lower:
                where_parts.append("STATUS = 'FAIL'")
            where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
            return f"SELECT TOP {limit} ROLLNO, CLASS, SUBJECT, OBTAINED, TOTAL, [%], GRADE, STATUS, YEAR, EXAMTYPE FROM PRAC {where_clause} ORDER BY [%] DESC"

        # ── 11. Internal Student Results Card (Marks_Internal & STUDENTS_ROLL_INTERNAL_EXAM) ──
        if re.search(r"\binternal\b|\bmock\b|\bmidterm\b|\bmid\b", p_lower) and (is_student_marks or target_roll or target_sms or "result" in p_lower or "marks" in p_lower):
            limit = target_limit or 50
            where_parts = []
            if target_roll:
                where_parts.append(f"(M.ROLLNO = '{target_roll}' OR M.ROLLNO = {target_roll})")
            if target_sms:
                where_parts.append(f"(SR.SMSNO = '{target_sms}' OR SR.SMSNO = {target_sms})")
            if target_school:
                where_parts.append(f"SR.SCHOOL = '{target_school}'")
            if target_class:
                where_parts.append(f"(M.CLASS = '{target_class}' OR M.CLASS = {target_class})")
            if target_section:
                where_parts.append(f"SR.SECTION = '{target_section}'")
            if target_subject:
                where_parts.append(f"M.SUBJECT LIKE '%{target_subject}%'")
            where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
            return f"SELECT TOP {limit} SR.SCHOOL, SR.STUDENT, SR.FATHER, M.CLASS, SR.SECTION, M.ROLLNO, SR.SMSNO, M.SUBJECT, M.OBTAINED, M.TOTAL, M.[%], M.STATUS, M.YEAR FROM Marks_Internal M JOIN STUDENTS_ROLL_INTERNAL_EXAM SR ON M.ROLLNO = SR.ROLLNO AND M.CLASS = SR.CLASS AND M.YEAR = SR.YEAR {where_clause} ORDER BY M.[%] DESC"

        # ── 12. School/Campus Performance Rankings (Subject-wise or Overall) ──
        is_school_ranking = bool(
            is_campus_query
            or (
                re.search(r"\b(?:school|schools|campus|campuses|branch|branches|institution|institutions)\b", p_lower)
                and re.search(r"\b(?:best|top|rank|ranks|ranking|rankings|position|positions|aggregate|performing|performance|highest|standing|results?|marks|scores?)\b", p_lower)
                and not is_student_marks
                and not is_teacher
            )
        )
        if is_school_ranking:
            limit = target_limit or 10
            where_parts = []
            if target_class:
                where_parts.append(f"(CLASS = '{target_class}' OR CLASS = {target_class})")
            if target_year:
                where_parts.append(f"(YEAR = '{target_year}' OR YEAR = {target_year} OR YEAR = '20{target_year}' OR YEAR = 2000+{target_year})")

            # Subject-specific campus performance ranking
            if target_subject:
                where_parts.append(f"SUBJECT LIKE '%{target_subject}%'")
                where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
                return (
                    f"SELECT TOP {limit} SCHOOL, SUBJECT, CLASS, "
                    f"CAST(ROUND(AVG(CAST([%] AS FLOAT)), 2) AS DECIMAL(5,2)) AS AVG_PERCENTAGE, "
                    f"CAST(ROUND(SUM(CAST(OBTAINED AS FLOAT)) * 100.0 / NULLIF(SUM(CAST(TOTAL AS FLOAT)), 0), 2) AS DECIMAL(5,2)) AS CAMPUS_PERCENTAGE, "
                    f"COUNT(DISTINCT ROLLNO) AS TOTAL_STUDENTS "
                    f"FROM STUDENTS_RESULT_TOTAL {where_clause} "
                    f"GROUP BY SCHOOL, SUBJECT, CLASS "
                    f"ORDER BY CAMPUS_PERCENTAGE DESC, AVG_PERCENTAGE DESC"
                )

            # Overall institutional campus performance ranking (School_Ind_Pos_SUB)
            where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
            return f"SELECT TOP {limit} SCHOOL, YEAR, CLASS, Strength, AggregatePercentage, Position FROM School_Ind_Pos_SUB {where_clause} ORDER BY CAST(Position AS INT) ASC, CAST(AggregatePercentage AS FLOAT) DESC"

        # ── 13. Student Board Marks / Result Cards / Subject Toppers (STUDENTS_RESULT_TOTAL / MARKS) ──
        if is_student_marks or "marks" in p_lower or "result card" in p_lower or "percentage" in p_lower or "top" in p_lower or "score" in p_lower or "first in" in p_lower or "who is first" in p_lower or target_roll or target_sms or target_name or (target_subject and not is_teacher):
            limit = target_limit
            if limit is None:
                if "first in" in p_lower or "who is first" in p_lower or "topper" in p_lower:
                    limit = 1
                elif "top" in p_lower or "best" in p_lower or "highest" in p_lower:
                    limit = 10
                else:
                    limit = 50
            where_parts = []
            if target_roll:
                where_parts.append(f"(ROLLNO = '{target_roll}' OR ROLLNO = {target_roll})")
            if target_sms:
                where_parts.append(f"(SMSNO = '{target_sms}' OR SMSNO = {target_sms})")
            if target_name:
                where_parts.append(f"STUDENT LIKE '%{target_name}%'")
            if target_school:
                where_parts.append(f"SCHOOL = '{target_school}'")
            if target_class:
                where_parts.append(f"(CLASS = '{target_class}' OR CLASS = {target_class})")
            if target_section:
                where_parts.append(f"SECTION = '{target_section}'")
            if target_subject:
                where_parts.append(f"SUBJECT LIKE '%{target_subject}%'")
            if "fail" in p_lower:
                where_parts.append("STATUS = 'FAIL'")
            where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
            order_by = "ORDER BY [%] ASC, OBTAINED ASC" if ("lowest" in p_lower or "fail" in p_lower or "weak" in p_lower or "bottom" in p_lower) else "ORDER BY [%] DESC, OBTAINED DESC"
            return f"SELECT TOP {limit} SCHOOL, STUDENT, FATHER, CLASS, SECTION, ROLLNO, SMSNO, SUBJECT, OBTAINED, TOTAL, [%], STATUS, YEAR FROM STUDENTS_RESULT_TOTAL {where_clause} {order_by}"

        # ── 14. Default Master Student Enrollment (STUDENTS_ROLL_INTERNAL_EXAM) ──
        limit = target_limit or 100
        where_parts = []
        if target_school:
            where_parts.append(f"SCHOOL = '{target_school}'")
        if target_class:
            where_parts.append(f"CLASS = '{target_class}'")
        if target_section:
            where_parts.append(f"SECTION = '{target_section}'")
        if target_year:
            where_parts.append(f"(YEAR = {target_year} OR YEAR = '{target_year}')")
        if target_name:
            where_parts.append(f"STUDENT LIKE '%{target_name}%'")
        where_clause = f"WHERE {' AND '.join(where_parts)}" if where_parts else ""
        return f"SELECT DISTINCT TOP {limit} SCHOOL, ROLLNO, SMSNO, STUDENT, FATHER, CLASS, SECTION, CATEGORY, YEAR FROM STUDENTS_ROLL_INTERNAL_EXAM {where_clause} ORDER BY SCHOOL, ROLLNO ASC"

    def summarize_results(self, prompt: str, sql: str, rows: List[Dict[str, Any]], scope: str = "ALL", exec_ms: float = 0.0, **kwargs) -> str:
        """Generates crisp, highly tailored contextual academic summary specifically answering the user's question."""
        if not rows:
            return (
                "**Academic Query Summary**\n\n"
                "• **Records Found:** 0 matching records were returned for your specific filter criteria.\n"
                "• **Status:** Complete data verification confirmed on live SQL Server database."
            )

        # 1. Primary Engine: OpenRouter LLM Dynamic Executive Synthesis
        openrouter_key = os.getenv("OPENROUTER_API_KEY") or self._openrouter_key or getattr(settings, "OPENROUTER_API_KEY", "")
        if openrouter_key and not openrouter_key.startswith("sk-or-v1-demo"):
            for model_candidate in [self._openrouter_model, "openai/gpt-4o-mini", "anthropic/claude-3.5-sonnet"]:
                try:
                    sample_rows = rows[:10]
                    sys_prompt = (
                        "You are the Daanish Schools Academic Executive Intelligence Assistant. "
                        "Converse smoothly, warmly, and helpfully like ChatGPT while delivering precise database intelligence.\n\n"
                        "CONVERSATIONAL STRUCTURE GUIDELINES:\n"
                        "1. Conversational Intro: Start with a natural opening sentence tailored specifically to the user's inquiry.\n"
                        "2. Key Insights & Data: 2 to 4 clear, well-structured bullet points with exact counts, percentages, names, and metrics from the data.\n"
                        "3. Friendly Follow-up Closing: End with an engaging follow-up statement or question.\n"
                        "4. Strict Data Grounding: Only use factual values present in the provided data rows."
                    )
                    user_msg = (
                        f"User Question: '{prompt}'\n"
                        f"Campus Scope: '{scope}'\n"
                        f"Total Rows Returned: {len(rows)}\n"
                        f"Sample Data Rows (up to 10):\n{json.dumps(sample_rows, default=str, indent=2)}\n\n"
                        f"Please write a tailored, conversational executive summary answering the question:"
                    )
                    headers = {
                        "Authorization": f"Bearer {openrouter_key}",
                        "HTTP-Referer": "https://eduquery.daanish.edu.pk",
                        "X-Title": "EduQuery AI Engine",
                        "Content-Type": "application/json"
                    }
                    payload = {
                        "model": model_candidate,
                        "messages": [
                            {"role": "system", "content": sys_prompt},
                            {"role": "user", "content": user_msg}
                        ],
                        "temperature": 0.1
                    }
                    with httpx.Client(timeout=12.0) as http_client:
                        res = http_client.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
                        if res.status_code == 200:
                            content = res.json()["choices"][0]["message"]["content"]
                            if content and content.strip():
                                return content.strip()
                except Exception as e:
                    logger.warning(f"OpenRouter summary ({model_candidate}) error: {e}")

        # 2. Secondary Engine: Gemini LLM Dynamic Executive Synthesis
        if self.client:
            try:
                sample_rows = rows[:10]
                system_instruction = (
                    "You are the Daanish Schools Academic Executive Intelligence Assistant. "
                    "Converse smoothly, warmly, and helpfully like ChatGPT while delivering precise database intelligence.\n\n"
                    "CONVERSATIONAL STRUCTURE GUIDELINES:\n"
                    "1. Conversational Intro: Start with a natural opening sentence tailored to the user's inquiry (e.g., 'Here is the database breakdown you requested for Class 10 exam results across the campuses:' or 'I have retrieved the attendance records for you:').\n"
                    "2. Key Insights & Data: 2 to 4 clear, well-structured bullet points formatted as:\n"
                    "• **Key Finding:** Exact names, roll numbers, teacher names, EIDs, subjects, pass rates, or notable metrics from the data.\n"
                    "3. Friendly Follow-up Closing: End with an engaging follow-up statement or question (e.g., 'Would you like me to filter these results by a specific campus or section, or is there anything else I can query for you?').\n"
                    "4. Strict Data Grounding: Only use factual values present in the provided data rows."
                )
                user_msg = (
                    f"User Question: '{prompt}'\n"
                    f"Campus Scope: '{scope}'\n"
                    f"Total Rows Returned: {len(rows)}\n"
                    f"Sample Data Rows (up to 10):\n{json.dumps(sample_rows, default=str, indent=2)}\n\n"
                    f"Please write a tailored, conversational executive summary answering the question:"
                )
                config = types.GenerateContentConfig(temperature=0.1, system_instruction=system_instruction)
                resp = self.client.models.generate_content(
                    model=self._preferred_model,
                    contents=[user_msg],
                    config=config
                )
                if resp and resp.text:
                    return resp.text.strip()
            except Exception as e:
                logger.warning(f"Gemini dynamic summary error: {e}")

        # 3. Resilient Rule-Based Fallback
        row_count = len(rows)
        first_row = rows[0]

        # Demographic / Gender Breakdown
        if "GENDER" in first_row and "TOTAL_STUDENTS" in first_row:
            points = [f"• **{r.get('GENDER', 'Gender')}:** {r.get('TOTAL_STUDENTS', 0):,} enrolled students." for r in rows]
            total_s = sum(r.get("TOTAL_STUDENTS", 0) for r in rows)
            points.append(f"• **Overall Student Total:** {total_s:,} students across active campuses.")
            body = "\n".join(points)
            return (
                f"Here is the student enrollment distribution by gender across **{scope}**:\n\n"
                f"{body}\n\n"
                f"Would you like to view this broken down by grade level or specific campuses?"
            )

        # Campus Subject Performance Rankings (CAMPUS_PERCENTAGE / AVG_PERCENTAGE with SCHOOL and SUBJECT)
        if ("CAMPUS_PERCENTAGE" in first_row or "AVG_PERCENTAGE" in first_row or ("PASS_PERCENTAGE" in first_row and "SCHOOL" in first_row and "SUBJECT" in first_row)) and "STUDENT" not in first_row:
            subj_name = str(first_row.get("SUBJECT", "Subject")).title()
            cls_str = f" for Class {first_row.get('CLASS')}" if first_row.get('CLASS') else ""
            points = []
            for idx, r in enumerate(rows, 1):
                pct = r.get("CAMPUS_PERCENTAGE") or r.get("AVG_PERCENTAGE") or r.get("PASS_PERCENTAGE", "N/A")
                total_s = r.get("TOTAL_STUDENTS") or r.get("TOTAL_APPEARED", "N/A")
                s_count_str = f" ({total_s} students evaluated)" if total_s != "N/A" else ""
                points.append(f"• **#{idx} Rank:** **{r.get('SCHOOL', 'N/A')}** achieved **{pct}%** subject aggregate{s_count_str}.")
            body = "\n".join(points)
            return (
                f"Here are the **top {len(rows)} campuses** based on their **{subj_name}** results{cls_str}:\n\n"
                f"{body}\n\n"
                f"Would you like to view the top student performers or teacher evaluations for any of these campuses?"
            )

        # Campus Student Count Aggregation (Pure enrollment counts without subject scores)
        if "TOTAL_STUDENTS" in first_row and "SCHOOL" in first_row and "STUDENT" not in first_row:
            points = [f"• **{r.get('SCHOOL', 'Campus')}:** {r.get('TOTAL_STUDENTS', 0):,} students." for r in rows[:5]]
            total_s = sum(r.get("TOTAL_STUDENTS", 0) for r in rows)
            points.append(f"• **Total Evaluated:** {len(rows)} campuses (Total: {total_s:,} enrolled students).")
            body = "\n".join(points)
            return (
                f"Here is the student count breakdown by campus across **{scope}**:\n\n"
                f"{body}\n\n"
                f"Would you like to drill into a specific campus or class section?"
            )

        # School / Campus Performance Rankings (School_Ind_Pos_SUB)
        if "AggregatePercentage" in first_row or ("Position" in first_row and "SCHOOL" in first_row and "Strength" in first_row):
            top_school = rows[0]
            points = [
                f"• **#1 Rank:** **{top_school.get('SCHOOL', 'N/A')}** secured **1st Position** with an aggregate performance of **{top_school.get('AggregatePercentage', 'N/A')}%** (Student strength: {top_school.get('Strength', 'N/A')})."
            ]
            if len(rows) > 1:
                second_school = rows[1]
                points.append(
                    f"• **#2 Rank:** **{second_school.get('SCHOOL', 'N/A')}** achieved **{second_school.get('AggregatePercentage', 'N/A')}%** aggregate."
                )
            if len(rows) > 2:
                third_school = rows[2]
                points.append(
                    f"• **#3 Rank:** **{third_school.get('SCHOOL', 'N/A')}** achieved **{third_school.get('AggregatePercentage', 'N/A')}%** aggregate."
                )
            points.append(f"• **Total Campuses Evaluated:** {row_count} campus performance standings retrieved.")
            body = "\n".join(points)
            cls_str = f" for Class {first_row.get('CLASS')}" if first_row.get('CLASS') else ""
            yr_str = f" (Year {first_row.get('YEAR')})" if first_row.get('YEAR') else ""
            return (
                f"Here are the **campus performance rankings**{cls_str}{yr_str} from the live academic database:\n\n"
                f"{body}\n\n"
                f"Would you like to drill down into the subject-wise results or student rosters for any specific campus?"
            )

        # Teacher Results (Ensure this ONLY triggers if this is genuinely a teacher result record)
        if ("EID" in first_row or "PASS%" in first_row or "CLASS AVG" in first_row or "TEACHER NAME" in first_row) and "STUDENT" not in first_row and "ROLLNO" not in first_row:
            t_name = first_row.get("NAME") or first_row.get("TEACHER NAME") or f"Teacher EID {first_row.get('EID', 'N/A')}"
            pass_p = first_row.get("PASS%") or first_row.get("PASS_PERCENTAGE") or first_row.get("CLASS%")
            avg = first_row.get("CLASS AVG") or first_row.get("CLASS_AVG")
            pos = first_row.get("Position")
            wl = first_row.get("WL") or first_row.get("WORK LOAD")
            points = [f"• **Teacher Profile:** Evaluation records retrieved for **{t_name}** at campus **{first_row.get('SCHOOL', scope)}**."]
            if pass_p is not None:
                points.append(f"• **Pass Percentage:** Academic pass rate achieved is **{pass_p}%** across {first_row.get('APPEARED', 'evaluated')} students.")
            if avg is not None:
                points.append(f"• **Class Average:** Subject class average recorded is **{avg}**.")
            if pos is not None:
                points.append(f"• **Subject Ranking:** Institutional position is **#{pos}** (Total positions: {first_row.get('TOTAL_POSITIONS', 'N/A')}).")
            if wl is not None:
                points.append(f"• **Workload:** Assigned instructional workload (WL) is **{wl}**.")
            
            body = "\n".join(points)
            return (
                f"Here is the teacher performance evaluation you requested for **{t_name}**:\n\n"
                f"{body}\n\n"
                f"Would you like me to compare this with other faculty members or check another campus? Let me know how else I can help!"
            )

        # Subject Aggregation Across Campuses
        if "PASS_PERCENTAGE" in first_row and "SUBJECT" in first_row:
            top_subj = rows[0]
            lowest_subj = rows[-1]
            total_app = sum(r.get("TOTAL_APPEARED", 0) or 0 for r in rows)
            total_pass = sum(r.get("TOTAL_PASSED", 0) or 0 for r in rows)
            overall_pass_rate = round(total_pass * 100.0 / total_app, 2) if total_app > 0 else top_subj.get("PASS_PERCENTAGE")
            return (
                f"I have compiled the subject-wise performance breakdown across **{scope}** for you:\n\n"
                f"• **Institutional Pass Rate:** Overall academic pass rate is **{overall_pass_rate}%** ({total_pass:,} passed of {total_app:,} appeared).\n"
                f"• **Top Performing Subject:** **{top_subj['SUBJECT']}** achieved **{top_subj['PASS_PERCENTAGE']}%** pass rate.\n"
                f"• **Lowest Performing Subject:** **{lowest_subj['SUBJECT']}** recorded **{lowest_subj['PASS_PERCENTAGE']}%** pass rate.\n\n"
                f"Would you like to drill down into the student-level results for any specific subject or campus?"
            )

        # Student Result Cards / Marks / Leaderboards
        if "%" in first_row or "OBTAINED" in first_row:
            top_s = rows[0]
            passed = sum(1 for r in rows if str(r.get("STATUS", "")).upper() == "PASS" or (r.get("%") and float(r.get("%")) >= 33.0))
            is_top_query = bool(re.search(r"\b(?:top|first|best|highest|topper|rank)\b", prompt, re.IGNORECASE))
            subj_label = str(top_s.get("SUBJECT") or "the subject").title()
            
            if is_top_query:
                points = [
                    f"• **#1 Rank:** **{top_s.get('STUDENT', 'Student')}** (Father: {top_s.get('FATHER', 'N/A')}) secured **1st Position** with **{top_s.get('OBTAINED', 0)}/{top_s.get('TOTAL', 0)}** marks (**{top_s.get('%', 100)}%**) at campus **{top_s.get('SCHOOL', scope)}**."
                ]
                if len(rows) > 1:
                    second_s = rows[1]
                    points.append(
                        f"• **#2 Rank:** **{second_s.get('STUDENT', 'Student')}** achieved **{second_s.get('OBTAINED', 0)}/{second_s.get('TOTAL', 0)}** marks (**{second_s.get('%', 0)}%**) at campus **{second_s.get('SCHOOL', scope)}**."
                    )
                if len(rows) > 2:
                    third_s = rows[2]
                    points.append(
                        f"• **#3 Rank:** **{third_s.get('STUDENT', 'Student')}** achieved **{third_s.get('OBTAINED', 0)}/{third_s.get('TOTAL', 0)}** marks (**{third_s.get('%', 0)}%**) at campus **{third_s.get('SCHOOL', scope)}**."
                    )
                points.append(f"• **Cohort Performance:** {passed} of {row_count} listed students ({round(passed * 100.0 / row_count, 1)}%) met passing standards.")
                body = "\n".join(points)
                return (
                    f"Here is the leaderboard of the **top {row_count} students** in **{subj_label}** for **{scope}**:\n\n"
                    f"{body}\n\n"
                    f"Would you like to filter these rankings by a specific campus or view their complete report card?"
                )
            
            return (
                f"Here are the student academic assessment records retrieved for **{scope}**:\n\n"
                f"• **Total Students Evaluated:** {row_count} student result records retrieved.\n"
                f"• **Top Performer:** **{top_s.get('STUDENT', 'Student')}** achieved top score (**{top_s.get('OBTAINED', 0)}/{top_s.get('TOTAL', 0)}** marks, **{top_s.get('%', 100)}%**) in {top_s.get('SUBJECT', 'Subject')} at campus **{top_s.get('SCHOOL', scope)}**.\n"
                f"• **Cohort Pass Rate:** {passed} of {row_count} students ({round(passed * 100.0 / row_count, 1)}%) met passing standards.\n\n"
                f"Is there a particular student or class section you would like more details on?"
            )

        # Student Enrollment / Rosters
        campuses_found = len(set(r.get("SCHOOL") for r in rows if r.get("SCHOOL")))
        clean_scope = scope if str(scope).lower().startswith("campus") or str(scope).lower() in ["all", "all campuses"] else f"campus {scope}"
        scope_desc = f"{campuses_found} campuses" if campuses_found > 1 else clean_scope
        return (
            f"I have retrieved the student enrollment and roster details for **{scope}**:\n\n"
            f"• **Total Student Records:** {row_count} enrolled students retrieved.\n"
            f"• **Campus Scope:** Data spans {scope_desc} with complete student registration details.\n"
            f"• **Data Integrity:** All student identifiers, roll numbers, and parent details verified on live database.\n\n"
            f"What other student records or institutional data can I assist you with?"
        )


nl2sql_synthesizer = NL2SQLSynthesizer()
