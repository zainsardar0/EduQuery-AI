import pytest
from services.api.app.services.nl2sql_synthesizer import nl2sql_synthesizer


def test_top_10_students_in_chemistry_class_10():
    prompt = "Top 10 students in chemistry class 10"
    sql = nl2sql_synthesizer.generate_sql(prompt)
    assert "STUDENTS_RESULT_TOTAL" in sql.upper()
    assert "TR_ALL" not in sql.upper()
    assert "TOP 10" in sql.upper()
    assert "CHEMISTRY" in sql.upper()
    assert "ORDER BY [%] DESC" in sql.upper()


def test_top_5_students_in_mathematics():
    prompt = "Top 5 students in mathematics"
    sql = nl2sql_synthesizer.generate_sql(prompt)
    assert "STUDENTS_RESULT_TOTAL" in sql.upper()
    assert "TOP 5" in sql.upper()
    assert "MATHEMATICS" in sql.upper()


def test_who_is_first_in_physics():
    prompt = "Who is first in Physics class 9"
    sql = nl2sql_synthesizer.generate_sql(prompt)
    assert "STUDENTS_RESULT_TOTAL" in sql.upper()
    assert "TOP 1" in sql.upper()
    assert "PHYSICS" in sql.upper()


def test_student_roster_queries_enrollment_table():
    prompt = "Show all students of Class 10 Section A in school ATKB for year 26"
    sql = nl2sql_synthesizer.generate_sql(prompt)
    assert "STUDENTS_ROLL_INTERNAL_EXAM" in sql.upper()
    assert "ATKB" in sql.upper()


def test_teacher_eval_query_routes_to_tr_all():
    prompt = "Show annual TR result of teacher EID 105"
    sql = nl2sql_synthesizer.generate_sql(prompt)
    assert "TR_ALL" in sql.upper()
    assert "EID = 105" in sql.upper()


def test_chemistry_teacher_with_explicit_teacher_keyword():
    prompt = "Show evaluation results for Chemistry teacher in Class 10"
    sql = nl2sql_synthesizer.generate_sql(prompt)
    assert "TR_ALL" in sql.upper() or "TR2_THEORY" in sql.upper()
    assert "CHEMISTRY" in sql.upper()


def test_summarize_results_for_top_students():
    prompt = "Top 10 students in chemistry class 10"
    sql = "SELECT TOP 10 SCHOOL, STUDENT, FATHER, CLASS, SECTION, ROLLNO, SMSNO, SUBJECT, OBTAINED, TOTAL, [%], STATUS, YEAR FROM STUDENTS_RESULT_TOTAL WHERE (CLASS = '10' OR CLASS = 10) AND SUBJECT LIKE '%CHEMISTRY%' ORDER BY [%] DESC, OBTAINED DESC"
    rows = [
        {"SCHOOL": "HSPG", "STUDENT": "ISHRAT BIBI", "FATHER": "MUHAMMAD NAZIR", "CLASS": 10.0, "SECTION": "A", "ROLLNO": 169540.0, "SMSNO": 0, "SUBJECT": "CHEMISTRY", "OBTAINED": 90.0, "TOTAL": 90.0, "%": 100.0, "STATUS": "PASS", "YEAR": 18.0},
        {"SCHOOL": "HSPG", "STUDENT": "MUNAZA ZAINAB", "FATHER": "GHULAM MURTAZA", "CLASS": 10.0, "SECTION": "A", "ROLLNO": 169531.0, "SMSNO": 0, "SUBJECT": "CHEMISTRY", "OBTAINED": 90.0, "TOTAL": 90.0, "%": 100.0, "STATUS": "PASS", "YEAR": 18.0}
    ]
    summary = nl2sql_synthesizer.summarize_results(prompt, sql, rows, scope="all campuses")
    assert "top 2 students" in summary.lower() or "leaderboard" in summary.lower()
    assert "ISHRAT BIBI" in summary
    assert "teacher performance" not in summary.lower()


def test_best_performing_campus_in_class_10_results_in_2025():
    prompt = "best performing campus in class 10th results in 2025"
    sql = nl2sql_synthesizer.generate_sql(prompt)
    assert "School_Ind_Pos_SUB" in sql or "AggregatePercentage" in sql or "Position" in sql
    assert "10" in sql
    assert "25" in sql
    assert "STUDENTS_ROLL_INTERNAL_EXAM" not in sql


