# EduQuery AI — Workforce Plan to August 20, 2026

## Delivery Definition

The August 20 deliverable is the first deployable release of a real institutional product: a polished board-demo MVP that proves safe natural-language academic analytics and credible student-risk prediction while establishing the security, scaling, deployment, and governance foundations needed for continued production implementation. The feature surface is narrower than the 12-week proposal; the engineering standard is not disposable-prototype quality.

## Human Team

The four-person project team remains accountable for product and domain decisions. Codex and Antigravity are an AI workforce that augments this team; neither replaces human ownership.

| Team member | Proposal ownership | August 20 accountability | AI support |
|---|---|---|---|
| Muhammad Junaid | Project lead; NL2SQL engine and semantic layer | Product decisions, schema/metric approval, NL2SQL acceptance, stakeholder alignment | Codex planning/query architecture; Antigravity bounded implementation |
| M. Zain ul Abideen | ML prediction pipeline and model engineering | Data profiling, leakage-safe validation, prediction metrics and explanation quality | Codex evaluation design; Antigravity feature/model packet |
| Abdur Rafay | Backend architecture and API development | FastAPI, auth/security integration, database access, deployment reliability | Codex contracts/security tests; Antigravity bounded backend tasks |
| Abeera Anwer | Frontend, visualization and UX | Next.js experience, charts, usability, gold-prompt UX and demo polish | Codex acceptance criteria; Antigravity frontend worktree |

Canonical identity note: Abeera Anwer is the teammate name. “Soban” is a legacy email/account label and must not be used as the contributor name in release documentation.

## Shared Tracking Contract

- `docs/00-control/PROJECT_CONTROL.md` is the only operational dashboard used by the team, Codex, Antigravity and Claude Code.
- `DOCUMENTS.md` is the only canonical document catalog.
- A workstream becomes `DONE` only when its required output and reproducible acceptance evidence exist.
- After every accepted work packet, update the affected Project Control row, evidence, blocker and next dependency using its common handoff format.
- Do not create a parallel tracker, private status document or competing roadmap.

## Locked August 20 Scope

### Must ship

1. Properly working English-only web MVP using Next.js, FastAPI and Wren AI.
2. Proposal-aligned modular architecture with Vercel hosting the browser interface and protected services remaining inside the institution.
3. Governed semantic layer: schema glossary, metric definitions, relationships and Wren AI MDL configuration.
4. Local RAG over approved schema, metrics, MDL and verified examples, plus Policy Search RAG using Headroom vector database for official policy PDFs. Raw or row-level student data is excluded from the retrieval corpus and external context.
5. GPT 5.6 Luna Pro through OpenRouter for de-identified intent assistance only. Local redaction/tokenization must run first; protected prompts, student identifiers, marks, returned rows and prediction payloads cannot leave the institution.
6. At least 200 gold prompts with expected answers, execution/evaluation results and human validation ownership.
7. ML prediction engine using leakage-safe temporal validation, a historical-average baseline, AutoGluon ensemble and TabPFN candidates, with adaptive model selection based on measured evidence.
8. MLflow experiment/model tracking and representative SHAP explainability reports. Predictions remain advisory and require disclaimers.
9. Security evidence: authentication, role/campus authorization, least-privilege read-only database identity, RLS verification, allowlisted semantic surface, SELECT-only SQL AST validation, parameterization, row/time limits, SQL-injection tests, PII-exclusion proof, secret isolation, redacted audit trail and rate limits.
10. Vercel deployment of the frontend integrated via a redirect button on the existing Daanish School portal (initially restricted to admins/principals), secure institutional HTTPS/VPN path to FastAPI, sanitized fallback data, automated critical-path tests, final report, demo runbook and two rehearsals.

### Post-demo roadmap

- Multilingual support, starting with Urdu after the English MVP is accepted.
- Additional institutional roles, richer policy administration and multi-tenant commercial operations beyond the initially approved role/campus model.
- Production-scale monitoring, high-availability operations, WhatsApp alerts and commercial billing.

## Confirmed Decisions and Evidence State

| Item | Current state | Evidence classification |
|---|---|---|
| Database access and sanitized data | Available | User-confirmed; implementation must still prove the connection path |
| Frontend | Ready; will integrate via a redirect button on the existing portal, restricted to existing admin/principal access levels | User-confirmed completion and sequencing decision |
| MVP language | English only | Approved decision; multilingual is future work |
| External model | `openai/gpt-5.6-luna-pro` through OpenRouter | Approved decision |
| Data boundary | Student data remains inside the institution | Approved non-negotiable constraint |
| RAG | Local governed retrieval over semantic documentation, plus Policy Search using Headroom vector database | Approved architecture decision |
| Deployment | Next.js frontend on Vercel; protected backend and intelligence services inside the institution | Approved architecture decision |
| Presentation | GIKI and Danish School Board, August 20, 2026 | Locked deadline |

## Workforce Ownership Split

