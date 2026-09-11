# Testing Patterns & Verification

## 1) Test Stack and Framework

- **Primary framework**: `pytest` (v9.1.1) + `pytest-asyncio` + `starlette.testclient`.
- **Test execution**: `pytest tests/` (105s execution time for the full 959-test suite).
- **Verified status**: **959 passed, 0 failed, 1 skipped** (100% pass rate).

## 2) Test Layout

```text
tests/
├── unit/
│   ├── test_auth_routes.py                  (11 tests - SSO/Demo authentication)
│   ├── test_db_adapters.py                  (17 tests - Read-only AST & preflight)
│   ├── test_engines.py                      (3 tests - Multi-engine response contracts)
│   ├── test_health.py                       (4 tests - Healthz, Readyz, Stats)
│   ├── test_middleware.py                   (2 tests - Fixed-window rate limiter & security headers)
│   ├── test_nl2sql_synthesizer.py           (7 tests - Wren intent parser & table routing)
│   ├── test_prediction_route.py             (5 tests - Risk estimation & SHAP attributions)
│   ├── test_query_route.py                  (5 tests - Unified /api/v1/query routing)
│   ├── test_stats_route.py                  (2 tests - Campus summary metrics)
│   └── test_wren_engine.py                  (20 tests - Strict Wren MDL & planning)
├── eval/
│   ├── test_all_610_gold_prompts.py         (612 tests - Comprehensive 14-table family gold prompts)
│   ├── test_100_exceptions_pytest.py        (100 tests - Safe refusal & out-of-scope prompts)
│   ├── test_gold_prompts.py                 (10 tests - Multi-domain gold assertions)
│   ├── test_persona_benchmarks_pytest.py    (2 tests - Role-based query benchmarking)
│   └── test_wren_human_queries.py           (34 tests - Natural language teacher/student queries)
├── integration/
│   ├── test_authorized_prompt_path.py       (7 tests - End-to-end authorized pipeline)
│   ├── test_live_wren_stress.py             (1 test - 100 concurrent queries stress test)
│   ├── test_wren_100_unique_live_prompts.py (1 test - 100 live prompts execution against SQL Server)
│   └── test_ws04_extensive.py               (11 tests - Semantic layer extensive checks)
├── test_gemini_file_search_20_benchmark.py  (1 test - 20/20 benchmark policy questions passed)
├── test_policy_batch_and_multiformat.py     (7 tests - Batch upload/deletion & multi-format support)
└── test_prediction_and_multiturn_integration.py (6 tests - Multi-turn threads & failsafe)
```

## 3) Verified Quality & Security Gates

- **Zero-Write AST Enforcement**: SQL AST validator strictly rejects `INSERT`, `UPDATE`, `DELETE`, `DROP`, and multi-statement queries.
- **Privacy & PII Protection**: Strict de-identification gates ensure student PII and unredacted marks are never sent to external LLMs.
- **Rate-Limiting**: Fixed-window rate limiter bounds requests at 300 req/min with `Retry-After` headers.
- **100% Policy Retrieval Accuracy**: Google Gemini File Search API benchmark passes 20/20 difficult test cases with 98.3% average keyword accuracy and valid document citations.

## 4) Evidence

- `docs/00-control/PROJECT_CONTROL.md`
- `tests/` (959 passed in 105.69s)