def test_summarize_results_for_campus_rankings():
    prompt = "best performing campus in class 10th results in 2025"
    sql = "SELECT TOP 10 SCHOOL, YEAR, CLASS, Strength, AggregatePercentage, Position FROM School_Ind_Pos_SUB WHERE (CLASS = '10' OR CLASS = 10) ORDER BY CAST(Position AS INT) ASC"
    rows = [
        {"SCHOOL": "HSPB", "YEAR": 25, "CLASS": 10, "Strength": 120, "AggregatePercentage": 92.5, "Position": 1},
        {"SCHOOL": "MNWG", "YEAR": 25, "CLASS": 10, "Strength": 115, "AggregatePercentage": 90.8, "Position": 2}
    ]
    summary = nl2sql_synthesizer.summarize_results(prompt, sql, rows, scope="all campuses")
    assert "campus performance rankings" in summary.lower() or "#1 rank" in summary.lower()
    assert "HSPB" in summary


def test_count_active_students_grouped_by_gender():
    prompt = "Count active students across all campuses grouped by gender"
    sql = nl2sql_synthesizer.generate_sql(prompt)
    assert "GENDER" in sql.upper() or "COUNT(" in sql.upper()
    assert "STUDENTS_ROLL_INTERNAL_EXAM" in sql.upper()
    assert "GROUP BY" in sql.upper()


def test_count_students_across_all_campuses():
    prompt = "Count students across all campuses"
    sql = nl2sql_synthesizer.generate_sql(prompt)
    assert "COUNT(" in sql.upper()
    assert "SCHOOL" in sql.upper()
    assert "GROUP BY" in sql.upper()


def test_show_10_students_in_section_a():
    prompt = "Show 10 students in section A"
    sql = nl2sql_synthesizer.generate_sql(prompt, campus_code="ATKB")
    assert "TOP 10" in sql.upper()
    assert "SECTION = 'A'" in sql.upper()
    assert "ATKB" in sql.upper()


def test_top_3_campuses_physics_results():
    prompt = "list top 3 campuses on the base of their class 10th physics results"
    sql = nl2sql_synthesizer.generate_sql(prompt)
    assert "TOP 3" in sql.upper()
    assert "PHYSICS" in sql.upper()
    assert "GROUP BY" in sql.upper()
    assert "SCHOOL" in sql.upper()
    assert "STUDENT, FATHER" not in sql.upper()


def test_3_different_campuses_physics_results():
    prompt = "3 different campuses listed on the base of their class 10 physics results"
    sql = nl2sql_synthesizer.generate_sql(prompt)
    assert "TOP 3" in sql.upper()
    assert "PHYSICS" in sql.upper()
    assert "GROUP BY" in sql.upper()
    assert "SCHOOL" in sql.upper()


def test_summarize_results_for_campus_subject_rankings():
    prompt = "list top 3 campuses on the base of their class 10th physics results"
    sql = "SELECT TOP 3 SCHOOL, SUBJECT, CLASS, AVG_PERCENTAGE, CAMPUS_PERCENTAGE, TOTAL_STUDENTS FROM STUDENTS_RESULT_TOTAL GROUP BY SCHOOL, SUBJECT, CLASS"
    rows = [
        {"SCHOOL": "ATKB", "SUBJECT": "PHYSICS", "CLASS": 10, "CAMPUS_PERCENTAGE": 94.2, "AVG_PERCENTAGE": 92.0, "TOTAL_STUDENTS": 85},
        {"SCHOOL": "HSPB", "SUBJECT": "PHYSICS", "CLASS": 10, "CAMPUS_PERCENTAGE": 91.5, "AVG_PERCENTAGE": 89.4, "TOTAL_STUDENTS": 90},
        {"SCHOOL": "MNWG", "SUBJECT": "PHYSICS", "CLASS": 10, "CAMPUS_PERCENTAGE": 88.0, "AVG_PERCENTAGE": 87.1, "TOTAL_STUDENTS": 78}
    ]
    summary = nl2sql_synthesizer.summarize_results(prompt, sql, rows, scope="all campuses")
    assert "top 3 campuses" in summary.lower() or "#1 rank" in summary.lower()
    assert "ATKB" in summary
    assert "HSPB" in summary



