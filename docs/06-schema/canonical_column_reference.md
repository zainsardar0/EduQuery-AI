# EduQuery AI — Canonical Column Reference

> Standardized column naming, synonym mapping, and data type documentation for the NLP model semantic layer.

---

## 1. Column Name Synonyms

The database uses inconsistent column names for the same concepts. This reference maps natural language terms and variant column names to their canonical meaning.

### Student Identity

| Canonical Name | Variants Found | Tables | Meaning |
|----------------|---------------|--------|---------|
| `STUDENT_NAME` | `STUDENT`, `STUDENTNAME`, `STUDENT NAME` | STUDENTS_ROLL_INTERNAL_EXAM (`STUDENT`), ALL_COMBINED (`STUDENTNAME`), ABSENT (`STUDENT NAME`) | Student's full name |
| `SMSNO` | `SMSNO`, `SMS_No` | All student tables | School Management System unique number |
| `ROLLNO` | `ROLLNO`, `BOARDROLLNO`, `Roll_No`, `Board_Roll_No` | Various | Roll number (internal or board) |
| `FATHER_NAME` | `FATHER`, `FATHER_NAME`, `Father_Name` | STUDENTS_ROLL_INTERNAL_EXAM (`FATHER`), STAFF_EMPLOYEE_CARD (`FATHER_NAME`) | Father's name |
| `CATEGORY` | `CATEGORY`, `CATEGROY` | Most tables (`CATEGORY`), STUDENTS_ROLL (`CATEGROY` — typo) | Student fee category (B=Boarder, S=Scholar, DS=Day Scholar) |

### Academic Structure

| Canonical Name | Variants Found | Tables | Meaning |
|----------------|---------------|--------|---------|
| `SCHOOL` | `SCHOOL`, `school`, `School`, `SchoolName` | Nearly all tables | Campus code (e.g., ATKB, MNWB, TNSG) |
| `CLASS` | `CLASS`, `Class`, `ClassName` | All tables | Class/grade level (1-12) |
| `SECTION` | `SECTION`, `Section` | Most tables | Section within a class (A, B, C) |
| `GROUP` | `GROUP`, `Class_Group` | Student and marks tables | Academic stream (PRE-MEDICAL, GENERAL SCIENCE, etc.) |
| `YEAR` | `YEAR`, `Year`, `ClassBatchYear` | All tables | Academic year (stored as 22, 23, 24, 25, 26 — two-digit format) |
| `HOUSE` | `HOUSE`, `HOUSE_NAME`, `House_Name` | Student tables, House_Management | Student house assignment |

### Exam & Assessment

| Canonical Name | Variants Found | Tables | Meaning |
|----------------|---------------|--------|---------|
| `EXAM_TYPE` | `EXAMTYPE`, `EXAM_TYPE`, `EXAM` | MARKS (`EXAMTYPE`), Marks_Internal (`EXAMTYPE`), Exam_Schedule (`EXAM_TYPE`), STUDENTS_ROLL_INTERNAL_EXAM (`EXAM`) | Type of exam (MID_DEC, ANNUAL, MOCK, etc.) |
| `SUBJECT` | `SUBJECT`, `SUBJECTNAME`, `SubjectName` | CorrectSubjects (`SUBJECT`), MARKS (`SUBJECT`), Marks_Internal (`SUBJECTNAME`), Subjects_Quiz (`SubjectName`) | Subject name |
| `MARKS` | `MARKS`, `OBTAINED` | MARKS (`OBTAINED`), Marks_Internal (`OBTAINED`) | Marks obtained by student |
| `TOTAL_MARKS` | `TOTALMARKS`, `TOTAL`, `TOTAL MARKS` | MARKS (`TOTAL`), Marks_Internal (`TOTAL`), SubjectTotals (`TOTALMARKS`), SUBJECT_GROUP_YEAR_MARKS (`TOTAL MARKS`) | Maximum marks possible |
| `PERCENTAGE` | `%`, `PERCENTAGE`, `PASS%`, `ANNUAL PASS%` | MARKS (`%`), Marks_Internal (`%`), HOF (`PERCENTAGE`), TR_ALL (`PASS%`), SUBJECT_GROUP_YEAR_MARKS (`ANNUAL PASS%`) | Percentage score |
| `GRADE` | `GRADE` | MARKS, Marks_Internal, HOF, ALL_COMBINED2_SNAPSHOT | Letter grade (A+, A, B, C, D, E, F) |
| `STATUS` | `STATUS` | MARKS, Marks_Internal, HOF | Pass/Fail status |

### Teacher Identity

| Canonical Name | Variants Found | Tables | Meaning |
|----------------|---------------|--------|---------|
| `TEACHER_NAME` | `TEACHER`, `NAME`, `TEACHER_NAME` | TEACHERS_PROFILE (`TEACHER`), TEACHERS_INTERNAL_EXAM (`NAME`), TEAHCERS (`NAME`), TR_ALL (`NAME`), HOF (`TEACHER_NAME`) | Teacher's full name |
| `EID` | `EID`, `eid`, `TEACHER_EID`, `HOUSE_MASTER_EID`, `RECORDED_BY_EID`, `GENERATED_BY_EID`, `CreatedByEID` | All teacher tables, marks tables | Employee ID |
| `STRENGTH` | `STRENGTH`, `count`, `TOTAL_STUDENTS` | TR_ALL (`STRENGTH`), GZT_STRENGTH (`count`), House_Attendance_Daily (`TOTAL_STUDENTS`) | Number of students |

### Performance Metrics

