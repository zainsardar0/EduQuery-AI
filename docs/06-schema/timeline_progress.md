# EduQuery AI - Schema and Data Layer Timeline Progress

> Tracks database-schema analysis, semantic-layer preparation, live verification and related delivery milestones. Status claims must distinguish repository checks, captured live evidence and independently repeatable live checks.

## Progress Log

### 2026-08-16 - Daanish 610-Prompt Wren Reconciliation

| Check | Result |
|---|---|
| Client inputs | 610 sequential, unique prompts; CSV SHA-256 `8969cc00350a9db84f5494099d116e5b3622368f9163b2da78cc8752c3f48379` |
| Live schema | All 13 named families checked read-only; singular result labels reconciled to plural live views |
| Strict Wren MDL | Expanded from 5 to 16 models; strict validation/build passed |
| External-off planning | 515 prompts compile through the verified single-object family; 95 governed refusals (55 cross-table, 40 invalid student-position source) |
| Live sweep | 510/515 concurrent executions succeeded; p50 28.43 ms, p95 1091.17 ms; five slow-view requests failed only under the four-worker sweep and passed individually |
| Regression | 299 tests passed; external planner disabled |
| Accuracy boundary | Routing/execution evidence is not domain answer accuracy; expected SQL/results and human validation were not supplied |

### 2026-08-02 - Schema Analysis Started

| Activity | Outcome |
|---|---|
| Located repository schema export | `docs/script.sql`, UTF-16LE, 6,933 lines |
| Parsed export inventory | 59 tables, 17 views, 2 stored procedures and 13 indexes |
| Inspected live inventory | 69 tables and 68 views reported |
| Profiled major tables | `Marks_Internal` approximately 429K rows; `MARKS` approximately 405K rows |
| Verified school network | 20 campuses: 10 boys and 10 girls campuses |
| Classified scratch objects | Non-production scratch/temporary tables documented and excluded |
| Found export gaps | Critical tables missing from the original export were documented |
| Corrected `ALLSCHOOLS26` | Teacher-subject assignment table, not a school list |
| Created schema documentation | Meeting notes, relationship map, canonical columns, master schema, changelog and future-change record |

### 2026-08-02 - Documentation Reconciliation

- Locked the approved NLP scope at 35 included tables and 26 excluded tables.
- Removed excluded, credential-bearing and authentication objects from training-bound semantic artifacts.
- Validated the partial six-table semantic model and its four declared relationships.
- Recorded the repository/live view-count discrepancy for read-only verification.

### 2026-08-03 - MVP Architecture and Delivery Decisions

| Decision/status | Outcome |
|---|---|
| Data | Database access and sanitized data are available |
| Frontend | Ready; intentionally held for integration after the backend is complete |
| Language | English-only MVP; multilingual support is future work |
| Model provider | GPT 5.6 Luna Pro through OpenRouter |
| Data sovereignty | Student identities, row-level academic data, results, predictions and protected prompts remain inside the institution |
| RAG | Local retrieval over approved schema, glossary, metrics, MDL and verified examples; no raw student data in retrieval/external context |
| Deployment | Next.js UI/static assets on Vercel; FastAPI, Wren AI, RAG, SQL access, MLflow/models, SHAP and audit services inside the institution |
| August 20 scope | Working FastAPI/Next.js/Wren MVP, semantic documentation, 200+ evaluated gold prompts, AutoGluon/TabPFN/MLflow, adaptive selection, SHAP samples, security evidence, final report and live demo |

### 2026-08-03 - Live View Reconciliation Completed by Antigravity

| Check | Result |
|---|---|
| Live catalog evidence | Antigravity's read-only session captured 68 distinct schema-qualified `sys.views` entries; all definitions were available and unencrypted |
| Legacy anchored parsing | 68 actual `CREATE VIEW` statements representing 66 distinct parsed names |
| Legacy duplicate | `BOARD_MIDDLE2` appeared three times and does not exist in the live catalog |
| Root cause | Several `sys.sql_modules.definition` headers retained obsolete draft names even though `sys.views` contained the authoritative catalog names |
| Captured legacy set comparison | 14 live catalog names were absent under their correct names; 12 obsolete header names were absent from the live catalog |
| Verified candidate | 68 deterministically ordered, schema-qualified statements with 68 distinct names and zero duplicates |
| Canonical exports | `database_views_export.sql`, `database_views_export_live.sql` and the verified candidate are byte-identical (SHA-256 `93b40692d521d655d8e70b5cfeaa1935d839864a85473179df3bc443f342e21c`) |
| Safety | Read-only catalog/definition inspection; no database mutation or student-row extraction |
| Replayable final audit | `candidate_live_set_comparison.csv` contains 68 `MATCHED` rows; `candidate_live_definition_hash_comparison.csv` contains 68 populated and equal live/candidate hashes with zero mismatches |
| Codex artifact check | Counts, distinct names, CSV columns, hashes and canonical byte equality independently confirmed. A separate Codex live reconnect was unnecessary for artifact acceptance and remained unavailable under its SSPI execution identity |

