# EduQuery AI — Master Schema Definition

> This is the **definitive schema scope** for EduQuery AI model training. Only tables and views listed here should be included in the NLP semantic layer, ML feature engineering, and prompt-to-SQL generation.

**Database:** `db_aadc11_sqldaanish`

**Server:** SQL Server 2022 (MSSQL16), Compatibility Level 160

**Schema inventory last verified:** 2026-08-02 (live database query)

**View reconciliation last verified:** 2026-08-03 (accepted candidate-versus-live audit)

**Total objects in live DB:** 69 tables, 68 views, 2 stored procedures, 13+ indexes

**Objects in master schema:** 35 tables (included) + 26 tables (excluded) + 68 views + 2 procedures

**Repository view-export status:** Both canonical exports contain 68 schema-qualified statements and 68 distinct names. The accepted audit proves 68/68 candidate-versus-live normalized definition matches with zero mismatches.

---

## Included Tables — By Domain

### Domain 1: Student Enrollment (3 tables)

| Table | Rows | Purpose | PK | Key Columns |
|-------|------|---------|----|---------|
| `STUDENTS_ROLL_INTERNAL_EXAM` | 72,752 | Student enrollment per internal exam | ID (identity) | SCHOOL, SMSNO, ROLLNO, STUDENT, FATHER, CLASS, SECTION, CATEGORY, YEAR, HOUSE, EXAM |
| `STUDENTS_ROLL_PROFILE` | 4,618 | Student master with active/inactive status | ID (identity) | Same as above + STATUS |
| `STUDENTS_ROLL` | 63,910 | Board exam student roll | ID | SCHOOL, SMSNO, ROLLNO, STUDENT, FATHER, CLASS, SECTION, CATEGROY*, YEAR |

*CATEGROY is a typo for CATEGORY — documented in canonical_column_reference.md

### Domain 2: Marks & Results (7 tables)

| Table | Rows | Purpose | PK |
|-------|------|---------|----|
| `MARKS` | 405,325 | Board/annual exam marks (permanent store) | ID |
| `Marks_Internal` | 428,926 | Internal exam marks (permanent store) | ID |
| `PRAC` | 17,413 | Practical exam marks (separate from theory) | ID (identity) |
| `ALL_COMBINED` | 20,463 | Combined marks from multiple sources | None |
| `ALL_COMBINED2_SNAPSHOT` | 0* | Snapshot with teacher attribution + grades | None |
| `HOF` | 11,806 | Hall of Fame — marks + grades + teacher info | ID (identity) |
| `TR_ALL` | 11,806 | Teacher result summary with grade distribution | None |

*Populated on-demand during result finalization cycles

### Domain 3: Teacher Management (4 tables)

| Table | Rows | Purpose | PK |
|-------|------|---------|----|
| `TEACHERS_PROFILE` | 367 | Teacher master — active assignments | TID (identity) |
| `TEACHERS_INTERNAL_EXAM` | 18,370 | Teacher-exam assignments with WL_LESSONS | ID |
| `TEAHCERS`* | 16,505 | Teacher assignments with STRENGTH (legacy) | ID |
| `ALLSCHOOLS26` | 3,279 | Teacher-subject assignments for all schools 2026 | None |

*Table name is a typo for TEACHERS — documented in canonical_column_reference.md

### Domain 4: Subject Configuration (5 tables)

| Table | Rows | Purpose | PK |
|-------|------|---------|----|
| `SUBJECTS` | 9 | Subject master (smaller set) | None |
| `CorrectSubjects` | 65 | Full subject master with abbreviations | None |
| `SubjectTotals` | 10 | Max marks per subject per class | None |
| `SUBJECT_GROUP_YEAR_MARKS` | 496 | Total marks config per subject/group/year | ID |
| `SUBJECT_GORUP_YEAR_MARKS_26`* | 1,212 | 2026 version with exam dates | None |

*Table name typo: GORUP → GROUP

### Domain 5: Board Benchmarks (2 tables)

