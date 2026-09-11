# Codebase Structure

## 1) Top-Level Map

| Path | Purpose | Evidence |
|---|---|---|
| `.agents/` | Repository-specific ownership and documentation rules | `.agents/AGENTS.md` |
| `docs/` | Canonical stakeholder documents, planning docs, schema catalog, and audit evidence | `DOCUMENTS.md` |
| `README.md` | Short product overview and quickstart instructions | `README.md` |
| `apps/web/` | React 19 + Vite + Tailwind CSS v4 frontend dashboard | `apps/web/src/App.jsx`, `apps/web/package.json` |
| `services/api/` | FastAPI service, auth middleware, rate-limiting, and query orchestration | `services/api/main.py`, `services/api/app/` |
| `services/query/` | Wren AI semantic layer, NL2SQL synthesizer, and T-SQL planning engine | `services/query/wren_engine.py` |
| `services/prediction/` | ML risk classification, SHAP feature attributions, and academic intervention engine | `services/api/app/services/prediction_intelligence.py` |
| `packages/contracts/` | Shared TypeScript and Pydantic DTO contracts | `packages/contracts/` |
| `data/` | Original databases, clean policy documents, and data dictionaries | `data/original_database/`, `data/clean_policies/` |
| `tests/` | Unit, integration, eval (610 gold prompts + 100 exceptions), and benchmark test suites (959 passing tests) | `tests/unit/`, `tests/eval/`, `tests/integration/` |
| `Rag_Archive/` | Archived legacy local RAG assets (LanceDB, FastEmbed, local models) | `Rag_Archive/` |

## 2) Entry Points

- **API Service**: `uvicorn services.api.main:app --reload --port 8000` (or `npm --prefix apps/web run dev:backend`).
- **Web Frontend**: `npm --prefix apps/web run dev` (runs Vite dev server on `http://localhost:5173`).
- **Test Suite**: `pytest tests/` (executes 959 automated tests covering unit, eval, benchmark, and live integration).

## 3) Module Boundaries and Responsibilities

| Boundary | Owns | Must not own |
|---|---|---|
| `apps/web` | Unified Chatbot UI (WrenAI NL2SQL, Google File Search RAG, Prediction AI), 20-campus selector, multi-turn chat threads, quality feedback, and administrative dashboard | Raw SQL generation, database credentials, or external API keys |
| `services/api` | API contracts, server-side `AuthMiddleware`, rate limiting (300 req/min), audit logging, and multi-engine routing | Frontend React rendering logic |
| `services/query` | Wren AI semantic layer, safe parameterized T-SQL synthesis, 14 table families, and local data-grounded summaries | Direct SQL write/mutation operations |
| `services/prediction` | Student drop-out and pass-rate risk forecasting, SHAP feature importance attributions, and student interventions | Final administrative or human grading authority |
| `packages/contracts` | Pydantic models, JSON schemas, and exported TypeScript declarations (`.d.ts`) | Business logic and execution |
| `tests` | Comprehensive test suites: 959 tests verifying unit behavior, 610 gold prompts, 100 exceptions, stress concurrency, and 20 policy benchmarks | Production application code |

## 4) Evidence

- `DOCUMENTS.md`
- `.agents/AGENTS.md`
- `docs/00-control/PROJECT_CONTROL.md`
- `services/api/main.py`
- `apps/web/package.json`
- `tests/` (959 passing tests)
