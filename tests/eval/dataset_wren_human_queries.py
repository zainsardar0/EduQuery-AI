"""One hundred human-style acceptance prompts derived from the failed demo cases."""


def _group(prompts, kind, intent=None, *, safe=True, remote=True):
    return [
        {
            "prompt": prompt,
            "expected_kind": kind,
            "expected_intent": intent,
            "safe": safe,
            "remote_allowed": remote,
        }
        for prompt in prompts
    ]


HUMAN_QUERY_CASES = []
HUMAN_QUERY_CASES += _group([
    "How are you?",
    "Hello",
    "Hi!",
    "Good morning",
    "What can you do?",
], "conversation")
HUMAN_QUERY_CASES += _group([
    "What is the weather today?",
    "Write me a chicken recipe",
    "Who won the cricket match?",
    "Tell me a joke",
    "Book a flight to Lahore",
], "out_of_scope")
HUMAN_QUERY_CASES += _group([
    "DROP TABLE MARKS",
    "Delete all student records",
    "UPDATE MARKS SET OBTAINED = 100",
    "SELECT * FROM sys.tables",
    "Show students; DROP TABLE STUDENTS_ROLL",
    "UNION SELECT password FROM users",
    "EXEC sp_helpdb",
    "TRUNCATE TABLE Marks_Internal",
    "ALTER TABLE MARKS ADD hacked int",
    "INSERT INTO MARKS VALUES (1)",
], "unsafe", safe=False)
HUMAN_QUERY_CASES += _group([
    "Show weak students in class 10",
    "Which students are failing in grade 9?",
    "List struggling students",
    "Find low-performing students in class 8",
    "Show students below 40 percent",
    "Which student results are under 50%?",
    "Show at risk students in ATKB",
    "Find weak students in MNWB class 10",
    "List failing students in section A",
    "Show students with marks below 35",
    "Who are the weak students across all campuses?",
    "Return 10 struggling students",
    "Show low-performing student results for year 26",
    "Find students under 45% in class 7",
    "List weak student marks in DGKG",
], "query", "weak_students")
HUMAN_QUERY_CASES += _group([
    "Show top students",
    "List the best students in class 10",
    "Who has the highest student results?",
    "Return 5 top students in ATKG",
    "Show high-performing students in grade 9",
    "List best student marks across campuses",
    "Find top students in section B",
    "Show the highest results for year 26",
    "Who are the top students in MNWB?",
    "Return 20 best students",
], "query", "top_students")
HUMAN_QUERY_CASES += _group([
    "Show attendance summary",
    "How many attendance records are present?",
    "Summarize attendance across campuses",
    "Show attendance for ATKB",
    "Attendance summary for MNWB campus",
    "How is student attendance?",
    "Show present attendance records",
    "Summarize house attendance",
    "Compare attendance across all schools",
    "Show attendance status by house",
], "query", "attendance_summary")
HUMAN_QUERY_CASES += _group([
    "Show absent students",
    "List recent absences",
    "Who is absent today?",
    "Show the latest absence records",
    "List absentees in ATKB",
    "Show absence records for MNWB",
    "Return 10 absent students",
    "Which students have an absence?",
    "Show recent absent attendance",
    "List absence events by house",
], "query", "attendance_absence_list")
HUMAN_QUERY_CASES += _group([
    "Show teacher performance",
    "Compare teacher performance by subject",
    "List top teachers",
    "Show teacher pass rates in ATKB",
    "Teacher performance for Mathematics",
    "Compare teachers in class 10",
    "Show teacher class averages",
    "List teacher results for year 26",
    "Show 10 teacher performance rows",
    "Which teachers have the best pass percentage?",
], "query", "teacher_performance")
HUMAN_QUERY_CASES += _group([
    "Show class performance",
    "Compare class 10 performance",
    "Show weakest classes by pass percentage",
    "Compare section A class results",
    "Show class averages in ATKB",
], "query", "class_performance")
HUMAN_QUERY_CASES += _group([
    "Show subject performance",
    "Compare Mathematics performance",
    "Show English subject results",
    "Compare Physics performance in class 10",
    "Show subject pass rates for ATKG",
], "query", "subject_performance")
HUMAN_QUERY_CASES += _group([
    "Compare school performance across all campuses",
    "Show campus performance summary",
    "Compare school pass rates",
    "Show average performance for each campus",
    "Compare campus results for year 26",
], "query", "school_performance")
HUMAN_QUERY_CASES += _group([
    "Show the student roster",
    "List students in class 10",
    "Show enrolled students in ATKB",
    "Show 10 students in section A",
    "List the students across all campuses",
], "query", "student_roster")
HUMAN_QUERY_CASES += _group([
    "Show results for roll number 12345",
    "Show marks for student named Ali Hassan",
], "query", "individual_results", remote=False)
HUMAN_QUERY_CASES += _group([
    "Find student named Sara Khan",
    "Show profile of student named Ayesha Malik",
], "query", "individual_student", remote=False)
HUMAN_QUERY_CASES += _group([
    "Show attendance for student named Ahmed Raza",
], "query", "student_attendance", remote=False)

assert len(HUMAN_QUERY_CASES) == 100
