# FastAPI Service Boundary

Owners: Abdur Rafay and Muhammad Junaid. Workstream: WS-03.

This service owns versioned APIs, uniform authenticated all-campus access, orchestration, redacted audit events, limits and fail-closed error handling. It must not contain frontend rendering or hard-coded secrets.

Current state: the local demo API is implemented with read-only SQL Server execution, strict Wren planning, local policy retrieval, JWT claim validation, request IDs, security headers, structured request telemetry, an in-process request limiter and test coverage. Seed fallback is disabled and seed modules are excluded from the build. Production mode additionally requires the `live_v1` database contract, an expected database and contract version, certificate validation, a non-local institutional endpoint, curated reporting-object access and a non-privileged application identity. `/readyz` fails closed on any contract or permission mismatch.

The live database migration and rollback runbook is `infra/institution/sql/README.md`. Production release remains gated on institutional configuration and acceptance evidence; repository scripts do not authorize a live migration.

Install or build from the repository root so the API, query service and shared contracts are packaged together:

```powershell
uv pip install --python .\.venv\Scripts\python.exe -e .
uv build .
```