| Table | Rows | Purpose | PK |
|-------|------|---------|----|
| `BOARD_PER` | 208 | Board exam benchmark percentages | ID |
| `GZT_STRENGTH` | 390 | Board gazette strength data (2022-2025) | ID |

### Domain 6: Exam Operations (5 tables)

| Table | Rows | Purpose | PK |
|-------|------|---------|----|
| `Exam_Schedule` | 29 | Generic exam schedule | ESID (identity) |
| `Exam_Schedule_26` | 1,032 | 2026 exam schedule | ESID (identity) |
| `MarksEntryAccessControl` | 219 | Marks entry open/close control | AccessID (identity) |
| `ClassTestScheduleRequests` | 13 | Teacher class test requests | RequestID (identity) |
| `ROLLNOSLIPS_STATUS` | 78 | Roll number slip generation tracking | ID (identity) |

### Domain 7: Attendance (3 tables)

| Table | Rows | Purpose | PK |
|-------|------|---------|----|
| `House_Attendance_Daily` | 13,181 | Daily attendance by house | ID (identity) |
| `House_Management` | 4 | House master data | HouseID (identity) |
| `ABSENT` | 242 | Exam absentees per subject | ID |

### Domain 8: Quiz System (3 tables)

| Table | Rows | Purpose | PK |
|-------|------|---------|----|
| `Subjects_Quiz` | 14 | Quiz subject master | SubjectID (identity) |
| `Questions` | 3 | MCQ question bank | QuestionID (identity) |
| `StudentAnswers` | 0 | Student quiz responses | AnswerID (identity) |

### Domain 9: Administrative (3 tables)

| Table | Rows | Purpose | PK |
|-------|------|---------|----|
| `STAFF_EMPLOYEE_CARD` | 5 | Staff HR data | ID (identity) |
| `DBDSUGGESTIONS` | 882 | Teacher suggestions to admin | ID (identity) |
| `StudentResultLogs` | 6,091 | Result viewing audit trail | LogID (identity) |

---

## Excluded Tables (26 — NOT part of AI training)

| # | Table | Rows | Reason |
|---|-------|------|--------|
| 1 | `12_25` | 1,042 | Raw import snapshot (all nvarchar255/float) |
| 2 | `4SCHL` | 2,953 | Ad-hoc 4-school student snapshot |
| 3 | `678_SUB` | 9 | Duplicate subset of CorrectSubjects |
| 4 | `ctnb810` | 223 | Duplicate subset of CorrectSubjects |
| 5 | `Ctttt` | 752 | Scratch data dump |
| 6 | `mar` | 7,261 | Marks data dump (one-off analysis) |
| 7 | `mmm` | 735 | Student roll dump (MNWB school) |
| 8 | `rafia` | 654 | Single-school data (named after person) |
| 9 | `MNKRA_UP` | 267 | One-school student data |
| 10 | `MNMARKS` | 267 | One-school marks data |
| 11 | `marks_with_school_name` | 347,713 | Old denormalized marks copy |
| 12 | `MISSED_RSLT_678` | 10 | One-time missing results |
| 13 | `PALCEMENT_ATKB` | 179 | One-school placement data |
| 14 | `TNS` | 542 | Teacher-subject snapshot |
| 15 | `TR` | 38,937 | Raw teacher results (float types, CATEGROY typo) |
| 16 | `ALL` | 12,592 | Duplicate student roll data |
| 17 | `ALLSTD26` | 7,414 | Year-specific student snapshot |
| 18 | `ExamMarksDeletionQueries` | 8 | Meta table storing SQL commands |
| 19 | `STUDENTS_ROLL_BKP` | 41,051 | Backup table |
| 20 | `STUDENTS_ROLL_BKP_BEFORE_PROMOTION_27` | 47,342 | Pre-promotion backup |
| 21 | `TEAHCERS_BKP` | 10,399 | Teacher backup (typo name) |
| 22 | `HOF_OLD` | 8,956 | Old Hall of Fame |
| 23 | `ALL_COMBINED_OLD` | 16,056 | Old combined marks |
| 24 | `Marksold` | 299,625 | Old marks data |
| 25 | `ALL_COMBINED_FINAL` | 0 | Unused/legacy table (dynamically generated instead) |
| 26 | `SUBJECT_MARKS_EXAM_RUNTIME` | 567 | Unused/orphaned staging table |

