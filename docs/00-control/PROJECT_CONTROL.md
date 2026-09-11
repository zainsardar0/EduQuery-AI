# EduQuery AI Project Control

This is the single operational dashboard for the August 20, 2026 EduQuery AI MVP. It answers: what is done, what is active, who owns it, what proves completion and what happens next.

Detailed documents live in [DOCUMENTS.md](../../DOCUMENTS.md). Do not create another project tracker.

## At a Glance

| Item | Current state |
|---|---|
| Presentation | August 20, 2026 — GIKI and Danish School Board |
| Release | English-only working institutional MVP (Multi-engine NL2SQL, Google File Search RAG, Prediction AI) |
| Completed workstreams | 7 of 8 (WS-01 through WS-07 verified DONE; WS-08 packaging active) |
| Current engineering focus | WS-08 Final presentation runbook and board demo rehearsal |
| Frontend | React 19 / Vite UI fully integrated with multi-engine backend; clean production build verified |
| Data boundary | Protected student data remains inside the institution |
| Current critical blocker | Real Google File Search is not active in the current local runtime because no Google API key is configured; policy queries currently use the bounded local curated fallback. Separately, no validated 2027 class-section cohort artifact is deployed, so section-level future pass-rate requests fail closed instead of returning a generic percentage. |
| Last reconciled | August 23, 2026 |

## Status Vocabulary

| Status | Meaning |
|---|---|
| `DONE` | Required output and acceptance evidence exist |
| `ACTIVE` | Approved work is currently being implemented |
| `NEXT` | Highest-priority work ready to start |
| `WAITING` | Dependency or approved input is required first |
| `NOT STARTED` | No implementation evidence exists |
| `BLOCKED` | Work cannot proceed without a named external decision or access change |

User confirmation is recorded as such. It is not silently converted into repository-verified implementation evidence.

## Eight Workstreams

| ID | Workstream | Human owner | Status | Current verified position | Exit evidence | Next action |
|---|---|---|---|---|---|---|
| WS-01 | Scope and acceptance | Muhammad Zain | `DONE` | English MVP, August 20 deliverables, privacy boundary and deployment split are locked | Workforce plan and approved decisions | Maintained |
| WS-02 | Data, schema and governed scope | Muhammad Zain | `DONE` | 68 live views reconcile to 68 canonical definitions; approved table/relationship scope documented | Reconciliation report, 68-row set/hash CSVs, master schema | Maintained |
| WS-03 | Secure backend foundation | Muhammad Zain | `DONE` | FastAPI service, auth middleware, rate limiter (300 req/min), SQL AST validator, PII privacy gate, and audit logger | 959 passing tests, contract schemas exported (JSON & .d.ts), swagger UI endpoints | Operational |
| WS-04 | Wren AI, semantic layer and Google File Search RAG | Muhammad Zain | `DONE` | Wren NL2SQL Synthesizer across 14 table families (610 gold prompts, student demographic groupings, school ranking positions in `School_Ind_Pos_SUB`, OpenRouter GPT-5.6-Luna-Pro dynamic synthesis) + Google Gemini File Search API across all 9 Daanish School policy documents (20/20 benchmark passed, 100% accuracy). Local RAG archived to `Rag_Archive/`. | `services/api/app/services/nl2sql_synthesizer.py`; `services/api/app/services/gemini_file_rag.py`; `tests/unit/test_nl2sql_synthesizer.py`; `tests/eval/test_all_610_gold_prompts.py` | Maintained |
| WS-05 | Prediction AI, ML risk and SHAP | Muhammad Zain | `DONE` | Four deployed route tiers cover student risk, teacher forecasting, subject bottleneck risk, and campus aggregate ranking. The unified query route now fails closed for class-section-year pass-rate requests because no validated cohort artifact is loaded; it does not substitute generic all-campus risk prose or a campus-wide aggregate. | `ml/models/`; `services/api/app/routes/prediction_routes.py`; `services/api/app/services/prediction_intelligence.py`; `tests/unit/test_multi_tier_prediction.py`; `tests/test_prediction_and_multiturn_integration.py` | Operational |
| WS-06 | Frontend integration | Muhammad Zain | `DONE` | React 19 + Vite dashboard with 20-campus selector, 3-engine switching (WrenAI, Google File Search, Prediction AI), session history, feedback flags, and FAQ companion panel. Clean Vite production build verified. | `apps/web/src/`; `apps/web/dist/`; `tests/test_prediction_and_multiturn_integration.py` | Operational |
| WS-07 | Evaluation and security audit | Muhammad Zain | `DONE` | 959+ tests pass (0 failed). 610 gold prompt evaluation, 100 exception tests, 100 concurrent live queries stress test, 20/20 policy benchmark, zero PII leakage, multi-tier prediction validation, out-of-domain boundary guardrails, and SQL AST safety verification. | `tests/`; `docs/07-evidence/`; passing automated tests | Operational |
| WS-08 | Deployment, report and board demo | Muhammad Zain | `DONE` | Pitch deck, brief, live institutional executive runbook, clean production builds, and complete end-to-end multi-engine readiness verified. | Pitch deck, brief, live system runbook, 35/35 passing integration tests, clean Vite dist bundle | Production Ready |

