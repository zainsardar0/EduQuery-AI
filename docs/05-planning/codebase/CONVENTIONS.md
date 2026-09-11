# Coding Conventions

## 1) Naming Rules

No coding convention is evidenced because no source exists. Proposed defaults:

| Item | Rule | Example | Evidence |
|---|---|---|---|
| TypeScript files | kebab-case | `query-result-card.tsx` | [TODO] enforce in scaffold |
| React components/types | PascalCase | `QueryResultCard` | [TODO] |
| Python modules/functions | snake_case | `validate_query` | [TODO] |
| Constants/env vars | UPPER_SNAKE_CASE | `SQLSERVER_DSN` | [TODO] |

## 2) Formatting and Linting

- Frontend formatter/linter: [TODO] configure Prettier and ESLint.
- Backend formatter/linter: [TODO] configure Ruff.
- Type checking: [TODO] TypeScript strict mode and Python type checks.
- Run commands: [TODO] created with scaffold.

## 3) Import and Module Conventions

- Imports may point inward to shared contracts and local feature modules; cross-feature internals are not public APIs.
- Frontend aliases: [TODO] define one root alias only.
- Python imports: absolute within service packages.

## 4) Error and Logging Conventions

- API errors use stable machine codes plus safe user messages; raw SQL, connection strings, and stack traces never reach the UI.
- Every query/prediction log includes request ID, actor scope, prompt family, duration, outcome and denial reason, but not raw protected payloads.
- Student names, roll numbers, marks, result rows, contact details, credentials, OTPs, raw prompts, predictions and raw response payloads are omitted or irreversibly tokenized.
- Outbound external-model logging records provider/model, policy flags, request ID, token counts, latency and outcome only. It never records the protected pre-redaction prompt or student-level response.
- Stable safe error codes are shared across the Vercel UI and institutional API; internal connection/provider details remain server-side.

## 5) Testing Conventions

- Python: `test_*.py`; TypeScript: `*.test.ts(x)`; end-to-end specs: `*.spec.ts`.
- External LLM and SQL calls use contract fakes for deterministic CI.
- Gold-prompt tests compare authorized intent, generated/selected query, result shape and final answer—not wording alone.
- ML tests use chronological/temporal partitions, record the baseline and candidate metrics in MLflow, and reproduce the adaptive-selection decision.
- Privacy tests inspect outbound OpenRouter payloads and fail if student identities, row values, results or predictions appear.

## 6) Evidence

- `DOCUMENTS.md`
- `.agents/AGENTS.md`
- `docs/01-proposal/EduQuery_AI_Proposal.md`
