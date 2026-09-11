# EduQuery AI — Meeting Notes: 2 August 2026 (Sunday)

## Attendees

> [TBD — fill in after meeting]

## Agenda

1. Schema Analysis Progress Report
2. Database Architecture Decisions
3. Master Schema Definition for AI Training
4. Open Questions Requiring Team Input

---

## 1. Schema Analysis Progress

### What Was Done
- Full export of `db_aadc11_sqldaanish` database schema (script.sql — 6933 lines DDL)
- Live database queried and verified against the export
- **Finding:** Live DB has **69 tables** and **68 views** — the SQL export only captured 59 tables and 17 views
- Complete table categorization: production core, authentication, quiz, aggregated, backup, scratch/temporary
- Row count analysis performed on all 69 tables
- Cross-reference with EduQuery AI proposal, brief, and planning documents completed

### Key Statistics
| Metric | Count |
|--------|-------|
| Total tables (live DB) | 69 |
| Total views (live DB) | 68 |
| Stored procedures | 2 |
| Indexes | 13+ |
| Schools in network | 20 (10 pairs: Boys/Girls campuses) |
| Largest table | `Marks_Internal` (428,926 rows) |
| Largest marks table | `MARKS` (405,325 rows) |

### School Network (20 Campuses)
| Code | Likely Location |
|------|----------------|
| ATKB / ATKG | Attock Boys / Girls |
| CTNB / CTNG | Chiniot/Chichawatni Boys / Girls |
| DGKB / DGKG | D.G. Khan Boys / Girls |
| HSPB / HSPG | Hasan Abdal/Hasanpur Boys / Girls |
| MNKB / MNKG | Mianwali Boys / Girls |
| MNWB / MNWG | Multan/Mianwali West Boys / Girls |
| RJNB / RJNG | Rajanpur Boys / Girls |
| RYKB / RYKG | Rahim Yar Khan Boys / Girls |
| TNSB / TNSG | T.T. Singh/Taunsa Boys / Girls |
| VEHB / VEHG | Vehari Boys / Girls |

> **ACTION:** Confirm actual school names for the codes above.

---

## 2. Questions for Discussion

### Q1: `ALL_COMBINED` vs `ALL_COMBINED_FINAL`
- Analysis of the 68 exported views and stored procedures reveals that `ALL_COMBINED_FINAL` is **not** actively used by core views.
- Instead, the system uses a stored procedure `GenerateConsolidatedView` which dynamically builds a `vw_consolidated_NEW` directly from the `MARKS` and `STUDENTS_ROLL` tables.
- Another procedure, `Refresh_ALL_COMBINED2_SNAPSHOT`, creates a snapshot of teacher performance using `TR_ALL_SECTIONS_POS` and `BOARD_MIDDLE`.
- **Conclusion:** `ALL_COMBINED_FINAL` is likely a legacy or abandoned table. The true source of truth is the `MARKS` and `Marks_Internal` tables, which feed into views like `STUDENTS_RESULT_TOTAL`.

### Q2: Scratch/Temporary Tables
- ~20 tables identified as scratch/temporary, including credential-bearing and one-off import sources
- Database is in active production use
- **Question:** Can we create a documentation-only "exclude list" so the AI model ignores these tables? No DB changes needed.
- **Recommendation:** Don't delete them from the live DB — just exclude them from the AI training schema definition