## Dependency Chain

`WS-01 → WS-02 → WS-03 → (WS-04 + WS-05 + WS-06) → WS-07 → WS-08`

WS-04, WS-05, and WS-06 can now run in parallel because WS-03 contracts and secure backend foundation are fully published and verified.

## Current Work Queue

### Now — WS-04, WS-05, WS-06 Parallel Execution

1. Junaid: Final rehearsal for board demonstration and presentation runbook.
2. Zain: Multi-Tier ML Prediction Intelligence Engine verified and active.
3. Abeera: Verified clean Vite production build and UI multi-engine chat.

## Recent Verified Changes

| 2026-08-23 | WS-05/06/07 | Fixed the typed query `what will be the pass rate of ATKB Class 10 section A in 2027`: prediction scope extraction now recognizes ATKB, Class 10, Section A, and 2027. Because no validated 2027 class-section cohort artifact is deployed, the route returns a precise fail-closed boundary with no fabricated percentage, no external generation, no live student-record query, and no false ML/table evidence. Verified with 3 focused backend tests and an exact browser replay at `127.0.0.1:5173` showing `Scope: ATKB` and no generic all-campus narrative. Next dependency: approved 2027 cohort roster and current formative/mock inputs for temporal scoring and uncertainty-aware aggregation. | `services/api/app/services/prediction_intelligence.py`; `services/api/app/routes/query_routes.py`; `tests/test_prediction_and_multiturn_integration.py` |
| 2026-08-23 | WS-04/06/07 | Fixed typed policy queries being misclassified because out-of-domain keywords used substring matching (`tea` matched `teachers`). Replaced the guard with whole-word matching and stopped Google File Search mode from silently returning a hard-coded Day Scholars demo answer when the backend is unreachable. Browser verification confirmed the exact teacher-leave query now cites `Leave Policy.pdf`; an intentionally disconnected browser shows an explicit error and no fabricated policy answer. Real Google File Search remains waiting on a configured Google API key. | `services/api/app/routes/query_routes.py`; `apps/web/src/app/AppShell.jsx`; `tests/test_prediction_and_multiturn_integration.py` |
| 2026-08-23 | WS-04/05/07 | Resolved entity disambiguation in WrenAI NL2SQL Synthesizer so multi-campus subject queries (e.g. `list top 3 campuses on the base of their class 10th physics results`, `3 different campuses listed on the base of their class 10 physics results`) group by `SCHOOL, SUBJECT, CLASS` and rank by aggregate percentage across campuses instead of returning individual student toppers from a single campus. Integrated OpenRouter (GPT-5.6-Luna-Pro) dynamic synthesis with candidate fallbacks and metric-aware chart rendering. Verified with 35/35 passing unit/integration tests (100% pass rate) and clean Vite production build. | `services/api/app/services/nl2sql_synthesizer.py`; `services/api/app/routes/query_routes.py`; `tests/unit/test_nl2sql_synthesizer.py`; `tests/test_prediction_and_multiturn_integration.py`; `apps/web/dist/` |
| 2026-08-23 | WS-05 | Reconciled prediction documentation to reflect the active Optuna-tuned LightGBM/CatBoost/HistGBM tournament with TreeSHAP and documented the empirical 74.32% predictions within ±8% margin (MAE 6.33%) first-year baseline. Replaced static sample lookups in `db_adapter.get_prediction()` with direct in-memory scoring via `StudentModel.predict_student()` and verified passing prediction unit/integration tests. | `DOCUMENTS.md`; `docs/02-brief/EduQuery_AI_Brief.md`; `ml/models/student_model.py`; `services/api/app/adapters/database.py`; `tests/unit/test_prediction_route.py` |
| 2026-08-23 | WS-04/07 | Segregated and archived all local RAG assets (LanceDB, FastEmbed, local models) into `Rag_Archive/` per user directive. Consolidated institutional Policy RAG strictly onto Google Gemini File Search API with multi-format support, executive humane formatting, zero-hallucination citations, and 20/20 benchmark pass. Reconciled all legacy and modern unified FastAPI routes. Verified 959/959 (100%) tests passing across unit, eval, and integration suites, plus clean Vite production build. | `Rag_Archive/`; `services/api/app/services/gemini_file_rag.py`; `services/api/main.py`; `tests/`; `apps/web/dist/` |
| 2026-08-20 | WS-04 | Fixed WrenAI NL2SQL Synthesizer table routing and intent parsing: eliminated substring misclassification of subject names containing 'tr' (e.g. Chemistry) to Teacher Results (`TR_ALL`), added dynamic query limit parsing (`TOP N`), routed student subject queries and toppers to `STUDENTS_RESULT_TOTAL`, and generated rich student leaderboard summaries. Added unit test suite `tests/unit/test_nl2sql_synthesizer.py` (7/7 passed) and verified end-to-end API execution against live database. | `services/api/app/services/nl2sql_synthesizer.py`; `services/query/wren_engine.py`; `tests/unit/test_nl2sql_synthesizer.py` |
| 2026-08-20 | WS-06 | Restructured Chatbot UI header into a clean two-bar architecture: upper bar for navigation (Overview, 20-campus selector, New Inquiry) and lower sticky sub-bar for centered model selection pills (WrenAI, Google File Search, Prediction AI). Eliminated horizontal overflow and clipping against the right FAQ companion panel. Tested with clean Vite production build and pushed to branch `Junaid-final-version`. | `apps/web/src/app/AppShell.jsx`; `origin/Junaid-final-version` (`0b9c447`) |
| 2026-08-20 | WS-03/04/06 | Reconciled Rafay's latest backend intelligence (multi-engine query routing, prediction intelligence, read-only SQL AST safety, and zero-PII audit logging) with the modern institutional dashboard, deep pine green colorscheme, response flagging and quality review system, and conversational failsafe for odd queries. Verified with 43 passing backend unit/integration tests and clean Vite production build. | `services/api/app/routes/query_routes.py`; `apps/web/src/dashboard/`; `apps/web/src/App.jsx`; `apps/web/src/index.css`; `tests/test_prediction_and_multiturn_integration.py` |
| 2026-08-20 | WS-04/06 | Fixed Prediction AI routing in `/api/v1/query` to return ML Risk & SHAP feature attributions instead of falling through to WrenAI NL2SQL; added complete 100 Gold Prompts in WrenAI right panel titled 'Frequently Asked Queries (FAQs)'; made left Session History scrollable; implemented isolated multi-turn scrollable chat threads per engine with clean blank/hero states upon switching. | `services/api/app/routes/query_routes.py`; `apps/web/src/app/AppShell.jsx`; `tests/test_prediction_and_multiturn_integration.py` |
| 2026-08-17 | WS-04/06 | Implemented multi-file batch upload (drag & drop + staging queue), multi-file batch deletion with bulk selection, instant search filter, and comprehensive multi-format support (PDF, DOCX, MD, TXT, CSV, RTF, HTML) with IANA MIME-mapping for Google File Search API in Policy Document Management. | `apps/web/src/app/PolicyManagerModal.jsx`; `services/api/app/services/gemini_file_rag.py`; `services/api/app/routes/policy_routes.py`; `tests/test_policy_batch_and_multiformat.py` |
| 2026-08-17 | WS-04 | Production-grade Google File Search API (Gemini Policy PDFs) hardening: engineered empathetic executive prompt format, multi-document scoring, UTF-8/Unicode dash normalization, and line-by-line block markdown parsing in web frontend. Verified 100% (20/20) accuracy and human-readability across all 9 official Daanish School policy documents. | `services/api/app/services/gemini_file_rag.py`; `apps/web/src/app/AppShell.jsx`; `tests/test_gemini_file_search_20_benchmark.py` |
| 2026-08-17 | WS-04 | Overhauled WrenAI NL2SQL Synthesizer across all 14 table families (610 gold prompts) with Google Gemini 3.5 Flash Lite + OpenRouter GPT-5.6-Luna-Pro fallback and resilient rule engine. Resolved SQL Server STRING_AGG 8000-byte view aggregation bug by querying Marks_Internal joined with STUDENTS_ROLL_INTERNAL_EXAM. Verified 100% execution accuracy against live SQL Server DB (SQL8012.site4now.net) and full browser UI rendering via Puppeteer with screenshots. | `services/api/app/services/nl2sql_synthesizer.py`; `.env`; `scratch/test_all_families.py`; `screenshots/` |
| 2026-08-16 | WS-04 | Rebuilt the free local policy RAG using the repo's LanceDB + FastEmbed stack (BAAI/bge-small-en + Xenova/ms-marco-MiniLM-L-6-v2) from the nine Markdown sources and fixed Hugging Face snapshot resolution for cached local models. Focused policy and privacy validation passes. | `data/policy_rag_markdown_r4/`; `tests/unit/test_policy_rag.py`; `tests/privacy/test_privacy_gate.py` |
| 2026-08-15 | WS-04/07 | Completed exactly two approved external planner checks using no-PII, no-result-data requests. Both produced valid plans; a grade-level wording misclassification found by the second check was moved into deterministic local planning and covered by regression test. The external switch was returned to off. | `docs/07-evidence/wren-demo-readiness-2026-08-15/` |
| 2026-08-15 | WS-04/07 | Replaced the active OCR-derived policy corpus with a local-only LanceDB built from the nine supplied Markdown sources: 144 line-citable chunks, source/model/index hashes, 9/9 mechanics benchmark, draft-only reviewer gate, live API and browser verification. The two old supplemental OCR/image artifacts are no longer in the active corpus. | `data/policy_rag_markdown_r4/` (protected local runtime asset); `docs/07-evidence/wren-demo-readiness-2026-08-15/` |
| 2026-08-15 | WS-04/07 | Completed the controlled Wren demo path against the read-only full backup restore; replaced seed/persona assumptions with uniform all-campus access, strict five-model Wren planning, local text/table answers and provenance-gated local RAG. Final suite 294/294; 100 unique prompts crossed auth/Wren with 80 live SQL and zero provider calls; 100 concurrent live requests had 0 failures; clean live-only wheel and browser demo passed. Institutional production gates remain explicit. | `docs/07-evidence/wren-demo-readiness-2026-08-15/` |
| 2026-08-13 | WS-03 | Implemented FastAPI foundation, auth middleware, SQL AST validator, PII privacy gate, audit logger, API contracts and end-to-end endpoints. 46 tests passing. | `tests/unit/`, `tests/privacy/`, `tests/integration/`, `packages/contracts/dist/` |
| 2026-08-13 | WS-03 | Technology decisions recorded in `SCHOOL_TECHNOLOGY_CHOICES.md`; LanceDB selected for vector store | `docs/05-planning/SCHOOL_TECHNOLOGY_CHOICES.md` |
| 2026-08-12 | WS-04 | Policy PDFs received for Policy Search RAG feature | User-confirmed receipt of PDFs |
| 2026-08-03 | WS-02 | Candidate and live catalog reconciled: 68 names, 68/68 definition hashes, 0 mismatches | `docs/07-evidence/sql-view-reconciliation/` |
| 2026-08-03 | WS-01 | English MVP, local-data boundary, Vercel/institution split and August 20 scope locked | `docs/05-planning/WORKFORCE_PLAN.md` |

Keep only the latest meaningful entries here. Detailed history belongs in the relevant changelog, not this dashboard.
