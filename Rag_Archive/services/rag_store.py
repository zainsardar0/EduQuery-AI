"""Provenance-verified, local-only LanceDB policy retrieval."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import threading
from typing import Any, Dict, List, Optional, Tuple

from services.api.config import get_settings
from services.query.policy_ingest import MARKDOWN_POLICY_SOURCES


class PolicyRAGUnavailable(RuntimeError):
    """The local policy index or its provenance evidence failed closed."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def _tree_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    for file_path in sorted(path.rglob("*")):
        if file_path.is_file():
            digest.update(str(file_path.relative_to(path)).replace("\\", "/").encode())
            with file_path.open("rb") as handle:
                for block in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(block)
    return digest.hexdigest().upper()


def _resolve_model_snapshot_dir(model_root: Path) -> Path:
    candidates = [model_root, *list(model_root.rglob("snapshots")), *list(model_root.rglob("model_optimized.onnx")), *list(model_root.rglob("model.onnx"))]
    for candidate in candidates:
        if candidate.is_file() and candidate.name == "model_optimized.onnx":
            return candidate.parent
        if candidate.is_file() and candidate.name == "model.onnx":
            return candidate.parent.parent if candidate.parent.name == "onnx" else candidate.parent
        if candidate.is_dir() and (candidate / "model_optimized.onnx").exists():
            return candidate
        if candidate.is_dir() and (candidate / "model.onnx").exists():
            return candidate
        if candidate.is_dir() and (candidate / "onnx" / "model.onnx").exists():
            return candidate
    if model_root.is_dir():
        return model_root
    raise PolicyRAGUnavailable(f"No usable model snapshot found under {model_root}")


