"""Index markdown source files into LanceDB using OpenAI embeddings.

Usage:
  python scripts/index_to_lancedb.py --source data/rag_sources --out ./data/lancedb

Notes:
- Requires OPENAI_API_KEY in environment or configured via services/api config.
- Install dependencies: pip install openai lance pyarrow numpy tqdm
- This script overwrites the target LanceDB dataset by default.
"""
import os
import argparse
import glob
import json
import time
from typing import List

try:
    import openai
except Exception:  # pragma: no cover
    openai = None

try:
    import lance
    import pyarrow as pa
    import numpy as np
except Exception:  # pragma: no cover
    lance = None


def read_markdown_files(source_dir: str) -> List[dict]:
    md_paths = sorted(glob.glob(os.path.join(source_dir, "*.md")))
    docs = []
    for p in md_paths:
        with open(p, "r", encoding="utf-8") as f:
            text = f.read()
        docs.append({"source": os.path.basename(p), "text": text})
    return docs


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200):
    # simple character-based chunker. For better results use token-based approach.
    chunks = []
    start = 0
    L = len(text)
    while start < L:
        end = min(start + chunk_size, L)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - overlap
        if start < 0:
            start = 0
        if start >= L:
            break
    return chunks


def compute_embeddings_openai(texts: List[str], model: str, batch_size: int = 64, api_key: str = None) -> List[List[float]]:
    if openai is None:
        raise RuntimeError("openai package not installed. pip install openai")
    if api_key:
        openai.api_key = api_key

    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        resp = openai.Embedding.create(model=model, input=batch)
        batch_emb = [r["embedding"] for r in resp["data"]]
        embeddings.extend(batch_emb)
        time.sleep(0.1)
    return embeddings


def compute_embeddings_baai(texts: List[str], model: str, batch_size: int = 64, api_key: str = None, baai_url: str = None) -> List[List[float]]:
    """Call a generic BAAI-compatible embedding endpoint.
    Requires BAAI_API_KEY in api_key and a BAAI_EMBED_URL (baai_url) that accepts JSON {"model":"bge-m3","input": [...]}
    and returns {"data":[{"embedding": [...]}, ...]}
    """
    try:
        import httpx
    except Exception:
        raise RuntimeError("httpx is required for BAAI embedding calls: pip install httpx")
    if not api_key or not baai_url:
        raise RuntimeError("BAAI provider requires api_key and baai_url")

    embeddings = []
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        payload = {"model": model, "input": batch}
        resp = httpx.post(baai_url, json=payload, headers=headers, timeout=30.0)
        resp.raise_for_status()
        data = resp.json()
        # Expecting structure similar to OpenAI: data -> list of {embedding: [...]}
        batch_emb = [item.get("embedding") or item.get("vector") for item in data.get("data", [])]
        embeddings.extend(batch_emb)
        time.sleep(0.1)
    return embeddings


def compute_embeddings_local(texts: List[str], model_name: str, batch_size: int = 64) -> List[List[float]]:
    try:
        from sentence_transformers import SentenceTransformer
    except Exception:
        raise RuntimeError("sentence-transformers not installed. pip install sentence-transformers")
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
    return [list(vec) for vec in embeddings]


def compute_embeddings(texts: List[str], provider: str, model: str, batch_size: int = 64, api_key: str = None, baai_url: str = None) -> List[List[float]]:
    """Unified embedding entrypoint. provider in {'openai','baai','local'}"""
    provider = provider.lower()
    if provider == 'openai':
        return compute_embeddings_openai(texts, model=model, batch_size=batch_size, api_key=api_key)
    if provider == 'baai':
        return compute_embeddings_baai(texts, model=model, batch_size=batch_size, api_key=api_key, baai_url=baai_url)
    if provider == 'local':
        return compute_embeddings_local(texts, model, batch_size=batch_size)
    raise RuntimeError(f"Unknown embedding provider: {provider}")



def build_lancedb(docs: List[dict], out_path: str, provider: str, embedding_model: str, batch_size: int, api_key: str, baai_url: str = None):
    if lance is None:
        raise RuntimeError("lance (LanceDB) not installed. pip install lance")

    rows = {
        "chunk_id": [],
        "source": [],
        "text": [],
    }
    texts = []
    for doc in docs:
        source = doc["source"]
        for i, chunk in enumerate(chunk_text(doc["text"])):
            cid = f"{source}::chunk::{i}"
            rows["chunk_id"].append(cid)
            rows["source"].append(source)
            rows["text"].append(chunk)
            texts.append(chunk)

    print(f"Computed {len(texts)} chunks — computing embeddings (provider={provider}, model={embedding_model})...")
    embs = compute_embeddings(texts, provider=provider, model=embedding_model, batch_size=batch_size, api_key=api_key, baai_url=baai_url)
    embs_arr = np.array(embs, dtype=np.float32)

    import pandas as pd

    df = pd.DataFrame({
        "chunk_id": rows["chunk_id"],
        "source": rows["source"],
        "text": rows["text"],
    })
    ds = lance.write_dataset(
        df,
        out_path,
        mode="overwrite",
        vectors={"embedding": embs_arr},
    )
    print(f"Wrote LanceDB dataset to {out_path}")
    return ds



def index_folder(source: str, out_path: str, provider: str, embedding_model: str, batch_size: int, api_key: str, baai_url: str = None):
    docs = read_markdown_files(source)
    if not docs:
        raise RuntimeError(f"No markdown files found in {source}")
    ds = build_lancedb(docs, out_path, provider, embedding_model, batch_size, api_key, baai_url=baai_url)
    return ds


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--source", default="data/rag_sources")
    p.add_argument("--out", default="./data/lancedb")
    p.add_argument("--provider", default="baai", help="Embedding provider: baai | openai | local")
    p.add_argument("--model", default="bge-m3", help="Embedding model name (provider-specific)")
    p.add_argument("--batch", type=int, default=64)
    p.add_argument("--baai_url", default=None, help="BAAI embedding endpoint URL (when provider=baai)")
    args = p.parse_args(argv)

    provider = args.provider.lower()
    api_key = None
    baai_url = args.baai_url
    if provider == 'openai':
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            print("OPENAI_API_KEY not set in environment. Aborting.")
            return
    elif provider == 'baai':
        api_key = os.environ.get("BAAI_API_KEY") or os.environ.get("BGE_API_KEY")
        if not api_key:
            print("BAAI_API_KEY not set in environment. Aborting.")
            return
        if not baai_url:
            print("BAAI embedding endpoint (--baai_url) not provided. Aborting.")
            return
    elif provider == 'local':
        # no api_key required
        api_key = None
    else:
        print(f"Unknown provider: {provider}")
        return

    index_folder(args.source, args.out, provider, args.model, args.batch, api_key, baai_url=baai_url)


if __name__ == "__main__":
    main()
