# Codebase Concerns

## 1) Top Risks

| Severity | Concern | Evidence | Impact | Action |
|---|---|---|---|---|
| Critical | Backend, semantic runtime, ML pipeline and tests are not verified 17 days before presentation | Workspace scan and `DOCUMENTS.md` | Delivery failure | Execute the parallel Aug 3-18 critical path; no optional scope additions |
| High | A local read-only SQL audit succeeded, but the production encrypted service identity and connection route are not configured | Accepted reconciliation evidence versus deployment requirements | Live NL2SQL deployment can stall or copy an unsafe diagnostic pattern | Obtain institution-approved encrypted connection, least-privilege identity and RLS/campus scope; keep sanitized fallback |
| Medium | Frontend integration is intentionally deferred until backend completion | Approved sequencing decision | Late API-contract drift could compress integration time | Freeze/version backend contracts before handoff and reserve Aug 10-14 for integration |
| High | Proposal and pitch deck promise different stacks/scopes | enhanced proposal vs pitch deck | Rework and credibility risk | Adopt one executable MVP contract |
| Critical | Security and scale claims are unimplemented | proposal risk/security/architecture sections | Real student privacy, institutional trust and deployment risk | Treat auth, authorization, query controls, PII isolation, audit, observability and deployment engineering as release work |
| Critical | Full proposal deliverables, including 200 prompts and advanced ML evidence, are locked for August 20 | Approved scope versus remaining time | Superficial or unfinished evidence | Parallel ownership, daily acceptance gates and August 18 freeze |
| Critical | External OpenRouter processing can violate the institutional data boundary | Approved provider plus data-sovereignty constraint | Student-data disclosure | Local redaction/tokenization, semantic-only RAG, provider routing controls and fail-closed privacy tests |
| High | Vercel frontend can accidentally process/log protected prompts through Server Actions, API routes or analytics | Approved split deployment | Data leaves institutional control | Browser-to-institution API path; prohibit protected server-side Vercel handling and logging |
| Medium | Market/research claims are not source-linked precisely | proposal sections 2, 9, 15 | Presentation challenge risk | Verify or remove unsupported headline claims |

## 2) Technical Debt

| Debt | Why | Where | Risk | Fix |
|---|---|---|---|---|
| Runtime architecture is not implemented | Contracts and tracked module boundaries exist, but no executable service exists | `services/`, `apps/`, `infra/` boundary READMEs | False sense of readiness from folder presence | Implement and prove one secure vertical slice first |
| Partial semantic model only | Six-table JSON mapping is not final Wren MDL | `docs/06-schema` | Incorrect SQL | Build and validate the Wren MDL against the approved master scope |
| No release/deployment/test tooling | Greenfield | scan | Demo instability | Add from day one |
| Multiple conflicting deliverable narratives | Documents evolved separately | proposal/pitch/brief | Board confusion | Publish one MVP definition |

## 3) Security Concerns

| Risk | OWASP | Current mitigation | Gap |
|---|---|---|---|
| Arbitrary or mutating SQL | A03 Injection | Proposal says SELECT-only | No validator or read-only account exists |
| Cross-campus data exposure | A01 Access Control | Proposed RLS/RBAC | No policy/schema/auth implementation |
| PII leakage to LLM/logs | A02/A09 | Approved institutional-only data boundary | Redaction, tokenization, provider-routing and proof tests are not implemented |
| Secret leakage | A02 | None visible | No environment template or secrets process |

## 4) Performance and Scaling

- Performance cannot be measured without code, data volume, indexes, or infrastructure details.
- The pitch deck promises under three seconds; the enhanced proposal allows under five seconds. Use under five seconds as the MVP gate and report measured results.
- Avoid loading broad schema/result sets into the LLM; use curated views, limits, and deterministic aggregates.

## 5) Fragile/High-Churn Areas

- Repository control and document structure changed substantially during setup.
- There is no production-code churn signal yet because runtime implementation has not started.

## 6) Remaining Inputs and Verification

1. [TODO] Publish stable backend contracts and trigger the planned frontend integration handoff after backend completion.
2. [TODO] Provision and verify the institution-approved encrypted SQL service connection, least-privilege identity and RLS/campus scope. Do not copy the localhost `Encrypt=False` diagnostic exception into deployment.
3. [TODO] Confirm the institution-approved authentication provider, RLS implementation and HTTPS/VPN gateway.
4. [TODO] Name the reviewers who will approve metric definitions and at least 200 expected answers.
5. [TODO] Confirm presentation internet/network conditions and the fallback operating mode.
6. [TODO] Verify exact dependency versions and licenses from manifests/lockfiles during implementation.

## 7) Evidence

- `DOCUMENTS.md`
- `docs/01-proposal/EduQuery_AI_Proposal.md`
- `docs/04-pitch/EduQuery_AI_Pitch_Deck.pptx`
- `docs/03-layman-brief/EduQuery_AI_Layman_Brief.pdf`