---

## Views (68 reported in live DB)

The live scope contains 68 views. Both canonical exports now contain the same 68 schema-qualified definitions, proven by the accepted candidate-versus-live set and hash comparisons. Key analytics views:

| View | Source Tables | Purpose |
|------|--------------|--------|
| `vw_CONSOLIDATED_ACCURATE` | MARKS, STUDENTS_ROLL | Core: Student results with %, grade, pass/fail |
| `STUDENTS_RESULT_TOTAL_INTERNAL` | MARKS_INTERNAL, STUDENTS_ROLL_INTERNAL_EXAM | Student total marks per internal exam |
| `TR_ALL_DEDUCTED` | MARKS, STUDENTS_ROLL | Teacher results with grade buckets |
| `VW_TEACHER_SUMMARY_MNWB` | MARKS, STUDENTS_ROLL, TEACHERS_PROFILE | Multi-school teacher summary |
| `vw_School_Mock_Performance_Summary` | vw_CONSOLIDATED_ACCURATE | School-level mock exam performance |
| `vw_StudentCategoryStrength` | STUDENTS_ROLL_INTERNAL_EXAM | Student counts by category |
| `CC_ALL` | STUDENTS_ROLL_INTERNAL_EXAM | Category counts with GROUPING SETS |
| `INTERNAL_CONSOLIDATED_RESULT_SHEET_VIEW` | MARKS_INTERNAL, STUDENTS_ROLL_INTERNAL_EXAM | Consolidated internal result sheet |
| `INTERNAL_STUDENT_RESULT_CARD_VIEW` | MARKS_INTERNAL, STUDENTS_ROLL_INTERNAL_EXAM | Individual student result card |
| `INTERNAL_STUDENT_SUMMARY_RANKS` | TBD | Student ranking within class |
| `Data_Entry_Status_View` | TBD | Marks entry progress |
| `vw_Expired_Exam_Deadlines` | Exam_Schedule, Exam_Schedule_26 | Overdue exam deadlines |
| `V_STUDENT_DATA_QUALITY_CHECK_INTERNAL` | TBD | Data quality validation |
| (+ 55 more views) | Various | Various analytics |


---

## Stored Procedures (2)

| Procedure | Parameters | Purpose |
|-----------|------------|--------|
| `GenerateConsolidatedView` | @ExamType, @Year | Dynamically generates consolidated result view |
| `Refresh_ALL_COMBINED2_SNAPSHOT` | None | Repopulates snapshot with teacher attribution |

---

## EduQuery AI Prompt Family → Schema Mapping

| Prompt Family | Primary Tables/Views | Domain |
|---------------|---------------------|--------|
| A: Student Lookup | STUDENTS_ROLL_INTERNAL_EXAM, STUDENTS_ROLL_PROFILE, STUDENTS_ROLL | Student |
| B: Individual Results | MARKS, Marks_Internal, STUDENTS_RESULT_TOTAL_INTERNAL, vw_CONSOLIDATED_ACCURATE | Marks |
| C: Class/Section Aggregates | vw_CONSOLIDATED_ACCURATE, TR_ALL, TR_ALL_DEDUCTED, CC_ALL | Marks + Teacher |
| D: Cross-School Comparison | vw_School_Mock_Performance_Summary, TR_ALL, GZT_STRENGTH | Board + Teacher |
| E: Teacher Analytics | TEACHERS_PROFILE, TR_ALL_DEDUCTED, VW_TEACHER_SUMMARY_MNWB, HOF | Teacher |
| F: Board Benchmarks | BOARD_PER, GZT_STRENGTH, TR_ALL | Board |
| G: Absenteeism | ABSENT, House_Attendance_Daily | Attendance |
| H: Exam Operations | Exam_Schedule, Exam_Schedule_26, MarksEntryAccessControl, vw_Expired_Exam_Deadlines | Exam Ops |
| I: Data Quality | V_STUDENT_DATA_QUALITY_CHECK_INTERNAL, Data_Entry_Status_View | Admin |
| J: Multi-Year Trends | MARKS, Marks_Internal, GZT_STRENGTH, TR_ALL (multi-year data) | Marks + Board |
| K: Future Predictions | MARKS, Marks_Internal, ABSENT, TR_ALL, BOARD_PER (ML features) | ML |
| L: Explainability | SHAP output on K features | ML |

