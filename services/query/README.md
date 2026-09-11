# Governed Query Service Boundary

Owners: Muhammad Junaid and Abdur Rafay. Workstream: WS-04.

This service owns Wren AI integration, local RAG over approved documentation, local redaction/tokenization, SELECT-only validation, allowlisted semantic access and read-only execution. Raw student rows and protected outputs must never enter external LLM context.

Current state: strict Wren MDL planning, live read-only SQL execution and provenance-verified local hybrid policy retrieval are implemented. The active policy corpus is `data/policy_rag_markdown_r4/`: 144 chunks from the nine supplied Markdown sources. It is a protected, ignored local runtime asset; the policy corpus remains draft-only until a named Daanish School domain reviewer accepts it.

The Daanish 610-prompt catalog is a protected local runtime asset at `data/gold_prompts/EduQuery_Gold_Prompts.csv`. It is used for deterministic routing of the exact school-supplied standard prompts and must not be sent to an external planner. The client catalog's singular `STUDENT_RESULT_TOTAL*` labels map to the live plural views. Internal result-card execution uses `INTERNAL_STUDENT_RESULT_CARD_VIEW` because the live `STUDENTS_RESULT_TOTAL_INTERNAL` view can fail when its `STRING_AGG` output exceeds 8,000 bytes.

`SQLSERVER_CONTRACT_MODE=legacy_snapshot` preserves the verified local restore. Production requires `live_v1`: after strict Wren planning, fixed code-owned routing moves every approved `dbo` reference into `eduquery_reporting`. The SQL adapter then rejects raw legacy objects. The database contract must be active and its version must match the application configuration before readiness succeeds.

Rebuild the asset only from the approved source directory and local model packages. The command refuses to overwrite an existing index; build to a new versioned `data/policy_rag_markdown_*` directory, validate it, then change `POLICY_RAG_ROOT` deliberately.

```powershell
$env:HF_HUB_OFFLINE = '1'
.\.venv\Scripts\python.exe -m services.query.policy_ingest `
  --source '<approved-policy-markdown-directory>' `
  --output '.\data\policy_rag_markdown_r4' `
  --model-root '<approved-local-model-directory>'
```

The builder requires the exact nine-file source set, embeds locally, runs one retrieval check per artifact, seals source/model/index hashes, and leaves release eligibility false. Do not replace the active asset with a failed or partially built directory.
