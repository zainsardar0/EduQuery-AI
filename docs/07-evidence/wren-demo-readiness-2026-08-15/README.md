# Wren demo readiness evidence — 2026-08-15

Workstream: WS-04 / WS-07. Human owner and acceptance authority: Muhammad Junaid with the named EduQuery team. This package is sanitized: it contains no prompt results, student identifiers, credentials, policy excerpts or database rows.

## Verdict

- **Today’s local Wren demo:** ready for a controlled rehearsal on this workstation.
- **Institutional production release:** not ready. The current database is a read-only restore of a July 13 backup, not a continuously updated institutional source. Production identity, ingress and operations gates remain open.
- **Policy RAG:** the active local LanceDB uses only the nine user-supplied Markdown policy files (144 chunks), with source/model/index hashes and real Markdown line-range citations. It remains draft-only and is not release eligible until a named Daanish School domain reviewer accepts it.
- **External model:** disabled. It is not required for the implemented natural-language answer plus optional table. Protected query results never go to an external model.

## Data evidence

- Backup: `C:\SQL_Database\db_aadc11_sqldaanish_7_13_2026_21.bak`
- Size: 422,694,912 bytes.
- SHA-256: `CC4206255E8BA81DA3F688AC6B3BF3260773910807DE30BD4B91FA45C5903714`.
- SQL backup header: full database backup; database `db_aadc11_sqldaanish`; start `2026-07-13 21:00:17`; finish `2026-07-13 21:00:20`; `IsDamaged=False`; no backup checksum; not encrypted according to the header.
- Safe restore target: `EduQuery_Wren_20260713`; updateability `READ_ONLY`; 69 tables; 68 views; 1,997,113 current heap/clustered rows reported by `sys.dm_db_partition_stats`.
- The original database was not overwritten.

## Implemented request path

`authenticated prompt -> local safety/identity parser -> optional privacy-safe concept planner -> strict Wren 0.13.2 MDL -> adapter T-SQL AST/object gate -> read-only SQL Server -> local deterministic narrative + supporting rows`

The five built Wren models are `student_enrollment`, `student_result_card`, `consolidated_results`, `house_attendance` and `teacher_results`. The consolidated model uses authoritative pre-aggregated `SUBJECT='TOTAL'` rows from `dbo.students_result_total`; the prior full pivot/rank view was removed from the execution allowlist after it exceeded the 12-second timeout for a five-row campus query. Every authenticated user has the same all-campus query visibility; legacy campus/role token arguments cannot recreate restrictions.

The local API now validates JWT issuer/audience and required claims, rejects unsafe production configuration, adds per-process request limiting, request IDs, security headers and structured request telemetry. These are application controls; the institutional gateway must still supply distributed ingress enforcement and managed identity/secrets.

## Reproducible checks

Run from the repository root with external calls forced off:

```powershell
$env:EXTERNAL_MODEL_ENABLED='false'
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m pytest -q -s tests\integration\test_live_wren_stress.py
uv pip check --python .\.venv\Scripts\python.exe
uv build . --out-dir .\_draft\build-check-root
```

Observed on 2026-08-15:

- Full suite after the Markdown corpus switch and grade-level planning regression fix: 296 passed; one upstream Starlette TestClient/httpx deprecation warning.
- Human Wren acceptance set: 100 unique prompts traversed authentication, FastAPI, local intent/safety, strict Wren physical planning and response validation; 80 executed live SQL; zero external calls; p95 500.91 ms.
- Live stress: 100 requests, 16 workers, 0 failures; p50 200.08 ms; p95 443.70 ms; maximum 545.58 ms.
- Dependency check: 79 packages compatible.
- Wheel inspection: 40 entries; API, contracts, Wren service and built `mdl.json` present; legacy seed builder and seed adapter absent.
- Markdown RAG mechanics: local-only LanceDB built 144 chunks from 9 exact supplied files; its nine artifact retrieval checks achieved 9/9 recall@3. The active corpus deliberately excludes the two old OCR/image-only supplemental artifacts.
- Browser QA: connection, greeting, weak-student query, personal result query and sibling-policy RAG with Markdown filename/line-range/artifact/hash evidence succeeded; zero browser console errors; zero external requests.
- Screenshot-regression QA: the current UI has no role label or role-named access state; the historical weak-student wording returns a local Wren result with a text answer; the historical personal-result wording routes locally and never invokes the external planner.

## Review findings fixed before this evidence was accepted

1. The initial wheel was metadata-only. The canonical build configuration was moved to the repository root and the rebuilt wheel was inspected.
2. The live adapter relied on the read-only database and Wren alone. It now independently rejects non-SELECT, multi-statement and unapproved-object SQL before connecting.
3. The optional provider fallback could have leaked an unrecognized name. Raw prompts no longer leave the institution; only locally extracted allowlisted concepts and filters can be sent when explicitly enabled.
4. The old consolidated pivot/rank view timed out for a five-row campus query. The same authoritative result source exposes pre-aggregated total rows; the Wren mapping now uses those rows and the failing direct query completed in 115.53 ms.
5. The wheel still shipped unused synthetic database modules. They and their seed-only tests were removed; the clean wheel proves they are absent.
6. The provider wrapper claimed an undocumented retention header. It now uses OpenRouter's documented per-request `provider.zdr=true` control; external execution remains disabled.

## Provider incident, bounded verification and current safeguard

Before the external-call kill switch was installed, a legacy integration run accidentally attempted 26 OpenRouter calls, exceeding the user-approved two-call budget. All 26 were refusals and produced no successful plan. After the local path, RAG, and test suite were ready, exactly two newly approved live planner checks were made with no PII and no database rows or result summaries in the outbound content. Both returned validated plans. The second exposed a grade-level wording misclassification; that wording now deterministically routes to local class-performance planning and is regression-tested. `EXTERNAL_MODEL_ENABLED=false` remains the normal configuration. No further provider check is authorized without a new explicit approval.

## Remaining production gates

1. Replace the July 13 restored snapshot with the continuously updated institutional SQL Server DSN.
2. Provision a dedicated read-only SQL identity; the local demo currently uses Windows authentication under a privileged login, constrained by the database-wide `READ_ONLY` state.
3. Replace demo JWT issuance with the institution’s production identity provider and secret lifecycle.
4. Deploy distributed gateway rate limiting, monitoring/alerting, backup/recovery rehearsal and deployment runbook evidence; the in-process limiter is not a multi-worker ingress substitute.
5. Record a named Daanish School policy reviewer and rerun the RAG acceptance set as domain-reviewed evidence.

The next safe action for today is one clean demo rehearsal with the external-model switch off. The first production action is provisioning the dedicated read-only identity against the continuously updated institutional database.
