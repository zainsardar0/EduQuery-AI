# EduQuery AI SQL Server View Reconciliation & Candidate Verification Report

## Executive Summary

This report documents the final, independently replayable audit of the SQL Server view definitions for EduQuery AI (`db_aadc11_sqldaanish`).

Using read-only catalog queries (`sys.views` joined with `sys.schemas` and `sys.sql_modules`), every live view definition was extracted, normalized, and compared 1-to-1 against the retained verified candidate export (`database_views_export_verified_candidate.sql`).

All 11 acceptance gates passed cleanly. Zero database mutations were performed, and no student data, PII, or credentials were extracted or exposed. Both canonical export files (`database_views_export.sql` and `database_views_export_live.sql`) are byte-identical to the candidate export (SHA-256: `93b40692d521d655d8e70b5cfeaa1935d839864a85473179df3bc443f342e21c`).

---

## Live Connection & Diagnostic Parameters

- **Target Database**: `db_aadc11_sqldaanish` (SQL Server 2022 RTM - 16.0.1000.6 X64)
- **Authentication Method**: Windows Integrated Authentication (NTLM / SSPI)
- **Transport & Security**: Localhost shared memory / loopback (`Server=localhost;Database=db_aadc11_sqldaanish;Integrated Security=True;Encrypt=False;`)
- **Encryption Status**: Localhost diagnostic connection exception documented; zero external routes unencrypted.
- **Verification Timestamp**: 2026-08-03 T08:29:00+05:00
- **Database Modification State**: UNCHANGED (0 rows/objects created, altered, or deleted).

---

## Key Findings & Root Cause Analysis

1. **Live Catalog State**:
   - The live SQL Server database `db_aadc11_sqldaanish` contains **exactly 68 distinct user views** (`sys.views` where `is_ms_shipped = 0`).
   - Every single view has an available definition in `sys.sql_modules`. Zero views are encrypted, null, or inaccessible.

2. **Root Cause of Historical Legacy Export Discrepancies**:
   - In earlier developer iterations, three live views (`[dbo].[BOARD_MIDDLE]`, `[dbo].[BOARD_MIDDLE_old]`, and `[dbo].[BOARD_MIDDLE_WORKING]`) contained un-updated `CREATE VIEW BOARD_MIDDLE2 AS` headers inside their `sys.sql_modules.definition` text.
   - When legacy export tools dumped `sys.sql_modules.definition` row-by-row, it generated **three `CREATE VIEW BOARD_MIDDLE2` statements** in the export files.
   - Live DB catalog verification (`sys.views`) confirmed **`[dbo].[BOARD_MIDDLE2]` DOES NOT EXIST in the live catalog**.
   - Standardizing statement headers to match the authoritative catalog schema-qualified name (`[schema].[view_name]`) while keeping 100% of the underlying SQL logic intact aligned every statement 1-to-1 with `sys.views`.

---

## Normalization Algorithm

Deterministic normalization applied to both live definitions and candidate statements for definition hash comparison:
1. Strip UTF-8 BOM (`\ufeff`) if present.
2. Convert line endings to LF (`\n`).
3. Trim trailing whitespace per line (`line.rstrip()`).
4. Strip trailing `GO` statements.
5. Trim leading and trailing blank lines.
6. Normalize ONLY the leading `CREATE VIEW` declaration header to match the catalog schema-qualified name (`CREATE VIEW [schema_name].[view_name] AS`).
7. Preserve 100% of the SQL body (comments, CTEs, SELECT clauses, JOINs, WHERE predicates, GROUP BY, UNION ALL).

---

## Candidate-versus-Live Audit Acceptance Gates

| Acceptance Gate | Requirement | Result | Status |
|---|---|---|---|
| Live Catalog User Views | `sys.views` where `is_ms_shipped = 0` | 68 Views | **PASS** |
| Candidate Statement Count | Distinct `CREATE VIEW` statements in candidate | 68 Statements | **PASS** |
| Both Sides Distinct Names | Union of live and candidate view names | 68 Names | **PASS** |
| Candidate Duplicates | Duplicate view names inside candidate export | 0 Duplicates | **PASS** |
| Set Difference: Live Only | Live views absent from candidate | 0 (`LIVE_ONLY = 0`) | **PASS** |
| Set Difference: Candidate Only | Candidate views absent from live catalog | 0 (`CANDIDATE_ONLY = 0`) | **PASS** |
| Hash CSV Row Count | Total rows in candidate_live_definition_hash_comparison.csv | 68 Rows | **PASS** |
| Hash Population | Both `live_normalized_sha256` & `candidate_normalized_sha256` present | 68 / 68 Populated | **PASS** |
| Definition Match | `definition_match = TRUE` for all 68 rows | 68 / 68 True | **PASS** |
| Inaccessible Definitions | Encrypted, null, or missing definitions | 0 Null/Encrypted | **PASS** |
| Sensitive Data Scan | Credentials, passwords, PII, internal paths scan | 0 Findings | **PASS** |
| Canonical Export Byte-Equality | `database_views_export.sql` & `database_views_export_live.sql` byte-identical to candidate | 100% Byte Match | **PASS** |

---

## Generated Evidence Artifacts

All mandatory accepted audit evidence files are stored together in `docs/07-evidence/sql-view-reconciliation/`:

1. `connection_diagnostics_sanitized.txt`
2. `live_views.csv`
3. `export_views.csv`
4. `duplicate_statements.csv`
5. `view_set_comparison.csv`
6. `definition_hash_comparison.csv`
7. `candidate_live_set_comparison.csv`
8. `candidate_live_definition_hash_comparison.csv`
9. `database_views_export_verified_candidate.sql`
10. `RECONCILIATION_REPORT.md`

---

## Conclusion & Verification Summary

The retained candidate and both canonical exports are independently proven to match all 68 live SQL Server view definitions. Every documented acceptance gate passed.
