# EduQuery AI Document Guide

This is the only catalog for canonical EduQuery AI documents. It explains what each document does, when to open it and how it must be maintained.

For current progress and next work, open [Project Control](docs/00-control/PROJECT_CONTROL.md). Do not create another document catalog or status tracker.

## Which File Should I Open?

| Question | Open |
|---|---|
| What is done, active, blocked or next? | `docs/00-control/PROJECT_CONTROL.md` |
| What does a file do and which copy is canonical? | `DOCUMENTS.md` |
| What must ship by August 20 and who owns it? | `docs/05-planning/WORKFORCE_PLAN.md` |
| What options does Daanish School have for production deployment choices? | `docs/05-planning/SCHOOL_TECHNOLOGY_CHOICES.md` |
| What architecture and security boundary are approved? | `docs/05-planning/codebase/ARCHITECTURE.md` |
| Which technologies and deployment boundaries are intended? | `docs/05-planning/codebase/STACK.md` |
| Which database objects and relationships are approved? | `docs/06-schema/master_schema.md` and `semantic_relationship_map.json` |
| What schema work changed over time? | `docs/06-schema/timeline_progress.md` and `system_changelog.md` |
| Where is final audit evidence? | `docs/07-evidence/README.md` |
| What was originally submitted? | `docs/01-proposal/` |
| What should leadership or non-technical reviewers read? | `docs/02-brief/` and `docs/03-layman-brief/` |
| What is presented live? | `docs/04-pitch/EduQuery_AI_Pitch_Deck.pptx` |

## Source-of-Truth Order

When documents disagree:

1. Explicit approved human decision.
2. `docs/00-control/PROJECT_CONTROL.md` for current status, active priority, blockers and evidence links.
3. `docs/05-planning/WORKFORCE_PLAN.md` for scope, ownership, schedule, architecture boundary and acceptance gates.
4. Current implementation, tests and accepted evidence for what actually works.
5. `docs/06-schema/` for governed database/semantic scope and schema history.
6. `docs/01-proposal/` for the submitted vision and institutional commitment.
7. Brief, layman and pitch artifacts for stakeholder communication.

An agent claim without retained evidence is not a completion source.

## Canonical Document Set

| Category | Canonical files | Purpose | Maintenance rule |
|---|---|---|---|
| Project control | `docs/00-control/PROJECT_CONTROL.md` | Shared progress, owners, active work, blockers and next dependencies | Update after verified status changes; keep concise |
| System Memory | `docs/00-control/SYSTEM_MEMORY.md` | Persistent architectural memory, knowledge invariants, and entity registry | Update after major system or architectural changes |
| Proposal | `docs/01-proposal/EduQuery_AI_Proposal.md`, `.html`, `.pdf` | Submitted project case and original architecture | Historical submission set; do not rewrite for later decisions |
| Executive brief | `docs/02-brief/EduQuery_AI_Brief.md`, `.pdf` | Current leadership summary | Edit Markdown first; regenerate PDF after approved revisions |
| Layman brief | `docs/03-layman-brief/EduQuery_AI_Layman_Brief.pdf` | Plain-language explanation | PDF-only canonical copy until revisions require editable source |
| Pitch | `docs/04-pitch/EduQuery_AI_Pitch_Deck.pptx` | Gamma-generated live presentation | Edit in Gamma/PowerPoint; avoid duplicate exports |
| Workforce plan | `docs/05-planning/WORKFORCE_PLAN.md` | August 20 scope, ownership, schedule, gates and AI work packets | Update only after approved scope/ownership/schedule changes |
| Client requirements | `docs/05-planning/DAANISH_SCHOOL_CLIENT_NEEDS_AND_SYSTEM_EXPECTATIONS.md` | Canonical Daanish School system expectations, needs and MVP scope decisions | Keep aligned with client meetings and scope updates |
| School Technology Choices | `docs/05-planning/SCHOOL_TECHNOLOGY_CHOICES.md` | Full menu of production tech choices for Daanish School | Update whenever tech stack decisions or school choices evolve |
| Technical references | `docs/05-planning/codebase/*.md` | Architecture, stack, structure, conventions, integrations, tests and risks | Keep aligned with implementation; `[TODO]` means unimplemented |
| Schema/semantic scope | `docs/06-schema/*` | Approved database scope, relationships, vocabulary and schema history | Verify against live evidence and exclude protected objects |
| Accepted evidence | `docs/07-evidence/*` | Sanitized, replayable completion and audit proof | Final evidence only; index each package |
| Original SQL export | `docs/script.sql` | Historical UTF-16LE database export | Incomplete reference; live catalog evidence has precedence |
| Original Database Backup | `data/original_database/*` | Original copies of full SQLite DB (169 MB) and clean ML features CSV (59k rows) | Reference backup set; read-only |