---

## Daanish 610-Prompt Catalog Reconciliation — 2026-08-16

Read-only inspection of the local July 13 restore verified the physical objects named by the school-supplied catalog. Client labels are intent metadata; live catalog names and columns remain authoritative.

| Client family | Verified live object | Type | Wren handling | Verified caveat |
|---|---|---|---|---|
| `STUDENTS_ROLL` | `dbo.STUDENTS_ROLL` | Table | `board_enrollment` | Board/annual enrollment source |
| `MARKS` | `dbo.MARKS` | Table | `board_marks` | Does not contain campus; campus joins need the approved roll/class/year relationship |
| `PRAC` | `dbo.PRAC` | Table | `practical_marks` | Does not contain campus; same join constraint as `MARKS` |
| `TR2_THEORY` | `dbo.TR2_Theory` | View | `theory_teacher_results` | Teacher-level theory aggregates |
| `TR2_PRAC` | `dbo.TR2_Prac` | View | `practical_teacher_results` | Teacher-level practical aggregates |
| `TR_ALL` | `dbo.TR_ALL` | Table | `teacher_results` | Expanded to include appeared/category and grade bands |
| `ALL_COMBINED` | `dbo.ALL_COMBINED` | Table | `teacher_career` | Numeric KPIs are stored as `nvarchar`; Wren queries use guarded numeric conversion for aggregation/order |
| `HOF_FRMT` | `dbo.HOF_FRMT` | View | `head_office_results` | Broad scans take about eight seconds on the restore |
| `INTERNAL_EXAM_GROUP_WISE_PERFORMANCE_VIEW` | same | View | `internal_teacher_results` | Broad scans take about five to twelve seconds and can time out under concurrent load |
| `SCHOOL_IND_POS_SUB` | `dbo.School_Ind_Pos_SUB` | View | Governed refusal | Live columns are school-level aggregates; no student, roll, subject, or individual-rank fields exist |
| `STUDENT_RESULT_TOTAL` | `dbo.STUDENTS_RESULT_TOTAL` | View | `annual_student_results` | Client catalog used the singular alias; live object is plural |
| `STUDENT_RESULT_TOTAL_INTERNAL` | `dbo.STUDENTS_RESULT_TOTAL_INTERNAL` | View | Safe fallback to `student_result_card` | Live plural view can fail when `STRING_AGG` exceeds 8,000 bytes |
| `vTeacher_sum_per` | `dbo.vTeacher_sum_per` and `dbo.vTeacher_sum_per_BOARD_MIDDLE` | Views | `teacher_overall` / `teacher_board_middle` | Board/Middle wording routes to the split view |

The supplied 55 cross-table prompts are requirements, not verified join/metric contracts. They remain blocked until the human owner approves each join grain, metric definition, and prediction boundary.

---

## Additional Requirements for Schema Completeness

> [!IMPORTANT]
> The following items were identified during analysis and need to be addressed:

1. **Confirm school code → school name mapping** — The 20 school codes need official full names.
2. **Domain-validate Gold Answers** — All 610 supplied prompts are routed and statically planned or safely refused, but expected SQL/result truth and human acceptance are still required for answer-accuracy claims.
3. **Complete Wren AI MDL** — The strict 16-model MDL covers verified single-object families. Cross-table contracts and the correct student subject-position source remain pending.
