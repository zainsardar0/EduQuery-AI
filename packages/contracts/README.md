# EduQuery AI API Contracts (v1)

> **Status:** Published v1  
> **Source of Truth:** Pydantic models in `packages/contracts/schemas/`

## Exported Assets

- `dist/schemas/*.json` — JSON Schemas for OpenAPI / FastAPI validation
- `dist/types.d.ts` — TypeScript interfaces for Next.js frontend (`apps/web`)

## Models Included

1. `AuthContext` — Authentication context & campus scope
2. `QueryRequest` / `QueryResponse` / `QueryRefusal` — NL2SQL query pipeline
3. `PredictionRequest` / `PredictionResponse` — Academic risk engine
4. `PolicyRequest` / `PolicyResponse` — Policy document RAG engine
5. `APIError` — Machine-stable error envelope

## Export Command

```bash
python packages/contracts/export_schemas.py
```
