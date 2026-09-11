# EduQuery AI — Versioned Shared Contracts Specification

> **Version:** 1.0.0  
> **Package:** `packages/contracts/`  
> **Human Owner / Acceptance Authority:** Muhammad Junaid  
> **Status:** Production-ready interface definition for WS-03 through WS-07  

---

## 1. System Topology & Security Boundary

```text
+-----------------------------------------------------------------------+
| Vercel Deployment (Browser UI & Static Assets Only)                   |
| - Routes: / , /query , /prediction                                    |
| - NO Server Actions, NO Vercel API Routes, NO OpenRouter Keys         |
| - NO SQL processing, NO RAG, NO raw student data                       |
+-----------------------------------------------------------------------+
                                  |
                                  | Direct HTTPS / VPN Request
                                  v
+-----------------------------------------------------------------------+
| Institution-Hosted FastAPI Backend                                    |
| 1. Authentication & Role/Campus Scope Authorization (Server-Side)     |
| 2. Query Intent Classification & Local RAG Retrieval                   |
| 3. Local Redaction / Tokenization (PII & Student IDs stripped)        |
| 4. OpenRouter API Call (GPT 5.6 Luna Pro - De-identified schema only) |
| 5. Read-Only SQL Validation (AST parse, SELECT-only, parameters)      |
| 6. MSSQL 2022 Query Execution (Least-privilege read-only user)        |
| 7. Prediction Pipeline (AutoGluon / TabPFN + SHAP explainability)     |
| 8. Redacted Audit Event Logging                                       |
+-----------------------------------------------------------------------+
```

---

## 2. Server-Derived Auth & Authorization (`auth_context.json`)

1. **Deny-by-Default Authorization**: Authority fields submitted in client payloads are strictly ignored.
2. **Server-Side Token Inspection**: The institutional backend parses the Bearer JWT token to construct `auth_context`:
   - `user_id`: Validated UUID.
   - `role`: Assigned institutional role (`admin`, `principal`, `teacher`, `counselor`, `auditor`).
   - `campus_scope`: List of 4-letter campus codes (`SCHOOL`) authorized for the user (e.g. `["MNWB", "MNWG"]`).
   - `teacher_eid`: Employee ID for row-level filtering if role is `teacher`.
3. **Cross-Campus Prevention**: If a user attempts to query a campus outside their `campus_scope`, FastAPI returns an immediate `403 Forbidden` (`CROSS_CAMPUS_ACCESS_DENIED`).

---

## 3. Error Handling & Privacy Guarantees (`error_response.json`)

Public error responses use a stable, structured payload and **never** expose internal implementation details:

- **Forbidden Content in Errors**: Raw SQL queries, T-SQL syntax error traces, database connection strings, credentials, server stack traces, or OpenRouter/LLM provider raw errors.
- **Stable Error Codes**:
  - `AUTH_UNAUTHENTICATED` (401): Missing or invalid Bearer token.
  - `AUTH_UNAUTHORIZED` (403): User lacks role privileges for the requested operation.
  - `CROSS_CAMPUS_ACCESS_DENIED` (403): Requested campus code is outside the user's `campus_scope`.
  - `VALIDATION_ERROR` (400): Malformed JSON or invalid parameter range.
  - `UNSAFE_QUERY_REJECTED` (400): Non-SELECT T-SQL statement, system table access attempt, or prohibited SQL function detected.
  - `NO_DATA_FOUND` (200 / 404): No records matching the authorized query parameters.
  - `RATE_LIMIT_EXCEEDED` (429): Request threshold exceeded.
  - `REQUEST_TIMEOUT` (500): Database or model processing exceeded execution budget.
  - `DEPENDENCY_FAILURE` (500): Downstream service unavailable.
  - `INTERNAL_SERVER_ERROR` (500): Generic safe failure message with `request_id` correlation log ID.

---

## 4. Query Response Contract (`query_response.json`)

The query response delivers four distinct data layers to the Next.js UI:

1. **Answer**: Natural language concise summary synthesized from SQL results.
2. **Data Table**: Tabular array of typed columns and sanitized rows for data grids.
3. **Chart Config**: UI rendering properties specifying chart type (`bar`, `line`, `pie`, `kpi_card`), axis keys, titles, and color palettes.
4. **Evidence Metadata**: Traceability details containing intent category, tables queried, campus code applied, latency in milliseconds, and local RAG reference sources.

---

## 5. Prediction Response Contract (`prediction_response.json`)

The prediction response delivers advisory student performance risk analysis:

1. **Target Entity**: Entity identifier (`target_id`).
2. **Risk Tier & Score**: Categorical risk (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`) and numeric predicted score (0-100%).
3. **Model Metadata**: Model algorithm name (`AutoGluon_WeightedEnsemble_L2`), version tag, MLflow run ID, and evaluation timestamp.
4. **SHAP Feature Attributions**: Top contributing factors with impact direction (`INCREASES_RISK` / `DECREASES_RISK`) and SHAP values.
5. **Advisory Disclaimer**: Mandatory constant disclaimer text asserting that predictions are advisory decision-support tools and not automated grading actions.

---

## 6. Synthetic Example Rule

All schema files and documentation examples **must** use synthetic placeholder identifiers (e.g., student name `"SYNTHETIC_STUDENT_01"`, roll number `"SYN_1001"`, teacher name `"SYNTHETIC_TEACHER_01"`). Real student names, roll numbers, marks, or institutional records must **never** be hardcoded in contract schemas or test files.
