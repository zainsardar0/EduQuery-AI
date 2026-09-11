# External Integrations

## 1) Integration Inventory

No integration is verified in this workspace today. Database access, sanitized data and frontend readiness are user-confirmed; implementation evidence remains required.

| System | Type | Purpose | Auth model | Criticality | Evidence |
|---|---|---|---|---|---|
| `db_aadc11_sqldaanish` | Institutional SQL Server | Authoritative academic data | Least-privilege read-only identity plus RLS/campus scope | Critical | Local read-only schema/view audit verified; production encrypted connection, RLS and service identity remain pending |
| Sanitized fallback | Institutional/local dataset | Deterministic demo and failure recovery | Local filesystem/service authorization | Critical | User-confirmed available |
| Wren AI | Institution-hosted service | Semantic model/MDL and NL2SQL orchestration | Private service identity | Critical | Locked deliverable; not implemented |
| Local RAG store | Institution-hosted store | Schema glossary, metrics, MDL and approved examples | Backend-only access | Critical | Approved architecture; not implemented |
| OpenRouter / `openai/gpt-5.6-luna-pro` | External API | De-identified intent assistance | Institutional backend API key | High | Approved provider/model; privacy adapter pending |
| Vercel | External frontend host | Next.js UI/static assets only | Deployment identity; user auth is institution-controlled | High | Approved deployment; not implemented |
| Audit store | Institution-hosted database/log | Accountability without protected payload logging | Append-only service identity | High | Required; not implemented |
| MLflow/artifact store | Institution-hosted service/store | Experiment/model tracking and prediction loading | Backend/ML service identity | High | Required; not implemented |

## 2) Data Stores

| Store | Role | Access layer | Key risk | Evidence |
|---|---|---|---|---|
| SQL Server | Authoritative academic data | [TODO] query adapter | Current local `sqlcmd` attempt fails during encryption/SSPI connection setup | schema timeline and August 3 check |
| Sanitized demo store | Board-demo fallback | [TODO] same query contract | Must preserve representative relationships without PII | delivery constraint |
| Audit store | Append-only access metadata | [TODO] API service | Accidental logging of PII/prompts | proposal |
| Local RAG store | Approved semantic knowledge only | [TODO] query service | Raw student rows or protected prompts entering embeddings/context | approved privacy boundary |
| MLflow/artifact store | Versioned experiment and model evidence | [TODO] prediction service | Uncontrolled artifact access or non-reproducible model selection | locked deliverable |

## 3) Secrets and Credentials

- Credential sources: [TODO] `.env.example` and secret-handling policy do not exist in this workspace.
- Hardcoding check: no application code exists; no committed credentials detected in visible proposal files.
- Rotation/lifecycle: institution policy and named account owners remain required implementation inputs.
- OpenRouter secrets must never be delivered to the browser or stored in Vercel client configuration.

## 4) Reliability and Failure Behavior

- Retries/backoff: [TODO].
- Timeouts: [TODO].
- Fallback: sanitized local demo data is required for the August 20 presentation.
- LLM failure: supported prompt families must have deterministic/template fallback for the demo path.
- Privacy failure: if local redaction cannot prove removal of student identities/records, the external-model call is blocked.
- Institutional API failure: the UI switches to the sanitized deterministic fallback and clearly labels the mode.

## 5) Observability

- External-call logging: [TODO].
- Metrics/tracing: [TODO].
- Minimum demo metrics: latency, query/prediction success, validation denials, fallback use.

## 6) OpenRouter Privacy Contract

1. FastAPI receives the authenticated request inside the institutional boundary.
2. Local logic removes or tokenizes student names, roll numbers and row-level values.
3. Local RAG supplies only approved schema, metrics, MDL and verified examples.
4. OpenRouter receives only de-identified intent/schema context with zero-retention and data-collection-deny routing enabled.
5. SQL completion, authorization, parameter injection, execution and response composition happen locally.
6. No student query result, prediction payload or protected audit content is returned to OpenRouter.

## 7) Evidence

- `docs/01-proposal/EduQuery_AI_Proposal.md`
- `DOCUMENTS.md`
