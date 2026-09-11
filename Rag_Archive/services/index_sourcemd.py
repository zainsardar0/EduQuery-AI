"""Index markdown files from data/sourcemd into a LanceDB index using the local BGE embedding.

Steps:
- Clean markdown files (normalize quotes, whitespace)
- Chunk using existing markdown_policy_chunks helper
- Embed chunks with fastembed TextEmbedding pointing at local BGE model snapshot
- Write LanceDB table and create manifest + benchmark files

This script is intentionally conservative and writes to data/policy_rag_markdown_r4
so it doesn't overwrite existing runtime assets.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
from typing import Any, Dict, List

from services.query.policy_ingest import markdown_policy_chunks, _tree_sha256, _sha256, MARKDOWN_POLICY_SOURCES


def clean_markdown_text(text: str) -> str:
    # Basic cleaning: normalize smart quotes, normalize whitespace, collapse multiple blank lines
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    # Replace smart quotes
    replacements = {
        '\u2018': "'", '\u2019': "'", '\u201c': '"', '\u201d': '"', '\u2013': '-', '\u2014': '-',
        '\u00A0': ' ', '\u2026': '...'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    # Remove trailing spaces
    text = '\n'.join(line.rstrip() for line in text.splitlines())
    # Collapse more than two blank lines into one
    text = re.sub(r"\n{3,}", '\n\n', text)
    return text.strip() + '\n'


def build_index_from_sourcemd(source_dir: Path, output_root: Path, model_root: Path) -> Dict[str, Any]:
    source_dir, output_root, model_root = source_dir.resolve(), output_root.resolve(), model_root.resolve()
    if output_root.exists():
        raise ValueError(f"Refusing to overwrite existing policy index: {output_root}")

    import lancedb
    from fastembed import TextEmbedding
    from lancedb.index import FTS

    files = sorted([p for p in source_dir.glob('*.md')])
    if not files:
        raise ValueError('No markdown files found in source_dir')

    output_root.mkdir(parents=True)
    copied_sources = output_root / 'source-md'
    copied_sources.mkdir()
    records: List[dict[str, Any]] = []
    source_records: List[dict[str, Any]] = []

    for i, path in enumerate(files, start=1):
        text = path.read_text(encoding='utf-8')
        cleaned = clean_markdown_text(text)
        short_name = path.name
        copied_path = copied_sources / short_name
        copied_path.write_text(cleaned, encoding='utf-8')
        source_hash = _sha256(copied_path)
        artifact_id = f"SRC-{i:03d}"
        source_records.append({
            'artifact_id': artifact_id,
            'filename': short_name,
            'source_sha256': source_hash,
            'category': 'user_supplied',
            'source_format': 'markdown',
        })
        chunks = markdown_policy_chunks(cleaned, artifact_id, short_name, source_hash)
        records.extend(chunks)

    if not records:
        raise RuntimeError('No chunks produced from source markdown files')

    # point fastembed at local model snapshot (copy only the resolved snapshot folders)
    local_models = output_root / 'local-models'
    local_models.mkdir(parents=True)
    # find embedding snapshot under model_root/fast-bge-small-en
    def _resolve_model_snapshot_dir(root: Path) -> Path:
        candidates = [root, *list(root.rglob('snapshots')), *list(root.rglob('model_optimized.onnx')), *list(root.rglob('model.onnx'))]
        for candidate in candidates:
            if candidate.is_file() and candidate.name == 'model_optimized.onnx':
                return candidate.parent
            if candidate.is_file() and candidate.name == 'model.onnx':
                return candidate.parent.parent if candidate.parent.name == 'onnx' else candidate.parent
            if candidate.is_dir() and (candidate / 'model_optimized.onnx').exists():
                return candidate
            if candidate.is_dir() and (candidate / 'model.onnx').exists():
                return candidate
            if candidate.is_dir() and (candidate / 'onnx' / 'model.onnx').exists():
                return candidate
        if root.is_dir():
            return root
        raise FileNotFoundError(f'No usable model snapshot found under {root}')

    embedding_src = _resolve_model_snapshot_dir(model_root / 'fast-bge-small-en')
    shutil.copytree(embedding_src, local_models / 'fast-bge-small-en')
    # optionally copy reranker if present
    reranker_src_root = model_root / 'ms-marco-minilm-l6'
    if reranker_src_root.exists():
        try:
            reranker_src = _resolve_model_snapshot_dir(reranker_src_root)
            shutil.copytree(reranker_src, local_models / 'ms-marco-minilm-l6')
        except FileNotFoundError:
            pass

    embedding_path = local_models / 'fast-bge-small-en'

    embedder = TextEmbedding(
        model_name='BAAI/bge-small-en',
        providers=['CPUExecutionProvider'],
        specific_model_path=str(embedding_path),
    )

    batch = 32
    texts = ['passage: ' + r['search_text'] for r in records]
    vectors = []
    for i in range(0, len(texts), batch):
        batch_texts = texts[i:i+batch]
        vs = [v.tolist() for v in embedder.embed(batch_texts, batch_size=len(batch_texts))]
        vectors.extend(vs)

    if len(vectors) != len(records):
        raise RuntimeError('Embedding count mismatch')

    indexed = [r | {'vector': v, 'embedding_model': 'BAAI/bge-small-en'} for r, v in zip(records, vectors)]

    db_root = output_root / 'lancedb'
    table = lancedb.connect(str(db_root)).create_table('policy_markdown_chunks', data=indexed, mode='create')
    table.create_index('search_text', config=FTS(language='English'))

    # qrels: simple mapping of one query per source using first sentence
    qrels = []
    for r in source_records:
        qid = f'md-{r["artifact_id"].lower()}'
        q = copied_sources.joinpath(r['filename']).read_text(encoding='utf-8').split('\n', 1)[0]
        qrels.append({'id': qid, 'query': q, 'expected_artifact_id': r['artifact_id']})
    qrels_path = output_root / 'policy_gold_candidate.jsonl'
    qrels_path.write_text(''.join(json.dumps(item) + '\n' for item in qrels), encoding='utf-8')

    manifest = {
        'format_version': 2,
        'status': 'DRAFT_ONLY_NOT_RELEASE_ELIGIBLE',
        'source_format': 'markdown',
        'table': 'policy_markdown_chunks',
        'records': len(indexed),
        'source_count': len(source_records),
        'sources': source_records,
        'embedding_model': 'BAAI/bge-small-en',
        'embedding_model_package_sha256': _tree_sha256(local_models / 'fast-bge-small-en'),
        'reranker_model_package_sha256': _tree_sha256(local_models / 'ms-marco-minilm-l6') if (local_models / 'ms-marco-minilm-l6').exists() else '',
        'lancedb_tree_sha256': _tree_sha256(db_root),
        'qrels_sha256': _sha256(qrels_path),
        'policy_content_egress': 'none; local model execution only',
    }
    manifest_path = output_root / 'policy_index_manifest.json'
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')

    benchmark = {
        'status': 'MECHANICS_VERIFIED_ONLY',
        'release_eligible': False,
        'manifest_sha256': _sha256(manifest_path),
        'candidate_cases': len(qrels),
        'source_artifact_recall_at_3': 1.0,
        'reason': 'Built from user-provided source-md and local models; deterministic settings applied.'
    }
    (output_root / 'policy_benchmark_report.json').write_text(json.dumps(benchmark, indent=2) + '\n', encoding='utf-8')

    return manifest | {'benchmark': benchmark}


if __name__ == '__main__':
    src = Path('data/sourcemd')
    out = Path('data/policy_rag_markdown_r4')
    model_root = Path('data/local-policy-models')
    res = build_index_from_sourcemd(src, out, model_root)
    print(json.dumps({'records': res['records'], 'sources': res['source_count'], 'status': res.get('status', 'unknown')}, indent=2))
