# EduQuery AI: RAG Research and Production Blueprint

Status: draft evidence package for WS-04
Human owner: Muhammad Junaid
Research date: 2026-08-03
Scope: English-only EduQuery MVP; local, governed RAG for Wren AI/NL2SQL

## Executive decision

EduQuery should not use RAG as a general answer engine and should not embed student rows. It should use a small, local, hybrid retrieval layer to select governed semantic context before Wren plans SQL:

`authenticated intent -> route -> exact/metadata retrieval + dense retrieval -> RRF fusion -> local reranker -> Wren MDL/verified examples -> SQL validation -> read-only execution -> redacted answer`

The MVP default is **deterministic routing plus hybrid retrieval with selective reranking**. Agentic/multi-hop retrieval, GraphRAG, HyDE, and repeated LLM query rewriting remain opt-in experiments behind the same contract. They are not release dependencies.

This is the best fit because EduQuery's authoritative facts are structured and current. RAG should retrieve definitions, relationships, metric rules, MDL fragments and verified query examples; SQL/Wren should retrieve current counts, marks, results and aggregates. Oracle's production guidance makes the same separation: use SQL/NL2SQL for current structured facts and keyword/vector/hybrid retrieval for unstructured context, then evaluate both paths on one ground-truth set. [Oracle production RAG evaluation](https://blogs.oracle.com/developers/production-rag-evaluation-keyword-vector-sql-or-hybrid-search)

## Evidence quality and coverage

| Evidence | What it shows | Confidence for EduQuery |
|---|---|---|
| Practitioner reports from r/Rag and r/LocalLLaMA | Hybrid BM25+dense retrieval, deduplication, metadata filters, reranking and golden datasets are repeatedly reported as higher-leverage than changing the generator; stale indexes and extra LLM calls are recurring failures. | Directional only; self-reported and not independently audited. |
| CSR-RAG text-to-SQL paper | Contextual, structural and relational retrieval is designed for enterprise schema retrieval; reports over 80% recall and about 30 ms average query-generation latency on its benchmark. | Strong design evidence; benchmark is not EduQuery evidence. [Paper](https://arxiv.org/abs/2601.06564) |
| Schema retrieval benchmark, July 2026 | Table/column retrieval is a first-class task; corpus-adaptive training increased recall@10 from 60.4 to 75.6 and nDCG@10 from 51.9 to 68.0 in the reported benchmark. | Strong evidence that generic embeddings should not be trusted without local evaluation. [Paper](https://arxiv.org/abs/2607.13311) |
| RAG variants for SQL/API generation | In a SAP banking benchmark, no-RAG exact match was 0%; retrieval raised execution accuracy up to 79.30%. Iterative query decomposition beat simple top-k under mixed documentation. | Strong evidence for retrieval and selective decomposition; not a promise of EduQuery accuracy. [Paper](https://arxiv.org/abs/2602.07086) |
| Microsoft Foundry evaluators | Retrieval and answer quality are separate: document retrieval can use NDCG/XDCG/fidelity/holes; groundedness and completeness measure answer precision/recall. | Strong evaluation design evidence. [Microsoft RAG evaluators](https://learn.microsoft.com/en-in/azure/foundry/concepts/evaluation-evaluators/rag-evaluators) |
| Amazon Bedrock metrics | Retrieve-only and retrieve-and-generate evaluations should separately measure context relevance/coverage, correctness, completeness, faithfulness, citation precision and coverage. | Strong evaluation design evidence. [Amazon RAG metrics](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-evaluation-metrics.html) |
| Wren AI documentation | Wren already separates retrieval, generation, validation and execution; MDL is the semantic contract, while memory retrieves schema context and confirmed NL-to-SQL pairs. | Directly applicable architecture evidence. [Wren service](https://docs.getwren.ai/oss/concept/wren_ai_service), [Wren memory](https://docs.getwren.ai/oss/concepts/memory_system) |
| Google Agentic RAG report | Planning, rewriting, fan-out and sufficient-context checks can improve factuality on complex queries; the reported “up to 34%” is a vendor result on its datasets. | Useful for a later experiment, not an MVP default. [Google Research](https://research.google/blog/unlocking-dependable-responses-with-gemini-enterprise-agent-platforms-agentic-rag/) |

### Research limitation

The `last30days` engine was run in public-only mode. Its Reddit, Hacker News and GitHub lanes were blocked by local socket/rate-limit permissions, so it returned no usable community items. That is a coverage failure, not evidence that discussion was absent. Public web search and official pages were used for the evidence above. `ego-browser` was unavailable on Windows; its installation guide is macOS-only, so direct browsing fell back to the host web-search tool.

## How people are actually making RAG accurate

### 1. They make retrieval a ranking pipeline, not one vector lookup

The recurring production pattern is:

1. Cheap candidate retrieval using exact/lexical search and dense similarity.
2. Metadata and permission filtering.
3. Reciprocal Rank Fusion (RRF) or equivalent deduplication.
4. A local cross-encoder or other reranker over a small candidate set.
5. Context selection and a hard token budget before generation.

This addresses two different failure modes: embeddings miss identifiers and exact business vocabulary; lexical retrieval misses paraphrases. Reranking then judges query-document relevance jointly. It costs latency, so it belongs after a cheap shortlist, not over the whole corpus.

### 2. They route by question type

Production systems increasingly route structured lookups to SQL, exact identifiers to keyword predicates, semantic questions to vector retrieval, and mixed questions to a controlled combination. This is not a cosmetic optimization. It prevents vector search from being used where it cannot answer a time-sensitive aggregate or a permission-sensitive row query. [Oracle's route guidance](https://blogs.oracle.com/developers/production-rag-evaluation-keyword-vector-sql-or-hybrid-search)

### 3. They retrieve structure before prose

For NL2SQL, the first retrieval problem is table and column selection, not answer writing. The current schema-retrieval benchmark shows generic embedding models transfer poorly to enterprise schema language and that table/column recall must be measured directly. [Schema retrieval benchmark](https://arxiv.org/abs/2607.13311)

CSR-RAG's contextual, structural and relational retrieval is the closest published pattern to EduQuery: retrieve business descriptions, schema objects and approved relationships as separate but linked units instead of flattening an entire database into text. [CSR-RAG](https://arxiv.org/abs/2601.06564)

### 4. They keep source truth versioned and indexes disposable

Wren's current model is instructive: durable MDL, business rules and accepted NL-to-SQL pairs remain reviewable source files; the semantic index is derived and rebuildable. Wren explicitly says memory is not a replacement for MDL. [Wren memory system](https://docs.getwren.ai/oss/concepts/memory_system)

This prevents a common silent failure: a changed metric definition leaves stale embeddings in production while the application still appears healthy.

### 5. They use iterative retrieval only for hard queries

Query decomposition and agentic retrieval help when a question crosses multiple sources or requires missing-context detection. They also add calls, failure modes and data-flow complexity. The SQL/API study found iterative decomposition useful under heterogeneous documentation; Google's agentic RAG report describes planning, rewriting, fan-out and sufficient-context checks. Both support a selective route, not “agents for every question.”

### 6. They evaluate retrieval and generation separately

A single “RAG accuracy” number hides the cause of failure. Teams that can improve reliably measure:

- retrieval: recall@k, precision@k, MRR, nDCG, fidelity, holes and exact table/column hit rate;
- grounded response: correctness, completeness, faithfulness, citation precision/coverage and abstention;
- system: p50/p95 latency by stage, cache hit rate, token count, error rate and fallback rate;
- NL2SQL: execution success, result-set equivalence, scope correctness, non-SELECT rejection and refusal correctness.

Microsoft and Amazon both document this split. [Microsoft](https://learn.microsoft.com/en-in/azure/foundry/concepts/evaluation-evaluators/rag-evaluators) [Amazon](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base-evaluation-metrics.html)

## EduQuery production design

### Retrieval corpus

Only these versioned, reviewed artifacts enter the index:

- approved schema and view descriptions;
- canonical column vocabulary and synonyms;
- Wren MDL models, relationships, views, cubes and calculated metrics;
- business rules and campus/role visibility rules;
- sanitized, human-approved NL-to-SQL examples;
- refusal examples and unsupported-intent definitions.

Never index student identities, roll numbers, row-level academic data, marks, results, predictions, protected prompts, raw query results, credentials or arbitrary external documents.

### Retrieval units and metadata

Use typed records rather than arbitrary text chunks:

`schema_model`, `column`, `relationship`, `metric`, `business_rule`, `verified_example`, `refusal_rule`.

Every record carries `source_version`, `object_id`, `campus_scope`, `role_scope`, `status`, `valid_from`, `valid_to`, `sensitivity`, and `parent_id`. The retriever must filter by authorization and version before ranking. Retrieval is not the security boundary; FastAPI authorization, SQL scope injection and database RLS remain mandatory.

### Query path

1. Normalize the English prompt and classify intent: structured lookup, semantic-definition lookup, prediction, unsupported, or mixed.
2. Apply deterministic entity/metric/campus extraction and exact lookup for known terms and identifiers.
3. Retrieve lexical and dense candidates only from approved semantic records.
4. Fuse and deduplicate; rerank at most the top 20 candidates locally.
5. Select a small context set: normally 3-6 typed records, never the whole schema.
6. Ask Wren to plan against MDL objects and verified examples, not physical raw tables.
7. Validate generated SQL locally: SELECT-only, allowlisted objects, expected columns, campus scope, row/time limits, timeout and safe functions.
8. Execute using a least-privilege read-only identity and compose the response locally.
9. Abstain or route to a deterministic template when required context is missing or confidence/evaluation gates fail.

### Speed controls

- No LLM query rewrite on the default path.
- No reranker when exact metadata retrieval already returns a high-confidence hit.
- Batch dense retrieval and reranking locally; keep candidate depth bounded.
- Cache only versioned, authorization-scoped retrieval context and safe deterministic plans. Never cache raw student results across users or campuses.
- Warm the index and model at service startup; record embedding, lexical, fusion, rerank, Wren, validation and SQL timings separately.
- Use pre-aggregated Wren cubes/views for common board-demo metrics.
- Add agentic decomposition only when a query classifier predicts multi-hop benefit and the latency budget permits it.

### Local technology stance

Do not add a dedicated vector database until the corpus size and measured concurrency require it. Start with Wren's reviewable `knowledge/` and MDL source plus its local derived memory index, and place an exact lexical index beside it. Wren documents LanceDB as an optional semantic-memory backend and grep as a zero-dependency fallback. [Wren memory backends](https://docs.getwren.ai/oss/concepts/memory_system)

The retrieval adapter must hide this choice behind one contract so the project can move from a small local index to an institutional database/vector service without changing API or security behavior. Exact embedding/reranker model versions remain an implementation decision gated by the local benchmark and license review; do not hard-code a vendor model from a blog claim.

## Evaluation gate for the 200 gold prompts

Split the gold set into at least these categories:

| Category | Required checks |
|---|---|
| Metric and vocabulary | Correct metric/column/definition retrieval; synonym and exact-term cases |
| Relationship and join | Correct tables, approved relationship path and no invented joins |
| Campus/role scope | Correct filter, denial on missing/unauthorized scope, no cross-campus leakage |
| Aggregation and time | Result-set equivalence, date boundaries, null handling and pre-aggregated paths |
| Verified-example reuse | Similar question retrieves the correct approved example without copying unsafe values |
| Unsupported/adversarial | Correct abstention, prompt injection resistance, stale/contradictory definition handling |
| Latency/failure | Warm/cold p50/p95, timeout, fallback and external-model failure behavior |

Run an A/B matrix on the same prompts:

`exact lexical -> dense -> hybrid -> hybrid+reranker -> selective decomposition`

Record configuration hashes, corpus/index version, model versions, retrieved IDs, scores, reranker output, Wren prompt hash, generated SQL, validation decision, result equivalence, answer grade, latency and error/fallback outcome.

Release criteria are gates, not aspirations:

- no regression in any security or refusal category;
- retrieval recall and result correctness thresholds agreed by Junaid and domain reviewers before tuning;
- p95 demo-path response under five seconds on presentation hardware, with stage-level evidence;
- every supported prompt has a reproducible expected result shape;
- every unsupported or unsafe prompt fails closed;
- external payload inspection proves no protected data leaves the institution;
- index rebuild and rollback are tested from versioned source.

Do not import the reported 79.30%, 80% recall or 34% vendor improvement as EduQuery performance. They are external benchmark or vendor results and must remain labelled as such until reproduced on EduQuery's gold set.

## Steelman: the strongest opposing cases

### Case A - no custom RAG; use Wren MDL and deterministic templates

This is the strongest MVP argument. EduQuery's corpus is small, structured and governed. Every extra vector index adds drift, dependency, and test surface. Wren already retrieves context, validates SQL and supports a memory index. For a narrow board demo, deterministic intent templates plus MDL may be faster and easier to audit than a custom hybrid pipeline.

Decision: **adopt this as the baseline and fallback**, but keep a retrieval adapter because the semantic slice will grow and verified examples need paraphrase-aware recall.

### Case B - pure vector RAG is sufficient

It is simple, handles paraphrases, and may work well on a small static corpus. The community reports include examples of high accuracy on controlled document collections.

Decision: **retain as a benchmark arm only**. It cannot be the default for exact identifiers, status values, schema names, permission filters or SQL structure.

### Case C - GraphRAG/agentic RAG is the future-proof answer

Relationships, multi-hop questions and cross-document evidence are real needs. Google reports better factuality from planning and iterative search, and CSR-RAG shows structural/relational retrieval can help enterprise SQL.

Decision: **selective future route**, activated only by measured multi-hop misses. A graph or multi-agent system on day one would increase latency, security surface and operational burden before EduQuery has a baseline.

### Case D - use a managed cloud vector service

It reduces indexing work and can provide scale, observability and managed rerankers.

Decision: **reject for the MVP** because the approved data boundary is institutional. Reconsider only for non-sensitive semantic artifacts after a formal governance decision.

## Premortem

Assume this RAG plan failed by 2027-02-03.

| Failure cause | Likelihood | Severity | Immediate control |
|---|---:|---:|---|
| Stale MDL/metric definitions remain indexed | 4 | 5 | Versioned source, rebuild checksum, freshness alarm, rollback |
| Retriever returns the wrong table/column for a synonym | 4 | 5 | Table/column qrels, hybrid baseline, hard negatives, refusal |
| Retrieval context bypasses campus authorization | 3 | 5 | Pre-retrieval scope filter plus server-side SQL scope and RLS tests |
| Raw student data enters the corpus through a “helpful” example | 3 | 5 | Corpus schema allowlist, secret/PII scanner, review gate |
| Reranker or rewrite calls push p95 above the demo budget | 4 | 4 | Stage budgets, selective rerank, no default rewrite, timeout fallback |
| Gold prompts are too friendly and miss real ambiguity | 4 | 4 | Domain-reviewer sampling, adversarial and unsupported categories |
| A model/index upgrade improves average but breaks a critical class | 4 | 5 | Per-category regression gate and rollback artifact |
| Cached retrieval context leaks across roles/campuses | 3 | 5 | Scope/version in cache key; negative isolation tests |
| Wren version changes MDL or memory behavior | 3 | 4 | Pin version, contract tests, adapter boundary, compatibility fixture |
| External model receives protected content after redaction failure | 3 | 5 | Fail closed; outbound payload inspection; no “best effort” call |
| Live SQL or institutional network fails during demo | 4 | 4 | Sanitized deterministic fallback with visible mode label |
| Index rebuild is not reproducible | 3 | 4 | Source-only durable corpus, manifest/hash, rebuild test in CI |

Top three act-now controls: (1) retrieval/security gold fixtures before tuning, (2) versioned semantic source plus rebuild/rollback, and (3) stage-level latency and redaction gates on the secure vertical slice.

## Red team

| Stance | Attack | Likelihood | Impact | Score | Required defense |
|---|---|---:|---:|---:|---|
| Hostile attacker | Poison a knowledge/example file with instructions that override the system prompt | 3 | 5 | 15 | Signed/approved corpus, typed records, instruction stripping, prompt-injection fixtures |
| Malicious user | Ask for another campus through a paraphrase that retrieves its rules/examples | 4 | 5 | 20 | Authorization before retrieval, scope in every cache key and SQL/RLS enforcement |
| Disgruntled insider | Add a “verified” NL-to-SQL pair containing sensitive values | 3 | 5 | 15 | Reviewer identity, PII scanner, no raw values in examples, append-only audit |
| Skeptical buyer | Challenge “80% recall” as an unmeasured external claim | 5 | 4 | 20 | Label all external results; publish EduQuery per-category metrics only |
| Compliance auditor | Find protected prompt/result data in embeddings, logs or OpenRouter payloads | 3 | 5 | 15 | Corpus allowlist, outbound inspection, redacted logs, fail-closed adapter |
| Power user | Submit a huge multi-hop prompt to trigger repeated retrieval/LLM calls | 4 | 4 | 16 | Query complexity limit, bounded fan-out, deadlines, rate limit and fallback |
| Competitor | Point out that “hybrid is always better” is not proven for this corpus | 4 | 3 | 12 | Treat hybrid as an A/B candidate; accept simpler routing if it wins locally |

Top five must mitigate before release: cross-campus retrieval, untrusted corpus instructions, sensitive examples, external-data egress, and unbounded latency/DoS. Residual risk: multilingual/Urdu retrieval is deferred because the approved MVP is English-only.

## Final implementation recommendation

Build one secure vertical slice first:

`authorized English prompt -> intent/router -> exact + dense semantic retrieval -> scoped context -> Wren MDL -> local SQL validator -> read-only query -> result equivalence/answer -> redacted audit`

For the August MVP, implement only:

- Wren MDL as the semantic authority;
- reviewable local knowledge files and verified examples;
- exact metadata/lexical retrieval plus dense retrieval;
- RRF fusion and a bounded local reranker;
- deterministic routing for SQL, semantic context, unsupported and mixed intents;
- selective decomposition behind a feature flag;
- versioned evaluation traces for all 200 gold prompts;
- fail-closed privacy, authorization, validation, timeout and fallback behavior.

Do not implement GraphRAG, always-on agentic loops, raw-row embeddings, managed external vector storage, or unmeasured model swaps in the MVP. Add them only when a gold-prompt failure category proves the simpler pipeline cannot meet the agreed gate.

This recommendation preserves the approved project boundary: local RAG contains only approved semantic knowledge; Wren/FastAPI/SQL/audit stay institutional; external model calls receive only de-identified intent/schema context; Vercel remains UI/static assets only.

## Next dependency

WS-03 must freeze authenticated request/response contracts and the read-only authorization boundary before WS-04 implementation. Then Junaid and the domain reviewers should approve the semantic record schema and gold-prompt categories, while Rafay owns the retrieval authorization/redaction tests.
