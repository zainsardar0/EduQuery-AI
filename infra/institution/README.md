# Institutional Deployment Boundary

Owners: Abdur Rafay and Muhammad Junaid. Workstreams: WS-03, WS-04, WS-05 and WS-08.

This boundary hosts FastAPI, Wren AI, local RAG, SQL access, MLflow/models, SHAP, audit services and the approved HTTPS/VPN gateway. Protected student data remains here.

The boundary now includes a versioned SQL reporting contract under `sql/`. The package is additive: it leaves legacy portal objects untouched, creates curated reporting wrappers, repairs the verified internal/HOF grain defects, materializes the two slow reporting families, validates the certified student-position source and pass-rule coverage, and activates only after every gate passes.

Production configuration, the institution-owned SQL endpoint, dedicated read-only application identity, approved pass rules, certified student-position source, refresh scheduling, backup/restore rehearsal and security acceptance remain deployment-site responsibilities.