| Workstream | Human owner | Workforce + Planner (Codex) | Antigravity | Integration rule |
|---|---|---|---|---|
| Scope and acceptance | Junaid + full team | Maintain MVP contract, priorities, gates, risk log | Execute approved packets | Human owner accepts behavior |
| Repository foundation | Rafay + Junaid | Architecture, contracts, CI/test baseline, integration | Consume published contracts | Contracts land before parallel work |
| Data/query safety | Junaid + Rafay | Query architecture, validator/audit/redaction tests | Bounded mappings/fixtures | No direct DB access from UI |
| Frontend | Abeera | Define measurable UX acceptance and integrate contracts | Next.js implementation/polish worktree | Abeera approves UX; mock contract first |
| Prediction | Zain | Evaluation design, leakage checks, API contract | Feature/model packet after data profile | Zain signs off metrics |
| Security/scaling | Rafay + Junaid | Threat model, controls, load/recovery tests, release gate | Implement bounded controls | Security failure blocks release |
| Demo/release | Full team | Critical path, packaging, runbook, narrative consistency | Screenshots/artifacts/polish | Code freeze August 18 |

## Antigravity Work Packets

Antigravity works in isolated Git worktrees/branches. One packet per conversation; no overlapping files.

| Packet | Scope | Inputs | Done when |
|---|---|---|---|
| AG-01 Frontend integration | Connect the existing Next.js interface to versioned FastAPI contracts; add loading, refusal, error and fallback states | Verified frontend location, API schemas and fixture payloads | All fixture states render; protected requests bypass Vercel server processing; typecheck/tests pass |
| AG-02 Secure backend slice | FastAPI orchestration, auth context, validation, redacted audit events and failure handling | Accepted API/security contracts | Authorized prompt and prediction flows pass; unsafe and cross-scope requests fail closed |
| AG-03 Semantic and gold fixtures | Wren MDL, schema glossary, metrics, sanitized fixtures and gold-prompt batches | Approved master schema and relationships | At least 200 prompts have expected answers and recorded evaluation results |
| AG-04 Prediction implementation | Feature transforms, baseline, AutoGluon/TabPFN candidates, MLflow records and SHAP payload | Profiled data and leakage-safe temporal split | Reproducible comparison selects the documented model and returns explanation payloads |
| AG-05 Presentation artifacts | Screenshots, demo capture, architecture/security evidence and runbook polish | Release candidate | Artifacts match actual product behavior and include a tested fallback path |

## Critical Path

| Dates | Exit criteria |
|---|---|
| Aug 3 | Reconcile documents; freeze privacy/deployment/API contracts; complete the 68-view reconciliation; keep frontend integration deferred until backend completion |
| Aug 3-5 | FastAPI foundation, database/sanitized adapters, authentication, authorization, audit events, query validation and one secure end-to-end prompt |
| Aug 4-7 | Wren AI connected to the six-table semantic slice; MDL, schema glossary, metrics, local RAG and OpenRouter redaction adapter operational |
| Aug 4-10 | Gold set built and validated in batches until at least 200 prompts have expected answers and evaluation results |
| Aug 5-10 | Feature profile, temporal split, historical baseline, AutoGluon and TabPFN experiments tracked in MLflow |
| Aug 8-12 | Adaptive model selection, prediction API and representative SHAP explanations integrated |
| Aug 10-14 | Frontend integration/tweaks, Vercel UI deployment, secure institutional API route, English UX and sanitized fallback |
| Aug 12-16 | RLS, SQL-injection, prompt-injection, PII-exclusion, authorization, load, recovery and failure-path evidence completed |
| Aug 16-17 | Final report, semantic documentation, architecture/security package, demo script and critical-defect burn-down |
| Aug 18 | Feature and content freeze; release candidate tagged |
| Aug 19 | Two rehearsals: normal path and failure/fallback path |
| Aug 20 | GIKI and Danish School Board presentation |

## Decision Gates

1. **Privacy gate - before first external call:** prove that local redaction/tokenization removes student identifiers and row-level academic data; enforce OpenRouter zero-retention and data-collection-deny routing. Failure blocks external LLM use.
2. **Backend gate - August 5:** one authenticated, campus-scoped, audited and read-only prompt works through FastAPI against an approved data adapter.
3. **Semantic gate - August 7:** Wren AI and local RAG produce validated results on the governed semantic slice; unsupported requests fail closed.
4. **Prediction gate - August 10:** temporal evaluation and MLflow evidence compare the historical baseline, AutoGluon and TabPFN. No unmeasured accuracy claim is permitted.
5. **Integration gate - August 14:** the Vercel UI reaches the institutional API without routing protected payloads through Vercel server functions.
6. **Release gate - August 18:** no unresolved critical security issue, broken authorization boundary, PII leakage, broken demo/recovery path, missing required artifact or undocumented external dependency.

## Immediate Inputs Needed

1. Backend API contracts and completion gate for the planned frontend integration handoff.
2. Production-safe institutional SQL connection configuration; the local reconciliation session is not a deployment connection pattern.
3. Institution-approved authentication, RLS and secure HTTPS/VPN gateway configuration.
4. OpenRouter credential stored only in the institutional backend and provider-routing configuration enforcing zero retention and no data collection.
5. Domain reviewers and time allocation for validating at least 200 expected answers.
6. Presentation network/environment details and an approved offline fallback path.

## Antigravity Operating Rules

- Use current Antigravity 2.0 project/worktree support; keep access scoped to this repository.
- Start from a written packet and acceptance criteria; return artifacts plus changed-file list and test evidence.
- Never modify the same files as Workforce concurrently.
- No secrets, real student PII, database writes, dependency swaps, or architecture changes without Planner approval.
- Human stream owners review and accept Antigravity output; Antigravity does not become the owner of their domain.
- Temporary generator scripts are deleted after use, per `.agents/AGENTS.md`.
