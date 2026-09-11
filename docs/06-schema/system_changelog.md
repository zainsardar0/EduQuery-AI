# EduQuery AI — System Changelog

> This file records all system-level changes for Codex memory synchronization.
> Updated after every meaningful change to the project.

---

## [2026-08-16] - Daanish 610-Prompt External-Off Wren Hardening

- Verified both school-supplied inputs locally: 610 sequential unique prompts, 13 named schema families plus 55 cross-table requests.
- Reconciled every named family against the read-only live catalog. Corrected singular result-card aliases to the plural live views and recorded that `School_Ind_Pos_SUB` is a school aggregate rather than a student subject-rank source.
- Expanded the strict Wren project from 5 to 16 models without adding a second NL2SQL framework or dependency.
- Added protected local catalog routing, strict SQL planning, adapter object gates, parameterized family queries, explicit cross-table/position refusals, and two-sentence local data-grounded summaries.
- Removed `STUDENTS_RESULT_TOTAL_INTERNAL` from the execution allowlist after reproducing its `STRING_AGG` 8,000-byte overflow; internal cards use the existing verified result-card view.
- Verified 515 static Wren plans with zero planning/parameter failures. A four-worker live sweep completed 510/515; the five failures were slow-view concurrency failures and each passed individually. Full regression: 299 tests passed with external calls disabled.
- This evidence proves routing, strict planning, safety and execution coverage. It does not prove answer correctness because expected SQL/results and Daanish human validation were not supplied.

## [2026-08-03] - SQL Server View Reconciliation & Schema Sync Complete

- **Live View Evidence Captured:** Antigravity connected to `db_aadc11_sqldaanish` through a local-only Windows Integrated session and performed read-only inspection of `sys.views` and `sys.sql_modules`. Its retained evidence records exactly 68 distinct live views, with all definitions available and unencrypted. Zero database mutations were reported. The successful session used `Encrypt=False` locally; this is not an approved remote or production configuration.
- **Root Cause & Discrepancy Resolved:** Anchored parsing confirms the legacy exports contained 68 actual `CREATE VIEW` statements / 66 distinct header names versus 68 captured live catalog names. Three live views (`BOARD_MIDDLE`, `BOARD_MIDDLE_old`, `BOARD_MIDDLE_WORKING`) retained obsolete `CREATE VIEW BOARD_MIDDLE2 AS` headers in `sys.sql_modules.definition`; `BOARD_MIDDLE2` does not exist in `sys.views`. Other definitions also retained obsolete draft headers.
- **Candidate Export:** Generated `database_views_export_verified_candidate.sql` with 68 deterministically ordered, schema-qualified statements matching the captured catalog-name set. The final `candidate_live_set_comparison.csv` and `candidate_live_definition_hash_comparison.csv` independently prove 68 matched names and 68/68 normalized definition hashes with zero mismatches. The older `definition_hash_comparison.csv` remains historical live-versus-legacy evidence.
- **Evidence Promotion:** Moved the accepted sanitized reconciliation package from `_draft/` to `docs/07-evidence/sql-view-reconciliation/` and indexed it from Project Control and the Document Guide.
- **Canonical Exports Replaced and Repository-Verified:** `docs/06-schema/database_views_export.sql`, `database_views_export_live.sql` and the verified candidate are byte-identical (SHA-256 `93b40692d521d655d8e70b5cfeaa1935d839864a85473179df3bc443f342e21c`). Each contains 68 statements, 68 distinct schema-qualified names and zero duplicates.
- **Full Delivery Scope Locked:** English working Next.js/FastAPI/Wren MVP, semantic documentation, at least 200 evaluated gold prompts, AutoGluon and TabPFN with MLflow, adaptive model selection, representative SHAP reports, security evidence, final report and live demonstration.
- **Privacy Boundary Approved:** Student identities, academic rows, marks, results, predictions and protected prompts remain inside the institution. Local RAG contains only approved semantic documentation and examples.
- **External Model Approved with Restrictions:** GPT 5.6 Luna Pro through OpenRouter receives only locally redacted/tokenized intent and schema context. Zero-retention and no-data-collection routing are required but do not replace content exclusion.
- **Split Deployment Approved:** Vercel hosts the Next.js UI/static assets. FastAPI, Wren AI, RAG, SQL access, model services, MLflow, SHAP and audit storage remain institutional.

## [2026-08-02] - Schema Scope Reconciliation
- **Created MVP Semantic Model (`semantic_model.json`)**: Added a partial six-table MVP mapping with four validated relationships. It is not the final Wren AI MDL layer.
- **Training Boundary Enforced**: The master schema now contains 35 included tables and 26 excluded tables. Semantic artifacts contain only the approved scope.
- **Semantic Map Reconciled**: Removed excluded-table relationships, vocabulary, and inventory metadata. The map now contains 22 approved relationships.
- **Canonical Reference Reconciled**: Removed excluded-table aliases and data-type notes from the NLP column reference.
- **Historical View Export Status (superseded 2026-08-03):** Before reconciliation, anchored parsing found 68 statements representing 66 distinct header names. The canonical export has since been replaced by the verified 68-name candidate.
- **Meeting Notes Updated**: Resolutions remain in `meeting_notes_2026-08-02.md`; no separate stakeholder-question file is tracked.
- **Updated** Codex Brain index to include the SQL view export.

## 2026-08-02 — Initial Schema Assessment Phase

### Files Created