| Canonical Name | Variants Found | Tables | Meaning |
|----------------|---------------|--------|---------|
| `CLASS_AVG` | `CLASS AVG` | TR_ALL | Class average percentage |
| `PASS_RATE` | `PASS%` | TR_ALL | Pass percentage for teacher's class |
| `BOARD_BENCHMARK` | `BOARD` | BOARD_PER | Board exam benchmark percentage |
| `APPEARED` | `APPEARED` | TR_ALL | Number of students who appeared |
| `PASSED` | `PASSED`, `PASS` | TR_ALL (`PASSED`), GZT_STRENGTH (`PASS`) | Number who passed |
| Grade Buckets | `Count_90_100`, `Count_80_90`, `Count_70_80`, `Count_60_70`, `Count_50_60`, `Count_40_50`, `Count_0_39` | TR_ALL | Grade distribution counts |

---

## 2. Known Naming Issues (Typos & Inconsistencies)

| Issue | Location | Correct Value | Impact |
|-------|----------|---------------|--------|
| `CATEGROY` | STUDENTS_ROLL.CATEGROY, TR_ALL.CATEGROY | `CATEGORY` | NLP model must map both spellings |
| `TEAHCERS` | Table name `dbo.TEAHCERS` | `TEACHERS` | NLP model must recognize both |
| `SUBJECT_GORUP_YEAR_MARKS_26` | Table name | `SUBJECT_GROUP_YEAR_MARKS_26` | NLP model must handle the typo |
| `STUDENT NAME` (with space) | ABSENT table column | `STUDENT_NAME` or `STUDENTNAME` | Column name has embedded space |
| `TOTAL MARKS` (with space) | SUBJECT_GROUP_YEAR_MARKS column | `TOTALMARKS` | Column name has embedded space |
| `CLASS AVG` (with space) | TR_ALL column | `CLASS_AVG` | Column name has embedded space |
| `ANNUAL PASS%` (with special char) | SUBJECT_GROUP_YEAR_MARKS column | — | Column name has `%` character |
| `PASS%` (with special char) | TR_ALL column | — | Column name has `%` character |
| `%` (single char column name) | MARKS, Marks_Internal | `PERCENTAGE` | Single-character column name |

---

## 3. Data Type Inconsistencies

| Column | Expected Type | Actual Variants |
|--------|---------------|------------------|
| `CLASS` | `INT` | `varchar(20)` in STUDENTS_ROLL_INTERNAL_EXAM; `int` in Marks_Internal; `float` in MARKS, STUDENTS_ROLL, TEAHCERS; `tinyint` in ALLSCHOOLS26; `smallint` in SUBJECT_GROUP_YEAR_MARKS |
| `YEAR` | `INT` or `SMALLINT` | `int` in most production tables; `float` in legacy/import tables; `tinyint` in ALLSCHOOLS26; `smallint` in config tables; `varchar(2)` in SUBJECT_GORUP_YEAR_MARKS_26 |
| `EID` | `INT` | `int` in production tables; `float` in TEAHCERS and TR_ALL |
| `ROLLNO` | `INT` or `VARCHAR` | `varchar(20)` in STUDENTS_ROLL_INTERNAL_EXAM; `float` in MARKS, STUDENTS_ROLL; `int` in Marks_Internal, ABSENT |
| `SMSNO` | `VARCHAR` or `INT` | `varchar(50)` in STUDENTS_ROLL_INTERNAL_EXAM; `nvarchar(30)` in marks tables; `int` in STUDENTS_ROLL; `nvarchar(50)` in StudentAnswers |
| `MARKS` / `OBTAINED` | `DECIMAL` or `FLOAT` | `float` in MARKS; `decimal` in Marks_Internal |

---

## 4. Exam Type Values

The following exam type values have been observed in the data:

| Value | Meaning |
|-------|---------|
| `MID_DEC` | Mid-year (December) exam |
| `ANNUAL` | Annual exam |
| `MOCK` | Mock exam (practice for board) |
| Other values | TBD — to be confirmed from data |

---

## 5. Category Values

| Value | Meaning |
|-------|---------|
| `B` | Boarder (residential student) |
| `S` | Scholar |
| `DS` | Day Scholar |
| Other values | TBD — to be confirmed from data |

---

## 6. Grade Scale

Based on the `STUDENTS_RESULT_TOTAL_INTERNAL` view logic:

| Grade | Percentage Range |
|-------|------------------|
| A1 (or A+) | 90% and above |
| A | 80–89% |
| B | 70–79% |
| C | 60–69% |
| D | 50–59% |
| E | 40–49% |
| F (Fail) | Below 33% |

**Pass threshold:** 33%

---

## 7. School Codes

20 campuses in the network (10 pairs: Boys/Girls):

| Code | Gender | Likely City/Region |
|------|--------|-----------|
| ATKB | Boys | Attock |
| ATKG | Girls | Attock |
| CTNB | Boys | Chiniot |
| CTNG | Girls | Chiniot |
| DGKB | Boys | D.G. Khan |
| DGKG | Girls | D.G. Khan |
| HSPB | Boys | Hasan Abdal |
| HSPG | Girls | Hasan Abdal |
| MNKB | Boys | Mianwali |
| MNKG | Girls | Mianwali |
| MNWB | Boys | Multan West |
| MNWG | Girls | Multan West |
| RJNB | Boys | Rajanpur |
| RJNG | Girls | Rajanpur |
| RYKB | Boys | Rahim Yar Khan |
| RYKG | Girls | Rahim Yar Khan |
| TNSB | Boys | Taunsa / T.T. Singh |
| TNSG | Girls | Taunsa / T.T. Singh |
| VEHB | Boys | Vehari |
| VEHG | Girls | Vehari |

> **Note:** City names are best-guess from school codes. Confirm with school management.
