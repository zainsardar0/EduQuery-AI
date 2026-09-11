RAG Upgrade — LanceDB + OpenAI embeddings + OpenRouter

This folder contains the new RAG workflow and instructions.

Files added:
- data/rag_sources/ — policy markdown sources (imported from local path)
- scripts/index_to_lancedb.py — indexer that computes OpenAI embeddings and writes a LanceDB dataset
- services/api/routers/rag_router.py — FastAPI router to query LanceDB and synthesize via OpenRouter

How to index locally
1. Install dependencies: pip install lance pyarrow numpy pandas tqdm sentence-transformers httpx
2. Choose embedding provider and set credentials in environment or pass CLI flags.
   - BAAI (bge-m3) — set BAAI_API_KEY (environment) and provide --baai_url when running the indexer. Example: export BAAI_API_KEY=...; python scripts/index_to_lancedb.py --provider baai --model bge-m3 --baai_url https://api.baai.example.com/v1/embeddings
   - OpenAI — set OPENAI_API_KEY and run with --provider openai --model text-embedding-3-large
   - Local (no external API) — use sentence-transformers model: --provider local --model all-mpnet-base-v2
3. Run (example using BAAI):
   python scripts/index_to_lancedb.py --source data/rag_sources --out ./data/lancedb --provider baai --model bge-m3 --baai_url https://api.baai.example.com/v1/embeddings

Notes:
- The indexer supports three providers: 'baai', 'openai', and 'local'. BAAI requires a provider-specific endpoint URL and API key.
- Indexer overwrites the LanceDB dataset by default.
- Do not commit API keys into the repo. Use services/api/.env or OS environment variables.

Running the server
- The RAG router is mounted at /rag (POST /rag/query and POST /rag/reindex).
- Protect /rag/reindex by setting ADMIN_API_KEY in environment and passing header x-admin-key.

Frontend example (fetch)

fetch('/api/v1/rag/query', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'What is the leave policy for boarders?', top_k: 5 })
}).then(r => r.json()).then(console.log)

Notes
- The indexer currently overwrites the LanceDB dataset; for production consider incremental upserts and checksums per source file.
- OpenAI embedding usage is billable. Monitor costs.
- Ensure privacy redaction is applied before sending any sensitive text to external LLMs (the OpenRouter client already applies the privacy gate).