### Q3: Tables Missing from Script Export
The following tables exist in the live DB but were NOT in the SQL script export:
| Table | Rows | Purpose |
|-------|------|---------|
| `MARKS` | 405,325 | Board/annual exam marks (SUBJECT, OBTAINED, TOTAL, %, GRADE, STATUS, ROLLNO, CLASS, YEAR, EXAMTYPE) |
| `Marks_Internal` | 428,926 | Internal exam marks (same structure + Remarks column) |
| `STUDENTS_ROLL` | 63,910 | Student enrollment (board exam roll list, has `CATEGROY` typo) |
| `TEAHCERS` | 16,505 | Teacher assignments with STRENGTH (typo name, float types) |
| `TEACHERS_INTERNAL_EXAM` | 18,370 | Teacher assignments per internal exam (proper types + WL_LESSONS) |
| `ABSENT` | 242 | Absent students per subject per exam |
| `BOARD_PER` | 208 | Board benchmark percentages per subject |
| `SUBJECT_GROUP_YEAR_MARKS` | 496 | Total marks config per subject/group/year |
| `SUBJECT_GORUP_YEAR_MARKS_26` | 1,212 | 2026 version (typo in name, adds StartDate/EndDate) |
| `ALLSCHOOLS26` | 3,279 | Teacher-subject assignments for all schools 2026 (NOT a schools list!) |

- **Question:** These are critical tables (`MARKS` is 405K rows, `Marks_Internal` is 429K rows). Should they be included in the master schema? They appear to be the PRIMARY marks data.

### Q4: `MARKS` / `Marks_Internal` vs `SUBJECT_MARKS_EXAM_RUNTIME`
- `MARKS` (405K rows) and `Marks_Internal` (429K rows) use ROLLNO-based identification and are the **primary source tables** for all major analytical views (`STUDENTS_RESULT_TOTAL`, `vw_CONSOLIDATED_ACCURATE`, etc.).
- `SUBJECT_MARKS_EXAM_RUNTIME` (567 rows) uses SMSNO-based identification but is **not referenced by any of the 68 live views or stored procedures**.
- **Conclusion:** `SUBJECT_MARKS_EXAM_RUNTIME` is likely an orphaned or deprecated staging table. `MARKS` and `Marks_Internal` are the definitive, permanent stores and the true data source for the AI semantic layer.

### Q5: View Export Completeness
- **Status at meeting:** Needed live verification.
- **Resolved 2026-08-03:** Captured 68 distinct schema-qualified live catalog names (`sys.views` joined with `sys.schemas` and `sys.sql_modules`). Standardized candidate export (`database_views_export_verified_candidate.sql`) containing 68 schema-qualified statements and 68 distinct names. Independently verified 68/68 candidate-versus-live normalized SHA-256 definition hash equality with 0 mismatches (`candidate_live_definition_hash_comparison.csv` and `candidate_live_set_comparison.csv`). Canonical export files updated to byte-identical match. Supporting evidence retained under `docs/07-evidence/sql-view-reconciliation/`.

### Q6: GZT_STRENGTH / GZT_CR
- Data confirmed: 390 rows, spans years 2022-2025, tracks school strength and pass counts per class
- GZT appears to be a "Gazette" (board exam result gazette) tracking system
- **Recommendation:** Include in master schema — contains multi-year historical board performance data

---

## 3. Decisions Made

| # | Decision | Status |
|---|----------|--------|
| D1 | Master schema will be defined as a cleaned subset of the production DB — no structural DB changes | ✅ Approved |
| D2 | Scratch/temporary tables will be excluded via documentation, not deleted | ✅ Approved |
| D3 | Semantic relationship map and canonical column reference will be created | ✅ Approved |
| D4 | Optional DB improvements listed as future changes, not immediate | ✅ Approved |

## 4. Action Items

| # | Action | Owner | Status |
|---|--------|-------|--------|
| A1 | Reconcile legacy export headers with the 68-view live catalog inventory | AI/Dev | Resolved 2026-08-03 |
| A2 | Create semantic relationship map (JSON) | AI/Dev | ✅ Done |
| A3 | Create canonical column reference | AI/Dev | ✅ Done |
| A4 | Confirm school name codes (ATKB, CTNB, etc.) | Team | Moved to Questionnaire |
| A5 | Clarify ALL_COMBINED_FINAL and SUBJECT_MARKS_EXAM_RUNTIME | AI/Dev | ✅ Resolved (they are unused/legacy) |

---

## Next Meeting

> [TBD]