| File | Path | Purpose |
|------|------|---------|
| Meeting Notes | `docs/06-schema/meeting_notes_2026-08-02.md` | Aug 2 Sunday meeting agenda, schema analysis progress, questions for team |
| Timeline Progress | `docs/06-schema/timeline_progress.md` | Master progress tracker for all schema and data layer work |
| Semantic Relationship Map | `docs/06-schema/semantic_relationship_map.json` | Curated implicit relationships for the approved NLP training scope (no FK exists in DB) |
| MVP Semantic Model | `docs/06-schema/semantic_model.json` | Partial six-table MVP mapping; not the final Wren AI MDL |
| View Export | `docs/06-schema/database_views_export.sql` | Verified candidate: 68 statements, 68 distinct schema-qualified names, zero duplicates |
| Canonical Column Reference | `docs/06-schema/canonical_column_reference.md` | Column name standardization, synonym mapping, data type inconsistencies |
| Master Schema Definition | `docs/06-schema/master_schema.md` | Definitive schema scope for AI model training — lists included/excluded tables |
| System Changelog | `docs/06-schema/system_changelog.md` | This file — all changes for Codex sync |
| Future DB Changes | `docs/06-schema/future_db_changes.md` | Deferred database improvements (optional, school management approval required) |

### Key Findings

1. **Database:** `db_aadc11_sqldaanish` on SQL Server 2022 (MSSQL16), compatibility level 160
2. **Live DB inventory:** 69 tables, 68 views, 2 stored procedures, 13+ indexes
3. **SQL export gap:** The `docs/script.sql` export (6933 lines) only captured 59/69 tables and 17/68 views
4. **Tables missing from export but present in live DB:**
   - `MARKS` (405,325 rows) — Board/annual exam marks
   - `Marks_Internal` (428,926 rows) — Internal exam marks
   - `STUDENTS_ROLL` (63,910 rows) — Board exam student enrollment
   - `TEAHCERS` (16,505 rows) — Teacher assignments (legacy, typo name)
   - `TEACHERS_INTERNAL_EXAM` (18,370 rows) — Teacher-exam assignments
   - `ABSENT` (242 rows) — Exam absentees
   - `BOARD_PER` (208 rows) — Board benchmark percentages
   - `SUBJECT_GROUP_YEAR_MARKS` (496 rows) — Total marks config
   - `SUBJECT_GORUP_YEAR_MARKS_26` (1,212 rows) — 2026 marks config (typo name)
   - `ALLSCHOOLS26` (3,279 rows) — Teacher-subject assignments (NOT a schools list)
5. **School network:** 20 campuses (10 Boys + 10 Girls) — ATKB/G, CTNB/G, DGKB/G, HSPB/G, MNKB/G, MNWB/G, RJNB/G, RYKB/G, TNSB/G, VEHB/G
6. **No foreign keys exist** in the entire database — all relationships are implicit
7. **26 non-training tables** are excluded from the master schema; sensitive and credential-bearing sources are not represented in training artifacts
8. **GZT_STRENGTH verified active** — 390 rows, multi-year (2022-2025) board gazette data
9. **ALLSCHOOLS26 corrected** — Not a school name list; it's teacher-subject assignments for 2026
10. **ALL_COMBINED_FINAL has 0 rows** — populated on-demand for result card submission

### Decisions Recorded

| Decision | Status | Notes |
|----------|--------|-------|
| Master schema = cleaned subset of production DB | Approved | No structural DB changes |
| Scratch tables excluded via documentation only | Approved | Don't delete from live DB |
| Semantic relationship map to be created | Approved | JSON format in docs/06-schema/ |
| Canonical column reference to be created | Approved | Markdown format in docs/06-schema/ |
| Optional DB improvements listed as future changes | Approved | Deferred to school management approval |
| Exam_Schedule_26 is 2026-specific exam schedule | Confirmed | Both Exam_Schedule and Exam_Schedule_26 active |
| ALL_COMBINED_FINAL is populated on-demand for result cards | Confirmed | Currently 0 rows is expected |

### Schema Categories Defined

The master schema organizes tables into:
- **Core Student** (3 tables): STUDENTS_ROLL_INTERNAL_EXAM, STUDENTS_ROLL_PROFILE, STUDENTS_ROLL
- **Core Marks** (7 tables): MARKS, Marks_Internal, PRAC, ALL_COMBINED, ALL_COMBINED2_SNAPSHOT, HOF, TR_ALL
- **Core Teacher** (4 tables): TEACHERS_PROFILE, TEACHERS_INTERNAL_EXAM, TEAHCERS, ALLSCHOOLS26
- **Core Subject** (5 tables): SUBJECTS, CorrectSubjects, SubjectTotals, SUBJECT_GROUP_YEAR_MARKS, SUBJECT_GORUP_YEAR_MARKS_26
- **Board Benchmark** (2 tables): BOARD_PER, GZT_STRENGTH
- **Exam Operations** (5 tables): Exam_Schedule, Exam_Schedule_26, MarksEntryAccessControl, ClassTestScheduleRequests, ROLLNOSLIPS_STATUS
- **Attendance** (3 tables): House_Attendance_Daily, House_Management, ABSENT
- **Quiz** (3 tables): Subjects_Quiz, Questions, StudentAnswers
- **Administrative** (3 tables): DBDSUGGESTIONS, StudentResultLogs, STAFF_EMPLOYEE_CARD
- **Excluded** (26 tables): Scratch, backup, temporary, and unused legacy tables

### Impact on EduQuery AI

- The NLP model training schema is now well-defined (35 approved tables; 68 reported live views)
- The semantic relationship map provides 22 approved join relationships (no FKs to rely on)
- The canonical column reference resolves naming ambiguities for prompt-to-SQL generation
- Critical tables `MARKS` (405K rows) and `Marks_Internal` (429K rows) were discovered and must be included — they are the PRIMARY marks data stores
- The `BOARD_PER` table is essential for Prompt Family F (board benchmark comparisons)
- The `ABSENT` table is essential for Prompt Family G (absenteeism analytics)
