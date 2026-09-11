# EduQuery live Wren model

This is the source Wren project for the live SQL Server analytics demo. It covers the five verified models used by the API. SQL Server has no enforceable foreign keys for these relations, so no relationship is declared until its cardinality and composite join keys are verified.

Build and validate it with a pinned `wrenai[mssql]` environment before deployment:

```powershell
wren context validate
wren context build
```

The API executes Wren-planned SQL through its hardened local SQL Server adapter. A Wren connector profile is intentionally not committed. Do not add raw protected rows, unapproved objects, or credentials to version control.