class PolicyRAGEngine:
    """Local hybrid retrieval with source-hash and line-range citations."""

    embedding_model = "BAAI/bge-small-en"
    reranker_model = "Xenova/ms-marco-MiniLM-L-6-v2"

    def __init__(self, root: Optional[Path] = None):
        settings = get_settings()
        configured = root or Path(settings.policy_rag_root)
        if not configured.is_absolute():
            configured = Path(__file__).resolve().parents[2] / configured
        self.root = configured.resolve()
        self.score_threshold = settings.policy_rag_min_rerank_score
        self._lock = threading.RLock()
        self._runtime: Optional[Dict[str, Any]] = None
        self._evidence: Optional[Dict[str, Any]] = None

    def _verify_evidence(self) -> Dict[str, Any]:
        manifest_path = self.root / "policy_index_manifest.json"
        benchmark_path = self.root / "policy_benchmark_report.json"
        qrels_path = self.root / "policy_gold_candidate.jsonl"
        if any(not path.is_file() for path in (manifest_path, benchmark_path, qrels_path)):
            raise PolicyRAGUnavailable("Markdown policy RAG provenance manifests are incomplete.")

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        benchmark = json.loads(benchmark_path.read_text(encoding="utf-8"))
        sources = manifest.get("sources")
        expected_sources = {
            artifact_id: {"filename": filename, "category": category}
            for artifact_id, filename, category in MARKDOWN_POLICY_SOURCES
        }
        actual_sources = {
            source.get("artifact_id"): {
                "filename": source.get("filename"), "category": source.get("category")
            }
            for source in sources
        } if isinstance(sources, list) else {}
        if (
            manifest.get("format_version") != 2 or manifest.get("source_format") != "markdown"
            or not isinstance(sources, list) or manifest.get("source_count") != len(sources)
            or not isinstance(manifest.get("records"), int) or manifest["records"] < 1
            or manifest.get("table") != "policy_markdown_chunks"
            or manifest.get("embedding_model") != self.embedding_model
            or actual_sources != expected_sources
        ):
            raise PolicyRAGUnavailable("Active RAG manifest is not a valid Markdown policy index.")
        if benchmark.get("manifest_sha256") != _sha256(manifest_path):
            raise PolicyRAGUnavailable("Policy benchmark is not bound to the active index manifest.")
        if benchmark.get("release_eligible") is not False:
            raise PolicyRAGUnavailable("Policy RAG release state must remain explicitly unapproved.")
        if benchmark.get("source_artifact_recall_at_3") != 1.0:
            raise PolicyRAGUnavailable("Markdown policy retrieval benchmark did not meet its required recall.")
        if manifest.get("policy_content_egress") != "none; local model execution only":
            raise PolicyRAGUnavailable("Policy RAG egress policy is not local-only.")
        if _sha256(qrels_path) != manifest.get("qrels_sha256"):
            raise PolicyRAGUnavailable("Policy benchmark label hash mismatch.")

        source_root = self.root / "source-md"
        for source in sources:
            source_path = source_root / source.get("filename", "")
            if (
                source.get("source_format") != "markdown" or not source_path.is_file()
                or _sha256(source_path) != source.get("source_sha256")
            ):
                raise PolicyRAGUnavailable(f"Markdown source hash mismatch for {source.get('artifact_id', 'unknown')}.")

        embedding_path = self.root / "local-models" / "fast-bge-small-en"
        reranker_path = self.root / "local-models" / "ms-marco-minilm-l6"
        index_path = self.root / "lancedb"
        if not embedding_path.is_dir() or not reranker_path.is_dir() or not index_path.is_dir():
            raise PolicyRAGUnavailable("Required local policy models or LanceDB index are missing.")
        if _tree_sha256(embedding_path) != manifest.get("embedding_model_package_sha256"):
            raise PolicyRAGUnavailable("Local embedding model package hash mismatch.")
        if _tree_sha256(reranker_path) != manifest.get("reranker_model_package_sha256"):
            raise PolicyRAGUnavailable("Local reranker model package hash mismatch.")
        if _tree_sha256(index_path) != manifest.get("lancedb_tree_sha256"):
            raise PolicyRAGUnavailable("LanceDB index hash mismatch.")

        return {
            "provenance_verified": True, "release_eligible": False,
            "review_status": manifest.get("status", "UNKNOWN"), "records": manifest["records"],
            "source_count": len(sources), "sources": sources, "table": manifest.get("table"),
            "categories_by_artifact": {source["artifact_id"]: source["category"] for source in sources},
        }

    def _load_runtime(self) -> Dict[str, Any]:
        with self._lock:
            if self._runtime is not None:
                return self._runtime
            self._evidence = self._verify_evidence()
            try:
                import lancedb
                from fastembed import TextEmbedding
                from fastembed.rerank.cross_encoder import TextCrossEncoder
                from lancedb.rerankers import RRFReranker
            except ImportError as exc:
                raise PolicyRAGUnavailable("Local LanceDB RAG dependencies are not installed.") from exc

            table = lancedb.connect(str(self.root / "lancedb")).open_table(str(self._evidence["table"]))
            if table.count_rows() != self._evidence["records"]:
                raise PolicyRAGUnavailable("LanceDB table count does not match the manifest.")
            embedding_model_path = _resolve_model_snapshot_dir(self.root / "local-models" / "fast-bge-small-en")
            reranker_model_path = _resolve_model_snapshot_dir(self.root / "local-models" / "ms-marco-minilm-l6")
            self._runtime = {
                "table": table,
                "embedder": TextEmbedding(model_name=self.embedding_model, providers=["CPUExecutionProvider"], specific_model_path=str(embedding_model_path)),
                "reranker": TextCrossEncoder(model_name=self.reranker_model, providers=["CPUExecutionProvider"], specific_model_path=str(reranker_model_path)),
                "rrf": RRFReranker(),
            }
            return self._runtime

    @staticmethod
    def _embed(embedder: Any, query: str) -> List[float]:
        vectors = list(embedder.embed(["query: " + query], batch_size=1))
        if len(vectors) != 1:
            raise PolicyRAGUnavailable("Local embedding runtime returned an invalid result.")
        return vectors[0].tolist()

    def search(self, query: str, top_k: int = 3, score_threshold: Optional[float] = None, category_filter: Optional[str] = None) -> Tuple[List[Dict[str, Any]], str, str]:
        clean_query = " ".join(query.split())
        if not clean_query:
            return [], "Enter a policy question.", "not_found"
        runtime = self._load_runtime()
        categories = set(self._evidence["categories_by_artifact"].values())
        if category_filter and category_filter not in categories:
            return [], "No indexed policy category matches that filter.", "not_found"
        with self._lock:
            table = runtime["table"]
            lexical = table.search(clean_query, query_type="fts", fts_columns="search_text").limit(20).to_list()
            hybrid = table.search(query_type="hybrid").vector(self._embed(runtime["embedder"], clean_query)).text(clean_query).rerank(runtime["rrf"]).limit(20).to_list()
            rows = list({row["id"]: row for row in lexical + hybrid}.values())
            if category_filter:
                rows = [row for row in rows if self._evidence["categories_by_artifact"].get(row["artifact_id"]) == category_filter]
            if not rows:
                return [], "No relevant policy evidence was found.", "not_found"
            scores = list(runtime["reranker"].rerank(clean_query, [row["text"] for row in rows], batch_size=32))
            ranked = sorted(zip(scores, rows), key=lambda item: item[0], reverse=True)

        threshold = self.score_threshold if score_threshold is None else score_threshold
        if not ranked or float(ranked[0][0]) < threshold:
            return [], "No sufficiently relevant policy evidence was found.", "not_found"
        sections = []
        for score, row in ranked[:max(1, min(top_k, 5))]:
            location = row.get("source_location") or "source location unavailable"
            sections.append({
                "section_title": f"{row['source_document']} — {location}", "excerpt": " ".join(row["text"].split())[:1200],
                "source_document": row["source_document"], "source_sha256": row["source_sha256"], "artifact_id": row["artifact_id"].replace("SRC-", "POL-"),
                "page": int(row.get("page") or 0), "source_location": location,
                "category": self._evidence["categories_by_artifact"].get(row["artifact_id"], "general"),
                "review_status": row["review_status"], "retrieval_score": round(float(score), 4),
            })
        lead = sections[0]
        excerpt = re.sub(r"\s+", " ", lead["excerpt"]).strip()[:650]
        explanation = (
            f"The strongest local matching source is {lead['source_document']} "
            f"({lead['source_location']}): {excerpt}"
        )
        return sections, explanation, "found"

    def readiness(self) -> Dict[str, Any]:
        self._load_runtime()
        return dict(self._evidence or {}) | {"retrieval_mode": "local_hybrid_reranked"}

    def get_all_documents(self) -> List[Dict[str, Any]]:
        evidence = self._evidence or self._verify_evidence()
        return [{"artifact_id": item["artifact_id"], "source_document": item["filename"], "source_sha256": item["source_sha256"], "page_count": None, "category": item["category"], "source_format": "markdown"} for item in evidence["sources"]]

    def get_categories(self) -> List[str]:
        evidence = self._evidence or self._verify_evidence()
        return sorted(set(evidence["categories_by_artifact"].values()))
