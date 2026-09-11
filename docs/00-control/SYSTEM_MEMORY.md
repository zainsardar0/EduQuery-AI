# EduQuery AI — System Memory & Persistent Knowledge Layer

## 1. System Identity & Core Contract

- **Project Title**: EduQuery AI: A Prompt-Based Intelligent Analytics and Prediction Engine for Multi-Campus Academic Databases.
- **Client & Institution**: Punjab Daanish Schools and Centres of Excellence Authority (PDS&CEA).
- **Project ID**: `2d56573c-3ab0-43e6-b5ab-3ade1bc171a9`.
- **Human Ownership**:
  - Lead / Repo Owner: Muhammad Junaid (`KSensei99`)
  - Team Members: Abdur Rafay, M. Zain ul Abideen, Abeera Anwer.
- **Governing Rail**: [`AGENTS.md`](file:///c:/Users/marsh/Downloads/The%20OG%20Project/AGENTS.md) and [`.agents/AGENTS.md`](file:///c:/Users/marsh/Downloads/The%20OG%20Project/.agents/AGENTS.md).
- **Single Status Dashboard**: [`docs/00-control/PROJECT_CONTROL.md`](file:///c:/Users/marsh/Downloads/The%20OG%20Project/docs/00-control/PROJECT_CONTROL.md).
- **Single Document Catalog**: [`DOCUMENTS.md`](file:///c:/Users/marsh/Downloads/The%20OG%20Project/DOCUMENTS.md).

---

## 2. Multi-Engine Architecture & Routing Invariants

EduQuery AI consolidates three specialized execution engines behind a unified, rate-limited FastAPI gateway:

```
                      ┌─────────────────────────────────┐
                      │    Unified Web Interface        │
                      │  (React 19 / Vite / Tailwind)   │
                      └────────────────┬────────────────┘
                                       │ HTTP POST /api/v1/query
                      ┌────────────────▼────────────────┐
                      │   FastAPI Gateway Orchestrator  │
                      │  - Rate Limiter (300 req/min)   │
                      │  - AuthMiddleware (RBAC/Campus) │
                      │  - Security Headers (nosniff)   │
                      │  - SQL AST Validator (sqlglot)  │
                      └────────┬───────┼───────┬────────┘
                               │       │       │
            ┌──────────────────┘       │       └──────────────────┐
            ▼                          ▼                          ▼
  ┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐
  │   WrenAI NL2SQL  │       │  Google File RAG │       │  Prediction AI   │
  │  Semantic Layer  │       │  Gemini File API │       │  Risk & SHAP ML  │
  │  - 14 Families   │       │  - 9 Policy Docs │       │  - Drop-out risk │
  │  - 68 Views      │       │  - Multi-format  │       │  - Pass rate     │
  │  - 20 Campuses   │       │  - Top Citations │       │  - Interventions │
  └──────────────────┘       └──────────────────┘       └──────────────────┘
```

### Engine Invariants:
1. **WrenAI NL2SQL (`wren_nl2sql`)**:
   - Routes analytical, roster, attendance, ranking, and exam queries across 14 table families and 20 campuses.
   - Leverages OpenRouter (`openai/gpt-5.6-luna-pro` / `OPENROUTER_API_KEY`) as primary LLM synthesizer with automatic candidate fallbacks and Gemini 3.5 Flash Lite failover.
   - Enforces semantic disambiguation between campus aggregations (e.g. `list top 3 campuses in physics results`) and individual student marks.
   - Generates demographic breakdowns (gender, class, campus) and enforces read-only AST safety via `sqlglot`.
   - Renders metric-aware charts exclusively for true numeric aggregations (excluding raw IDs, roll numbers, and years).
2. **Google File Search RAG (`google_file_search_rag`)**:
   - Primary and sole policy document retrieval pipeline using Google Gemini File API (`gemini-3.1-flash-lite`).
   - Supports multi-format policy ingestion (`PDF`, `DOCX`, `MD`, `TXT`, `CSV`, `RTF`, `HTML`).
   - Generates empathetic, executive answers with explicit document citations (`(Source: <filename>.pdf)`).
3. **Prediction AI (`prediction_ai`)**:
   - Multi-Tier Predictive Intelligence Engine:
     - **Tier 1 (Students)**: Continuous percentage prediction ($\hat{y} \in [0, 100]$), risk classification (`LOW`, `MEDIUM`, `HIGH_RISK_FAIL`), TreeSHAP feature attributions, and non-punitive interventions.
     - **Tier 2 (Teachers)**: Temporal value-added forecasting with tier classifications (`EXEMPLARY`, `PROFICIENT`, `DEVELOPING`, `NEEDS_SUPPORT`).
     - **Tier 3 (Subjects)**: Curriculum transition bottleneck risk & Board alignment gap metrics.
     - **Tier 4 (Campuses)**: Multi-campus reputation aggregate ranking with class-specific (e.g. Class 10th Board) vs. all-class comparative forecasts.
   - Enforces institutional context boundaries against out-of-domain queries.

---

## 3. Data Sovereignty & Security Invariants

- **Student PII Boundary**: Raw student records, marks, and personal identification never leave the institutional boundary.
- **AST Enforced Read-Only Execution**: The system rejects `INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `EXEC`, and multi-statement queries.
- **Audit Traceability**: Every request, authentication attempt, query execution, quality flag, and error event is logged in [`logs/audit.jsonl`](file:///c:/Users/marsh/Downloads/The%20OG%20Project/logs/audit.jsonl).
- **Public Bypass Endpoints**: Only `/health`, `/healthz`, `/readyz`, `/`, `/api/v1/auth/demo-login`, and `/api/v1/auth/sso-login` bypass token verification. All other routes require an authorized session.

---

## 4. Policy Knowledge Entity Registry

| Policy Artifact | Canonical Document Name | Core Scope & Rules |
|---|---|---|
| `POL-001` | `Day Care Centre Policy.pdf` | Childcare facilities for female staff children; nursery care and supervisory safety. |
| `POL-002` | `Day Scholars Policy.pdf` | Admission quota (10/class, 6-8), Rs. 2,000/mo fee, 15th late fee, daily timings (7:45 AM-1:40 PM, Fri 12:15 PM), gate pass security. |
| `POL-003` | `Induction Policy.pdf` | Class 6 intake, Boys 10-12 yrs, Girls 10-13 yrs, Class 5 public/madrassah background, "Intellect with Poverty". |
| `POL-004` | `Late Arrival of Students Policy.pdf` | Progressive sanctions: 1st/2nd verbal warning, 3rd parent letter, Principal counseling. |
| `POL-005` | `Medical Policy for Students.pdf` | 24/7 dispensary staffed by RMO, contagious ward isolation, immediate DHQ Hospital referral for trauma/surgery. |
| `POL-006` | `Leave Policy.pdf` | RMO medical leave, mandatory medical fitness certificate upon return, Sunday 5:00 PM weekend leave deadline. |
| `POL-007` | `Policy Regarding Admission of Siblings.pdf` | Sibling quota applies to currently enrolled students only; graduated siblings excluded; qualifying twins admitted together. |
| `POL-008` | `Promotion Discharge Policy.pdf` | 40% passing threshold (Classes 6-8), 33% BISE standard (9-12), class detention for 2 failed subjects, discharge for 2 consecutive failures. |
| `POL-009` | `School Instructions.pdf` | Prescribed uniform, mandatory supervised prep sessions, strict ban on mobile devices, smartwatches, cash, and contraband. |

---

## 5. Verification & Test Evidence Baseline

- **Total Test Suite**: **959+ baseline tests passed + 35 active predictive/NL2SQL integration tests (0 failed, 100% pass rate)**.
- **Gold Prompts**: 612 automated test cases verifying 14 table families and 20 campuses.
- **Exception & Safety Cases**: 100 safe refusal test cases.
- **Live SQL Concurrency**: 100 concurrent queries benchmarked with 0 failures.
- **Policy RAG Benchmark**: 20/20 benchmark queries passed with 100% citation and accuracy across all 9 official Daanish School policy documents.
- **Multi-Tier Predictive Intelligence**: Multi-tier evaluation across students, teachers, subjects, and campuses ($100\%$ pass rate across all 4 tiers).
- **Out-of-Domain Guardrails**: Complete domain-boundary protection verified across all 3 engines.
- **Frontend Build**: React 19 / Vite production build verified clean in `apps/web/dist/` (0 errors, built in <700ms).

---

## 6. System Archival State

- Legacy local RAG assets (LanceDB, FastEmbed local models, local chunkers, indexes, and ingest scripts) are cleanly isolated in [`Rag_Archive/`](file:///c:/Users/marsh/Downloads/The%20OG%20Project/Rag_Archive).
- The root project remains strictly focused on production-ready multi-engine services and institutional deployment.
