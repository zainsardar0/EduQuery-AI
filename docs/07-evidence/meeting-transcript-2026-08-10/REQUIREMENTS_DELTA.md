# Daanish School Meeting — Requirements Delta

> **Status:** `PENDING_TRANSCRIPTION`
> **Authority:** Draft analysis only; this file does not change the approved EduQuery AI scope.
> **Source recording:** `Project requirements outline and Discussion .mp4`
> **Required coverage:** `00:00.000–16:44.299`

No meeting-derived requirement has been entered yet. The recording must first be transcribed, reconciled and validated. Until then, every current baseline below remains in force.

## Input Controls

- Working institutional spelling: **Daanish School**, supplied by Muhammad Junaid for this task. Current canonical documents still contain “Danish School Board”; this draft does not alter them.
- Contextual attendee roster supplied for this task: Muhammad Junaid, Abdur Rafay (Rafay), Abeera, Ali Imran, and Awais (Daanish School representative).
- The roster is not a speaker map. A name may be attached to a transcript turn only after audible self-identification; otherwise the turn remains anonymous.
- Awais's statements are stakeholder expectations unless the recording explicitly establishes decision authority. They do not supersede approved project decisions without Muhammad Junaid's validation.

## Canonical Current-State Baseline

The source order is controlled by [`DOCUMENTS.md`, “Source-of-Truth Order” (lines 23–35)](../../DOCUMENTS.md#source-of-truth-order). Repository/test evidence governs implementation claims; user-confirmed status stays labelled as such.

| Baseline ID | Current controlled state | Evidence class | Exact canonical anchor |
|---|---|---|---|
| B-01 | The August 20, 2026 release is an English-only working institutional MVP and board demonstration. | Approved scope and locked deadline | [`PROJECT_CONTROL.md`, “At a Glance” (lines 7–18)](../../docs/00-control/PROJECT_CONTROL.md#at-a-glance); [`WORKFORCE_PLAN.md`, “Locked August 20 Scope” (lines 28–47)](../../docs/05-planning/WORKFORCE_PLAN.md#locked-august-20-scope) |
| B-02 | The product provides governed natural-language academic analytics plus advisory student-risk prediction and explainability. It does not replace academic authority. | Approved product goal | [`EduQuery_AI_Brief.md`, “Executive Overview” (lines 14–22)](../../docs/02-brief/EduQuery_AI_Brief.md#executive-overview); [`EduQuery_AI_Brief.md`, “Explainability” (lines 95–99)](../../docs/02-brief/EduQuery_AI_Brief.md#43-explainability) |
| B-03 | Vercel hosts only the Next.js browser interface/static assets. FastAPI, Wren AI, local RAG, SQL Server access, prediction, MLflow, SHAP and audit services stay inside the institution and are reached through an institution-approved HTTPS/VPN path. | Approved architecture and deployment decision | [`ARCHITECTURE.md`, “Architectural Style” and “System Flow” (lines 3–31)](../../docs/05-planning/codebase/ARCHITECTURE.md#1-architectural-style); [`EduQuery_AI_Brief.md`, “Deployment Sovereignty” (lines 112–116)](../../docs/02-brief/EduQuery_AI_Brief.md#52-deployment-sovereignty) |
| B-04 | Protected prompts, student identities, roll numbers, row-level records, marks, results and prediction payloads remain inside the institution. Local RAG contains only approved schema, glossary, metrics, MDL and verified examples. | Approved non-negotiable privacy boundary | [`WORKFORCE_PLAN.md`, “Must ship,” items 4–5 (lines 34–36)](../../docs/05-planning/WORKFORCE_PLAN.md#must-ship); [`ARCHITECTURE.md`, “Security and Scale Baseline” (lines 43–52)](../../docs/05-planning/codebase/ARCHITECTURE.md#4-security-and-scale-baseline) |
| B-05 | Database access is least-privilege and read-only, with server-side authentication, role/campus authorization, allowlisting, SELECT-only validation, parameterization, row/time limits, RLS verification, redacted audit events and fail-closed behavior. | Approved security baseline; implementation evidence still required | [`WORKFORCE_PLAN.md`, “Must ship,” item 9 (line 40)](../../docs/05-planning/WORKFORCE_PLAN.md#must-ship); [`PROJECT_CONTROL.md`, WS-03 (line 39)](../../docs/00-control/PROJECT_CONTROL.md#eight-workstreams) |
| B-06 | External model assistance is `openai/gpt-5.6-luna-pro` through OpenRouter and receives de-identified intent/schema context only after local redaction/tokenization. Zero-retention and no-collection routing controls are mandatory. | Approved model/provider decision and privacy gate | [`WORKFORCE_PLAN.md`, “Confirmed Decisions and Evidence State” (lines 49–60)](../../docs/05-planning/WORKFORCE_PLAN.md#confirmed-decisions-and-evidence-state); [`WORKFORCE_PLAN.md`, “Decision Gates,” item 1 (line 105)](../../docs/05-planning/WORKFORCE_PLAN.md#decision-gates) |
| B-07 | The governed semantic scope is defined by 35 included tables, 26 excluded tables, 68 views and 2 procedures; excluded objects cannot enter NLP training, semantic-layer or gold-prompt material. The accepted view audit reports 68/68 candidate-versus-live definition matches and zero mismatches. | Live/schema evidence verified August 2–3, 2026 | [`master_schema.md`, inventory (lines 1–17)](../../docs/06-schema/master_schema.md#eduquery-ai--master-schema-definition); [`master_schema.md`, “Excluded Tables” (lines 113–142)](../../docs/06-schema/master_schema.md#excluded-tables-26--not-part-of-ai-training) |
| B-08 | The semantic layer must use the approved schema glossary, metric definitions, relationships and Wren AI MDL; at least 200 versioned gold prompts require expected answers, execution/evaluation results and human validation. | Approved release requirement; delivery evidence pending | [`WORKFORCE_PLAN.md`, “Must ship,” items 3 and 6 (lines 34–37)](../../docs/05-planning/WORKFORCE_PLAN.md#must-ship); [`master_schema.md`, “Additional Requirements” (lines 198–205)](../../docs/06-schema/master_schema.md#additional-requirements-for-schema-completeness) |
| B-09 | Prediction evaluation must use a leakage-safe temporal split and compare a historical-average baseline with AutoGluon and TabPFN candidates; selected results are tracked in MLflow and representative SHAP explanations are produced. No unmeasured accuracy claim is permitted. | Approved release requirement; model evidence pending | [`WORKFORCE_PLAN.md`, “Must ship,” items 7–8 (lines 38–39)](../../docs/05-planning/WORKFORCE_PLAN.md#must-ship); [`WORKFORCE_PLAN.md`, “Decision Gates,” item 4 (line 108)](../../docs/05-planning/WORKFORCE_PLAN.md#decision-gates) |
| B-10 | Human ownership remains with Muhammad Junaid (product/NL2SQL/semantic approval), M. Zain ul Abideen (prediction), Abdur Rafay (backend/security/deployment reliability) and Abeera Anwer (frontend/UX). AI agents augment rather than replace them. | Approved ownership model | [`WORKFORCE_PLAN.md`, “Human Team” (lines 7–18)](../../docs/05-planning/WORKFORCE_PLAN.md#human-team) |
| B-11 | Current recorded state: WS-01 and WS-02 are `DONE`; WS-03 is `NEXT`; WS-04 and WS-06 are `WAITING`; WS-05, WS-07 and WS-08 are `NOT STARTED`. | Operational status as last reconciled August 3, 2026 | [`PROJECT_CONTROL.md`, “Eight Workstreams” (lines 33–44)](../../docs/00-control/PROJECT_CONTROL.md#eight-workstreams) |
| B-12 | The frontend is ready by team confirmation but remains outside this backend-first workspace; repository integration waits for stable backend contracts. | User-confirmed state, not repository-verified implementation | [`PROJECT_CONTROL.md`, WS-06 (line 42)](../../docs/00-control/PROJECT_CONTROL.md#eight-workstreams); [`ARCHITECTURE.md`, “Architectural Style” (lines 3–8)](../../docs/05-planning/codebase/ARCHITECTURE.md#1-architectural-style) |
| B-13 | Urdu/multilingual product support is post-demo scope, beginning only after the English MVP is accepted. This does not affect the requirement to transcribe this meeting accurately in Urdu and English. | Approved product sequencing | [`WORKFORCE_PLAN.md`, “Post-demo roadmap” (lines 43–47)](../../docs/05-planning/WORKFORCE_PLAN.md#post-demo-roadmap); [`EduQuery_AI_Brief.md`, roadmap note (line 130)](../../docs/02-brief/EduQuery_AI_Brief.md#61-product-roadmap) |

## Delta Classification Contract

Exactly one classification must be assigned to every candidate statement after transcription.

| Classification | Use only when |
|---|---|
| `CONFIRMS` | The statement repeats a current baseline without changing meaning, scope, priority, owner, deadline or acceptance evidence. |
| `CLARIFIES` | The statement removes ambiguity while preserving the current baseline. |
| `ADDS` | The statement introduces a new required outcome, constraint, actor, interface, deliverable or acceptance condition not present in the baseline. |
| `MODIFIES` | The statement changes part of an existing baseline while leaving the baseline item in force. |
| `SUPERSEDES` | The statement explicitly replaces an existing baseline item in full. |
| `DEFERS` | The statement explicitly moves an existing committed item to a later phase or unresolved future date. |
| `CONFLICTS` | The statement cannot coexist with one or more current baseline items and no explicit, authorized resolution is present. |
| `OPEN_DECISION` | The recording raises a material choice or request but does not resolve or authorize it. |
| `NON_REQUIREMENT` | The statement is context, discussion, opinion, example or social speech and imposes no project obligation. |

Classification describes the relationship to the baseline; it is not approval. `ADDS`, `MODIFIES`, `SUPERSEDES` and `DEFERS` remain proposals until Muhammad Junaid validates them.

## Evidence-Linked Delta Row Schema

| Field | Required value and rule |
|---|---|
| `delta_id` | Stable sequential identifier: `REQ-001`, `REQ-002`, and so on. Never reuse an ID. |
| `classification` | Exactly one value from the classification contract above. |
| `atomic_statement` | One requirement or non-requirement only; split compound statements into separate rows. Preserve negation, quantities, dates and conditions. |
| `evidence_turn_ids` | One or more exact `turn_id` values from `transcript-segments.json`. No row may exist without a transcript join. |
| `timestamp_range` | Earliest start to latest end across the cited turns, using `HH:MM:SS.mmm`. |
| `anonymous_speaker` | Exact diarization label from the transcript. |
| `verified_name` | Name only after audible self-identification; otherwise `UNVERIFIED`. |
| `speaker_status` | `SELF_IDENTIFIED` or `ANONYMOUS`. Context or elimination is not identification. |
| `qa_status` | `VERIFIED`, `NEEDS_REVIEW` or `UNRESOLVED`, matching the cited transcript evidence. |
| `current_baseline` | Relevant baseline ID(s), or `NONE_FOUND` after checking all canonical sources. |
| `canonical_anchor` | Relative link plus exact section/row and current line range. Use `N/A` only for `NONE_FOUND`. |
| `affected_workstream` | `WS-01` through `WS-08`, or `NONE` for a true non-requirement. Multiple IDs are allowed when justified. |
| `implementation_impact` | Concrete behavior, contract, data, UI, security, deployment, documentation or schedule impact. Use `PENDING_ANALYSIS` until evidence is clear. |
| `dependencies` | Named prior decision, access, contract or workstream dependency; `NONE_IDENTIFIED` is allowed only after analysis. |
| `acceptance_evidence` | Reproducible proof required to accept the change; never “code exists” or an agent claim. |
| `approval_status` | `PENDING_JUNAID_VALIDATION`, `APPROVED`, `REJECTED`, `DEFERRED` or `NOT_APPLICABLE`. Default is `PENDING_JUNAID_VALIDATION`; use `NOT_APPLICABLE` only with `NON_REQUIREMENT`. |
| `uncertainty_note` | Exact disagreement, inaudibility, overlap or unresolved meaning; `NONE` only for verified evidence. |

## Meeting-Derived Delta Ledger

No rows have been created. This prevents the current project plan, attendee roster or conversational context from being misrepresented as meeting evidence.

| Delta ID | Classification | Atomic statement | Evidence turns / timestamps | Speaker / QA | Baseline / canonical anchor | Workstream | Impact / dependencies | Acceptance evidence | Approval |
|---|---|---|---|---|---|---|---|---|---|

## Reconciliation Rules

1. Account for the full recording from `00:00.000` through `16:44.299`; gaps must be explicit silence, non-speech, inaudible or unresolved intervals.
2. Preserve Urdu source speech in Urdu script, add Roman Urdu only after the source line is fixed, and preserve spoken English without translation or paraphrase.
3. Replay every disagreement involving a name, number, date, percentage, negation, deadline, owner, scope, approval or technical commitment.
4. Never reconstruct inaudible or overlapping speech from context.
5. If a statement conflicts with the baseline, retain both positions and mark `CONFLICTS`; do not choose a winner without explicit approval evidence.
6. No canonical document, workstream status, architecture, schema, ownership assignment or delivery commitment changes from this draft.
