# Live SQL Server deployment package

Owners: Abdur Rafay (deployment/security), Muhammad Junaid (semantic and metric acceptance), and the Daanish School database owner (backup, migration and production authorization).

Contract version: `2026.08.16.1`.

## Identity separation

- **Migration identity:** temporary DDL rights; runs the scripts during an approved maintenance window.
- **Refresh identity:** execute permission only on `eduquery_reporting.RefreshPerformanceCaches` plus the minimum source permissions needed by the procedure.
- **Application identity:** `SELECT` on approved `eduquery_reporting` query objects only. It must not be `sysadmin`, `db_owner`, `db_datawriter`, or hold `INSERT`, `UPDATE`, `DELETE`, `ALTER`, or `CONTROL` on those objects.

Never run migrations through the Wren/FastAPI application identity.

## Required sequence

1. Restore the current production backup to an isolated writable rehearsal database.
2. Record baseline object definitions, row counts, representative answers and query latency.
3. Run `001_contract_control.sql`.
4. Insert effective-dated pass rules approved by Daanish School into `eduquery_reporting.PassThresholdRule`. Do not infer the missing year/class rules.
5. Run `002_reporting_views.sql` and `003_materialized_reporting.sql`.
6. Have the database owner supply `dbo.EDUQUERY_STUDENT_SUBJECT_RESULT_SOURCE` at the documented unique grain, then run `004_student_subject_position.sql`.
7. Resolve every row returned by `eduquery_reporting.INTERNAL_STUDENT_GRAIN_CONFLICTS_V1`.
8. Run `900_validate_and_activate.sql`. Any failure blocks activation.
9. Provision the read-only application identity and set the production environment values shown below.
10. Run readiness, security, reconciliation, concurrent-load and all 610 prompt tests.
11. Repeat the same sequence against the live database in an approved maintenance window.

## Production application settings

```dotenv
APP_ENV=production
ENABLE_DEMO_AUTH=false
SQLSERVER_CONTRACT_MODE=live_v1
SQLSERVER_EXPECTED_DATABASE=<institution-approved-database-name>
SQLSERVER_EXPECTED_CONTRACT_VERSION=2026.08.16.1
SQLSERVER_DSN=Driver={ODBC Driver 18 for SQL Server};Server=<institution-endpoint>;Database=<database>;Encrypt=yes;TrustServerCertificate=no;ApplicationIntent=ReadOnly;<institution-authentication>
EXTERNAL_MODEL_ENABLED=false
```

`/readyz` must report `ready`, `live_v1`, contract version `2026.08.16.1`, and no database reason codes.

## Refresh and monitoring

Schedule `eduquery_reporting.RefreshPerformanceCaches` after source-result imports and at the institution-approved interval. Alert on:

- failed or overlapping refreshes;
- freshness older than the agreed service level;
- zero or unexpected row-count change;
- refresh duration regression;
- database blocking, timeout, or storage pressure.

The activation gate currently rejects caches older than 24 hours. Set a stricter operational alert if the school requires fresher results.

## Rollback

Run `rollback_deactivate.sql` to deactivate this contract. The API then fails readiness closed. Preserve reporting objects and evidence for diagnosis; switch to a previously accepted contract only through a separate approved activation.

Database backup/restore remains the recovery mechanism for migration damage. The rollback script is not a substitute for a tested backup.
