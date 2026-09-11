# Wren Daanish 610-prompt evidence — 2026-08-16

Workstreams: WS-02, WS-04 and WS-07. Human owner and acceptance authority: Muhammad Junaid with the named EduQuery team.

## Verdict

- **External-off Wren routing and strict planning:** passed for all 610 prompts.
- **Single-object live execution:** 510/515 passed under a four-worker sweep; all five slow-view failures passed individually.
- **Institutional production:** not ready. Slow/broken views, the missing student-position source, unapproved cross-table contracts, institutional identity/DSN/ingress, and human answer validation remain open.
- **Answer accuracy:** unknown. The client files provide prompt text and intended family, but no expected SQL or expected result values.

## Protected inputs

The source files stay in the ignored local `data/gold_prompts/` directory and are not included in this package.

| File | Rows/size | SHA-256 |
|---|---:|---|
| `EduQuery_Gold_Prompts.csv` | 610 rows / 57,814 bytes | `8969cc00350a9db84f5494099d116e5b3622368f9163b2da78cc8752c3f48379` |
| `EduQuery_Tables_and_Prompt_Catalog.md` | 47,753 bytes | `f89c002c468a0091c6145e31afd9c025561113b9e1f243e97836e0cd3f916dbd` |

No prompt text, student row, name, roll/SMS identifier, SQL result, credential or raw audit log is retained here.

## Results

| Gate | Result |
|---|---|
| Input integrity | 610/610 sequential and unique |
| Strict Wren MDL | 16 models; validate/build passed; MDL SHA-256 `977b61a0859094e7243797196a922309c2bdbc27b034fc9eaf02cc2cdff4a7f4` |
| Static client sweep | 515 compiled/executable single-object prompts; 95 correct governed refusals; 0 provider-required routes; 0 planning failures |
| Refusal split | 55 cross-table/prediction prompts without approved contracts; 40 student-position prompts contradicted by the live view |
| Live four-worker sweep | 510 succeeded; 5 slow-view concurrency failures; p50 28.43 ms; p95 1091.17 ms; max successful 10588.61 ms |
| Individual replay of failed cases | 5/5 succeeded; about 5–12 seconds each |
| Full regression | 299 passed; one upstream Starlette/httpx deprecation warning |
| Existing 100-prompt E2E | 100 prompts; 80 live SQL; zero external calls; p95 700.48 ms |
| Dependency/package check | 79 packages compatible; wheel built with 40 entries and the MDL present; protected catalog absent by design |
| Graph/brain closeout | Code map rebuilt to 463 nodes / 794 edges; brain doctor passed with 0 stale evidence and 0 problems |

## Reproducible checks

```powershell
$env:EXTERNAL_MODEL_ENABLED='false'
.\.venv\Scripts\wren.exe context validate --path .\services\query\wren_project --strict
.\.venv\Scripts\wren.exe context build --path .\services\query\wren_project
.\.venv\Scripts\python.exe -m pytest -q
```

The protected 610-case test is `tests/eval/test_daanish_610_gold_prompts.py`; it skips when the ignored client catalog is absent.

## Production blockers

1. Obtain expected SQL/result truth and named Daanish domain acceptance for answer accuracy.
2. Supply the correct student-level subject-position source.
3. Approve cross-table join grains, metrics, diagnosis rules, and prediction-service boundaries.
4. Repair the internal-total `STRING_AGG` overflow and optimize/materialize the slow HOF/internal views.
5. Replace the July 13 restore and privileged Windows identity with the continuously updated institutional DSN and dedicated read-only identity.
6. Complete production authentication, distributed ingress limits, monitoring, recovery and operational acceptance.
7. When explicitly authorized, attach the LLM API and run a separate privacy-safe planner comparison; protected prompts and results must remain local.
