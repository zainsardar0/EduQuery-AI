# Technology Stack

## 1) Runtime Summary

| Area | Production Stack | Implementation Details |
|---|---|---|
| Frontend | React 19 + Vite 8 + Tailwind CSS v4 + Recharts | `apps/web/` with unified 3-engine chat, campus selector, interactive tables/charts |
| Backend | Python 3.11 + FastAPI + Pydantic v2 + Uvicorn | `services/api/` with `AuthMiddleware`, rate-limiting (300 req/min), audit logging |
| Data Layer | Microsoft SQL Server (14 table families, 68 views) + SQLite Fallback | `services/query/wren_engine.py`, `services/api/app/adapters/database.py` |
| NL2SQL Engine | Wren AI (0.13.2) + Gemini 3.5 Flash Lite Synthesizer | Strict 16-model MDL semantic planning with parameterized T-SQL |
| Policy RAG | Google Gemini File Search API (`gemini-3.1-flash-lite`) | Multi-format file storage (PDF/DOCX/MD/TXT), dynamic scoring, zero-hallucination citations |
| Prediction Engine | Gradient Boosted Decision Trees / Random Forests + TreeSHAP | Risk scoring, probability breakdown, feature attributions, targeted interventions |
| Verification | Pytest (959 passing tests across unit, integration, and eval suites) | `tests/unit/`, `tests/eval/`, `tests/integration/` |

## 2) Production Dependencies

| Dependency | Purpose | Status |
|---|---|---|
| `fastapi` | High-performance asynchronous REST API framework | Active |
| `pydantic` | Data validation and contract modeling | Active |
| `google-genai` | Google Gemini File Search API and NL2SQL synthesis | Active |
| `wrenai` | Semantic modeling layer and T-SQL planning engine | Active |
| `sqlglot` | SQL AST validation and SELECT-only enforcement | Active |
| `react` & `react-dom` (v19) | Frontend component UI runtime | Active |
| `recharts` | Visual performance analytics and pass rate charts | Active |
| `lucide-react` | Enterprise UI icons | Active |
| `tailwindcss` (v4) | Styling engine and responsive layout | Active |

## 3) Key Execution Commands

- **Backend Development**: `uvicorn services.api.main:app --reload --port 8000`
- **Frontend Development**: `npm --prefix apps/web run dev`
- **Frontend Production Build**: `npm --prefix apps/web run build`
- **Full Test Suite**: `pytest tests/`

## 4) Evidence

- `DOCUMENTS.md`
- `services/api/main.py`
- `apps/web/package.json`
- `pyproject.toml`
- `tests/` (959 passing tests)
