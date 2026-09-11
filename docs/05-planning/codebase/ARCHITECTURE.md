# Architecture & System Design

## 1) Architectural Style

EduQuery AI is a multi-engine prompt-based analytics and prediction engine designed specifically for multi-campus academic databases (Punjab Daanish Schools and Centres of Excellence Authority).

The system integrates three specialized execution engines behind a unified, secure FastAPI orchestrator:
1. **WrenAI NL2SQL Engine**: Semantic layer modeling 14 core table families (68 views) with parameterized T-SQL generation and data-grounded summaries.
2. **Google File Search API (Gemini RAG)**: Direct cloud file storage retrieval across official institutional policy documents (PDF, DOCX, MD, TXT, CSV, RTF, HTML) with executive-level citations.
3. **Prediction AI Engine**: ML risk modeling with TreeSHAP feature attributions and tailored student academic intervention recommendations.

## 2) System Flow

```text
React 19 / Vite Web UI (apps/web/)
  ├── Navigation: 20-campus selector, Engine switcher, Session history
  └── Endpoints:
        POST /api/v1/query (Unified Orchestrator)
        POST /api/v1/policies/ask (Google File Search)
        POST /api/v1/predict (Prediction AI & SHAP)
        POST /api/v1/auth/demo-login & /sso-login
        POST /api/v1/query/flag (Quality feedback)

FastAPI Backend Gateway (services/api/)
  ├── AuthMiddleware: Deny-by-default session verification
  ├── Rate Limiter: Fixed-window bounded at 300 req/min
  ├── Security Headers: nosniff, frame-options, xss-protection
  ├── SQL AST Validator: SELECT-only enforcement via sqlglot
  └── Engine Router:
        ├── Wren NL2SQL Synthesizer -> SQL Server / SQLite Demo
        ├── Google Gemini File Storage RAG -> Policy Documents
        └── Prediction Intelligence -> Risk & SHAP Attributions

Audit Trail & Privacy Gate (logs/audit.jsonl)
  └── Zero-PII structured logging with UUID event correlation
```

## 3) Verified Security Baseline

- **Server-Side Authorization**: `AuthMiddleware` verifies session tokens, role scopes, and campus permissions.
- **Read-Only Data Access**: Strict SQL AST parsing rejects all data manipulation statements (`INSERT`, `UPDATE`, `DELETE`, `DROP`).
- **Data Sovereignty**: Student identifiers and individual grades remain inside the institutional network boundary; external calls receive only de-identified intent.
- **Audit Traceability**: Every query, flag, and prediction event is recorded in `logs/audit.jsonl` with latency, user ID, engine type, and anonymized metadata.

## 4) Evidence

- `DOCUMENTS.md`
- `docs/00-control/PROJECT_CONTROL.md`
- `services/api/main.py`
- `services/api/app/routes/query_routes.py`
- `tests/` (959 passing tests)