## Technical Reference Files

| File | Purpose |
|---|---|
| `SCHOOL_TECHNOLOGY_CHOICES.md` | Canonical records of internal MVP choices and school's production alternatives |
| `ARCHITECTURE.md` | System flow, trust boundaries, privacy and scaling baseline |
| `ML_PREDICTION_ARCHITECTURE.md` | Multi-tier ML models, variable registry, Optuna tuning, and empirical accuracy estimates |
| `STACK.md` | Intended technologies, deployment location and configuration requirements |
| `STRUCTURE.md` | Repository/module boundaries and current implementation presence |
| `CONVENTIONS.md` | Coding, configuration, logging and error-handling rules |
| `INTEGRATIONS.md` | SQL Server, Wren AI, OpenRouter, audit and model integrations |
| `TESTING.md` | Unit, contract, security, gold-prompt, ML and end-to-end validation |
| `CONCERNS.md` | Prioritized risks, unresolved dependencies and release concerns |

## Schema Files

| File | Purpose |
|---|---|
| `master_schema.md` | Definitive included/excluded table and view scope for AI work |
| `semantic_relationship_map.json` | Approved implicit joins and synonyms; the database has no reliable FK graph |
| `semantic_model.json` | Partial six-table mapping; not the final Wren AI MDL |
| `canonical_column_reference.md` | Approved vocabulary and physical-name normalization |
| `database_views_export.sql` | Canonical 68-view export |
| `database_views_export_live.sql` | Byte-identical verified live export copy |
| `timeline_progress.md` | Schema/data progress and current schema risks |
| `system_changelog.md` | Detailed schema-system change history |
| `meeting_notes_2026-08-02.md` | Source meeting notes and resolved schema questions |
| `future_db_changes.md` | Deferred optional database improvements |

## Accepted Evidence

`docs/07-evidence/wren-demo-readiness-2026-08-15/` records the sanitized Wren live-database, strict-MDL, privacy, packaging, test, stress and browser-demo gates. Its verdict is local-demo ready, not institutional-production ready.

`docs/07-evidence/wren-gold-610-2026-08-16/` records the sanitized 610-prompt input integrity, live schema reconciliation, 16-model strict Wren expansion, external-off planning/refusal results, live execution sweep, regression result and unresolved answer-accuracy/production gates.

`docs/07-evidence/sql-view-reconciliation/` proves:

- 68 live catalog views and 68 candidate views.
- 68 distinct schema-qualified names.
- 68/68 normalized definition hash matches.
- Zero live-only, candidate-only, duplicate, null/encrypted or mismatched definitions.
- Canonical export SHA-256: `93b40692d521d655d8e70b5cfeaa1935d839864a85473179df3bc443f342e21c`.
- Read-only audit with no database mutation.

The local `Encrypt=False` connection was a localhost-only diagnostic exception and is not an approved deployment pattern.

## Implementation Boundaries

- `apps/web/`
- `services/api/` (WS-03 Secure Backend — FastAPI, auth, SQL AST validator, PII privacy gate, audit logger)
- `services/query/` (WS-04 Wren AI & RAG)
- `services/prediction/` (WS-05 Optuna-tuned LightGBM/CatBoost/HistGBM tournament with TreeSHAP)
- `packages/contracts/` (API Contracts — Pydantic models, JSON Schemas, TypeScript .d.ts)