### 2026-08-03 — Shared Contracts & Governed Semantic Assets Step 1 Completed by Antigravity

| Check | Result |
|---|---|
| OpenAPI 3.1 & Schemas | Added `packages/contracts/openapi.json` and JSON schemas (`auth_context`, `error_response`, `query_request/response`, `prediction_request/response`) |
| Governance & Topology | Created `CONTRACTS_SPEC.md` and `SEMANTIC_GOVERNANCE.md` detailing security boundaries and 26-table exclusion list |
| Governed MVP Slice | Created `data/semantic/mvp_semantic_slice.json` (6 approved tables, 4 relationships) with canonical source SHA-256 provenance hashes |
| Domain Glossary | Created `data/semantic/canonical_glossary.json` (20 campus codes, 7 grade boundaries, fee categories, typo mappings, metrics) |
| Automated Validation | `_draft/validate_packet.py` executed cleanly (exit code 0) verifying JSON structure, 6-table scope, 0 excluded tables, and synthetic example safety |
| Evidence Promotion | Promoted verification report to `docs/07-evidence/contract_semantic_v1_verification.md` |

Connection note: the successful Antigravity session used a local-only Windows Integrated connection with encryption disabled. This is not an approved remote or production connection pattern and must not be copied into deployed configuration.

## Milestones

| # | Milestone | Target date | Status |
|---|---|---|---|
| M1 | Schema analysis complete | 2026-08-02 | Done |
| M2 | Scratch-table verification | 2026-08-02 | Done |
| M3 | Meeting notes prepared | 2026-08-02 | Done |
| M4 | Semantic relationship map created | 2026-08-02 | Done |
| M5 | Canonical column reference created | 2026-08-02 | Done |
| M6 | Master schema definition finalized | 2026-08-02 | Done |
| M7 | Canonical view exports reconciled to captured live catalog evidence | 2026-08-03 | Done |
| M8 | Gold prompt set aligned and evaluated (at least 200) | 2026-08-14 | Partial: 610 routed/planned; answer truth pending |
| M9 | Wren AI MDL and local RAG integrated | 2026-08-07 | Partial: 16-model single-object MDL; cross-table contracts pending |
| M10 | AutoGluon/TabPFN/MLflow adaptive prediction pipeline | 2026-08-12 | Pending |
| M11 | Security evidence and final demo package | 2026-08-18 | Pending |

## Action Items

- [x] Reconcile the canonical exports with captured live `sys.views` evidence.
- [x] Remove duplicate/obsolete view headers from the canonical exports.
- [x] Create semantic relationship map.
- [x] Create canonical column reference.
- [ ] Confirm school-name codes with the client/domain owner.
- [x] Clarify `ALL_COMBINED_FINAL` and `SUBJECT_MARKS_EXAM_RUNTIME` lifecycle.
- [x] Produce and verify explicit candidate-versus-live set and definition-hash CSVs: 68/68 matches, zero differences.

## Active Risks

| # | Risk | Status/impact | Mitigation |
|---|---|---|---|
| R1 | No foreign keys exist in the database | Semantic joins cannot be inferred automatically | Maintain the approved relationship map and gold-query validation |
| R2 | Inconsistent physical names and legacy definition headers | Can mislead regex-based discovery | Use `sys.views` schema/name as identity; use definitions only for SQL bodies |
| R3 | Codex cannot independently repeat the live connection under its current SSPI context | Live result currently depends on retained Antigravity evidence | Preserve sanitized evidence; repeat through the approved execution identity when required |
| R4 | Candidate-versus-live definition proof was previously missing | Resolved: the retained 68-row set and definition-hash CSVs independently reconstruct the 68/68 result | Preserve the accepted evidence package and rerun after live view changes |
| R5 | `School_Ind_Pos_SUB` contradicts the student-position prompt description | Forty prompts cannot be answered from the named live view | Obtain the correct student/subject merit source from Daanish School |
| R6 | Internal total and broad performance views are not production-safe | `STRING_AGG` overflow and five-to-twelve-second broad scans | Fix/materialize/index the institutional views, then repeat concurrent acceptance |

## Evidence and Files

- Canonical exports: `docs/06-schema/database_views_export.sql`, `docs/06-schema/database_views_export_live.sql`
- Reconciliation evidence: `docs/07-evidence/sql-view-reconciliation/`
- Schema authority: `docs/06-schema/master_schema.md`
- Relationships: `docs/06-schema/semantic_relationship_map.json`
- Vocabulary: `docs/06-schema/canonical_column_reference.md`
- Change history: `docs/06-schema/system_changelog.md`
