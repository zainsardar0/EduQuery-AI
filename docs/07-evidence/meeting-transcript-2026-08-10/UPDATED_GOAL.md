# EduQuery AI Updated Goal — Pending Meeting Validation

> **Status:** `NOT_YET_ESTABLISHED`
> **Reason:** The meeting transcript and evidence-linked requirements delta are not yet complete.
> **Effect:** No current scope, schedule, architecture, schema, ownership or workstream status is changed by this file.

## Current Controlled Goal

Until the meeting evidence passes the gates below, the controlled goal remains:

> Deliver the first deployable EduQuery AI institutional release for the August 20, 2026 board demonstration: an English-only Next.js/FastAPI/Wren AI MVP for governed natural-language academic analytics and advisory student-risk prediction, with protected data and services kept inside the institution, a read-only and role/campus-scoped query boundary, a governed semantic layer, at least 200 evaluated gold prompts, leakage-safe model comparison, MLflow/SHAP evidence, security validation, a final report and a tested demonstration fallback.

This is a synthesis of the current approved baseline, not a meeting-derived update: [`WORKFORCE_PLAN.md`, “Delivery Definition” and “Locked August 20 Scope” (lines 3–47)](../../docs/05-planning/WORKFORCE_PLAN.md#delivery-definition), [`PROJECT_CONTROL.md`, “At a Glance” and “Eight Workstreams” (lines 7–44)](../../docs/00-control/PROJECT_CONTROL.md#at-a-glance), and [`ARCHITECTURE.md`, “Architectural Style” and “Security and Scale Baseline” (lines 3–52)](../../docs/05-planning/codebase/ARCHITECTURE.md#1-architectural-style).

## Updated Goal

**Pending.** No updated-goal wording may be drafted as fact until all mandatory gates pass. Meeting requests may become proposed changes in `REQUIREMENTS_DELTA.md`, but they do not become the controlled goal through transcription alone.

Working institutional spelling in this draft is **Daanish School**, as supplied by Muhammad Junaid. This naming input does not itself establish a project requirement or authorize silent edits to current canonical documents.

## Mandatory Validation Gates

| Gate | Pass condition | Current state |
|---|---|---|
| G-01 Source integrity and coverage | `source-manifest.json` records the source hash, media properties and processing settings; transcript coverage accounts for every interval from `00:00.000` to `16:44.299`. | `PENDING` |
| G-02 Independent transcription evidence | OpenAI diarization/lexical results and Google `chirp_3` results exist or a provider failure is documented without substituting guessed text. | `PENDING` |
| G-03 Language fidelity | Urdu is preserved in Urdu script, Roman Urdu is derived only after source review, spoken English is preserved, and no Hindi/Devanagari normalization or translation is introduced. | `PENDING` |
| G-04 Speaker integrity | Every turn retains an anonymous label; a verified name appears only after audible self-identification. The attendee roster is never used as proof by elimination. | `PENDING` |
| G-05 Critical-claim QA | Names, numbers, dates, percentages, negations, roles, deadlines, scope, approvals and technical commitments are replayed and every disagreement is marked `NEEDS_REVIEW` or `UNRESOLVED`. | `PENDING` |
| G-06 Atomic requirements extraction | Every candidate statement has a `REQ-*` row, exact transcript turn/timestamp evidence, one allowed classification, a speaker/QA status and no reconstructed content. | `PENDING` |
| G-07 Baseline reconciliation | Each requirement row maps to a baseline ID and canonical anchor, or records `NONE_FOUND`; impact, dependencies, acceptance evidence and affected workstreams are explicit. | `PENDING` |
| G-08 Conflict and authority review | Awais's statements remain stakeholder expectations unless decision authority is explicit. Conflicts and proposed scope changes remain unresolved until Muhammad Junaid reviews them. | `PENDING` |
| G-09 Human validation | Muhammad Junaid validates all critical commitments, every `NEEDS_REVIEW`/`UNRESOLVED` segment, conflicts, and every `ADDS`/`MODIFIES`/`SUPERSEDES`/`DEFERS` row. | `PENDING` |
| G-10 Canonical change authorization | Approved changes identify the exact canonical documents, workstream rows and acceptance evidence to update in a separate controlled work packet. | `PENDING` |

## Required Approval Record

The updated goal can be finalized only after this record is completed by Muhammad Junaid.

| Decision | Required entry |
|---|---|
| Transcript accepted | `PENDING` |
| Critical/uncertain segments resolved | `PENDING` |
| Accepted requirement row IDs | `PENDING` |
| Rejected/deferred requirement row IDs | `PENDING` |
| Resolved conflicts and rationale | `PENDING` |
| Approved updated-goal wording | `PENDING` |
| Approval date | `PENDING` |

After approval, canonical changes must still follow the source-of-truth and evidence rules in [`DOCUMENTS.md`](../../DOCUMENTS.md#source-of-truth-order) and the handoff/control rules in [`PROJECT_CONTROL.md`](../../docs/00-control/PROJECT_CONTROL.md#mandatory-team-and-agent-workflow). Accepted, sanitized evidence may then move from `_draft/` to `docs/07-evidence/`; the raw recording must remain untracked and outside Git, RAG and accepted evidence.
