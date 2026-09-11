"""RAG router: query -> embedding -> LanceDB search -> synthesize via OpenRouter.

Endpoints:
- POST /rag/query {"query": "...", "top_k": 5}
- POST /rag/reindex (protected by ADMIN_API_KEY) triggers reindex from data/rag_sources

This router relies on:
- services.api.config.get_settings() for OPENAI key, LANCE path, embedding model
- services.api.privacy.openrouter_client.OpenRouterClient for generation (respects privacy redaction)
- scripts.index_to_lancedb.index_folder for indexing (local script)

Note: Ensure lance and openai are installed in the environment where this runs.
"""
from typing import Any, Dict, List
import os
import time
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel

from services.api.config import get_settings
from services.api.privacy.openrouter_client_impl import OpenRouterClient

import asyncio

try:
    # Use the local policy RAG engine for embeddings and retrieval
    from services.query.rag_store import PolicyRAGEngine, PolicyRAGUnavailable
except Exception:  # pragma: no cover
    PolicyRAGEngine = None
    PolicyRAGUnavailable = Exception

router = APIRouter(prefix="/rag", tags=["RAG"])

settings = get_settings()
openrouter = OpenRouterClient()


class QueryRequest(BaseModel):
    query: str
    top_k: int = 5


class QueryResponse(BaseModel):
    status: str
    answer: str
    sources: List[Dict[str, Any]]
    meta: Dict[str, Any] = {}


@router.post("/query", response_model=QueryResponse)
async def rag_query(req: QueryRequest):
    if not req.query or not req.query.strip():
        raise HTTPException(status_code=400, detail="empty query")

    # Prefer local PolicyRAGEngine for retrieval (embeddings, LanceDB, reranker)
    if PolicyRAGEngine is None:
        raise HTTPException(status_code=500, detail="Local PolicyRAG engine is not available on server")

    engine = PolicyRAGEngine()
    try:
        sections, explanation, status_str = engine.search(req.query, top_k=req.top_k)
    except PolicyRAGUnavailable as e:
        raise HTTPException(status_code=500, detail=f"RAG engine unavailable: {e}")

    if not sections:
        return {"status": status_str, "answer": explanation, "sources": [], "meta": {"retrieved_count": 0}}

    # Build context from top sections
    top_texts = []
    sources = []
    for s in sections[:5]:
        src = s.get("source_document") or s.get("artifact_id")
        excerpt = s.get("excerpt", "")
        sources.append({"score": s.get("retrieval_score"), "source": src})
        top_texts.append(f"Source: {src}\nText:\n{excerpt}\n---\n")

    context = "\n".join(top_texts)
    system_prompt = (
        "You are an assistant that answers queries using only the provided policy excerpts. "
        "Cite sources by filename. If the answer is not found in the excerpts, say you could not find relevant information."
    )
    user_prompt = f"Policy context:\n{context}\n\nUser question:\n{req.query}\n\nAnswer concisely and list source filenames."

    # Try local generator (Ollama) first, then fall back to institutional OpenRouter if configured
    assistant_msg = ""
    try:
        from services.api.privacy.local_generator import generate_completion as local_generate
    except Exception:
        local_generate = None

    if local_generate is not None:
        # run blocking generator in thread
        try:
            assistant_msg = await asyncio.to_thread(local_generate, user_prompt, system_prompt, settings)
        except Exception as e:
            # fallback to openrouter
            assistant_msg = f"[local generator failed: {e}]"

    if not assistant_msg or assistant_msg.startswith("[local generator failed"):
        # fallback to OpenRouterClient (external) if allowed
        if settings.external_model_enabled:
            gen = await openrouter.generate_completion(user_prompt, system_prompt=system_prompt)
            try:
                choices = gen.get("choices", [])
                if choices and choices[0].get("message"):
                    assistant_msg = choices[0]["message"].get("content", "")
                elif choices and choices[0].get("text"):
                    assistant_msg = choices[0].get("text", "")
                else:
                    assistant_msg = str(gen)
            except Exception:
                assistant_msg = str(gen)
        else:
            # No generator available; return retrieval explanation only
            assistant_msg = explanation

    return {
        "status": "found" if sections else "not_found",
        "answer": assistant_msg,
        "sources": sources,
        "meta": {"retrieved_count": len(sources)},
    }


@router.post("/reindex")
def reindex(request: Request):
    # Simple admin protection via header 'x-admin-key' or env ADMIN_API_KEY
    admin_key = request.headers.get("x-admin-key")
    configured = os.environ.get("ADMIN_API_KEY") or settings.admin_api_key
    if not configured or admin_key != configured:
        raise HTTPException(status_code=403, detail="admin key required")

    # Run the indexer (import the indexer function)
    try:
        from scripts.index_to_lancedb import index_folder
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indexer not available: {e}")

    src = os.environ.get("RAG_SOURCES_PATH", "data/rag_sources")
    out = os.environ.get("LANCEDB_PATH", settings.lancedb_path)
    emb_model = os.environ.get("EMBEDDING_MODEL", settings.embedding_model)
    batch = int(os.environ.get("EMBEDDING_BATCH", settings.embedding_batch_size))
    api_key = os.environ.get("OPENAI_API_KEY") or settings.openai_api_key
    try:
        index_folder(src, out, emb_model, batch, api_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indexing failed: {e}")

    return {"status": "ok", "indexed_path": out}
