import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
from typing import Any, Dict, Iterable, List


MARKDOWN_POLICY_SOURCES = (
    ("POL-001", "Day Care Centre Policy.md", "general"),
    ("POL-002", "Day Scholars Policy.md", "admission"),
    ("POL-003", "Decision Regarding Admission of Siblings.md", "admission"),
    ("POL-004", "Induction Policy.md", "admission"),
    ("POL-005", "Late Arrival of Students Policy.md", "attendance"),
    ("POL-006", "Leave Policy.md", "leave"),
    ("POL-007", "Medical Policy for Students.md", "general"),
    ("POL-008", "Promotion Discharge Policy.md", "grading"),
    ("POL-009", "School instructions.md", "general"),
)


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
    """Hugging Face caches store ONNX checkpoints under nested snapshot folders."""
    candidates = [
        model_root,
        *list(model_root.rglob("snapshots")),
        *list(model_root.rglob("model_optimized.onnx")),
        *list(model_root.rglob("model.onnx")),
    ]
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
    raise FileNotFoundError(f"No usable model snapshot found under {model_root}")


def _paragraphs(raw_text: str) -> Iterable[tuple[int, int, int | None, str]]:
    page: int | None = None
    start = 1
    lines: list[str] = []
    for line_number, raw_line in enumerate(raw_text.splitlines(), start=1):
        page_match = re.fullmatch(r"\s*---\s*Page\s+(\d+)\s*---\s*", raw_line)
        if page_match:
            if lines:
                yield start, line_number - 1, page, " ".join(lines)
                lines = []
            page = int(page_match.group(1))
            start = line_number + 1
            continue
        line = " ".join(raw_line.split())
        if not line:
            if lines:
                yield start, line_number - 1, page, " ".join(lines)
                lines = []
            start = line_number + 1
            continue
        if not lines:
            start = line_number
        lines.append(line)
    if lines:
        yield start, len(raw_text.splitlines()), page, " ".join(lines)


def markdown_policy_chunks(raw_text: str, artifact_id: str, source_document: str, source_sha256: str) -> List[Dict[str, Any]]:
    """Create bounded, line-citable chunks without inventing PDF pages."""
    chunks: List[Dict[str, Any]] = []
    current: list[str] = []
    start_line = end_line = 0
    declared_page: int | None = None
    section_title = source_document.rsplit(".", 1)[0]

    def flush() -> None:
        nonlocal current, start_line, end_line, declared_page
        if not current:
            return
        chunk_number = len(chunks) + 1
        location = f"lines {start_line}-{end_line}"
        if declared_page is not None:
            location += f"; declared source page {declared_page}"
        text = " ".join(current)
        chunks.append({
            "id": f"{artifact_id}-{chunk_number:04d}",
            "text": text,
            "search_text": f"{section_title}. {text}",
            "artifact_id": artifact_id,
            "source_document": source_document,
            "source_sha256": source_sha256,
            "source_location": location,
            "page": declared_page or 0,
            "chunk": chunk_number,
            "review_status": "USER_SUPPLIED_MD_UNREVIEWED",
            "approval_scope": "INSTITUTIONAL_INTERNAL_UNTIL_REVIEWED",
        })
        current = []

    for para_start, para_end, page, paragraph in _paragraphs(raw_text):
        heading = re.match(r"^(?:\d+[.)]|[A-Z][A-Z /&-]{8,}:)\s*(.+)", paragraph)
        if heading and len(paragraph) < 220:
            section_title = heading.group(1).strip()
        if current and (len(" ".join(current)) + len(paragraph) > 1100 or page != declared_page):
            flush()
        if not current:
            start_line, declared_page = para_start, page
        current.append(paragraph)
        end_line = para_end
    flush()
    return chunks


def build_markdown_policy_index(source_dir: Path, output_root: Path, model_root: Path) -> Dict[str, Any]:
    """Copy authoritative Markdown, build a local-only LanceDB index, and seal it with hashes."""
    source_dir, output_root, model_root = source_dir.resolve(), output_root.resolve(), model_root.resolve()
    if output_root.exists():
        raise ValueError(f"Refusing to overwrite existing policy index: {output_root}")
    expected = {name for _, name, _ in MARKDOWN_POLICY_SOURCES}
    actual = {path.name for path in source_dir.glob("*.md")}
    if actual != expected:
        raise ValueError(f"Markdown source set mismatch; missing={sorted(expected - actual)} extra={sorted(actual - expected)}")
    required_models = (model_root / "fast-bge-small-en", model_root / "ms-marco-minilm-l6")
    if any(not path.is_dir() for path in required_models):
        raise ValueError("Required local embedding or reranker model package is missing.")

    os.environ.setdefault("HF_HUB_OFFLINE", "1")
    import lancedb
    from fastembed import TextEmbedding
    from lancedb.index import FTS

    output_root.mkdir(parents=True)
    copied_sources = output_root / "source-md"
    copied_sources.mkdir()
    records: list[dict[str, Any]] = []
    source_records: list[dict[str, Any]] = []
    for artifact_id, filename, category in MARKDOWN_POLICY_SOURCES:
        source_path = source_dir / filename
        copied_path = copied_sources / filename
        shutil.copy2(source_path, copied_path)
        source_hash = _sha256(copied_path)
        source_records.append({
            "artifact_id": artifact_id,
            "filename": filename,
            "source_sha256": source_hash,
            "category": category,
            "source_format": "markdown",
        })
        records.extend(markdown_policy_chunks(copied_path.read_text(encoding="utf-8"), artifact_id, filename, source_hash))
    if not records:
        raise ValueError("Markdown policy source produced no indexable chunks.")

    local_models = output_root / "local-models"
    shutil.copytree(model_root, local_models)
    embedding_path = _resolve_model_snapshot_dir(local_models / "fast-bge-small-en")
    embedder = TextEmbedding(
        model_name="BAAI/bge-small-en",
        providers=["CPUExecutionProvider"],
        specific_model_path=str(embedding_path),
    )
    vectors = [vector.tolist() for vector in embedder.embed(["passage: " + row["search_text"] for row in records], batch_size=32)]
    if len(vectors) != len(records) or not vectors:
        raise RuntimeError("Local embedding did not return one vector per policy chunk.")
    indexed_records = [row | {"vector": vector, "embedding_model": "BAAI/bge-small-en"} for row, vector in zip(records, vectors)]
    db_root = output_root / "lancedb"
    table = lancedb.connect(str(db_root)).create_table("policy_markdown_chunks", data=indexed_records, mode="create")
    table.create_index("search_text", config=FTS(language="English"))

    qrels = [
        {"id": "md-day-care", "query": "Who can use a Daanish School day care centre?", "expected_artifact_id": "POL-001"},
        {"id": "md-sibling", "query": "Can siblings be admitted to Daanish School?", "expected_artifact_id": "POL-003"},
        {"id": "md-day-scholar", "query": "What is the day scholar admission policy?", "expected_artifact_id": "POL-002"},
        {"id": "md-induction", "query": "What is the Daanish School induction policy?", "expected_artifact_id": "POL-004"},
        {"id": "md-late", "query": "What happens when a student returns late from leave?", "expected_artifact_id": "POL-005"},
        {"id": "md-leave", "query": "What are the boarder leave rules?", "expected_artifact_id": "POL-006"},
        {"id": "md-medical", "query": "What medical policy applies to students?", "expected_artifact_id": "POL-007"},
        {"id": "md-promotion", "query": "What are the promotion and discharge rules?", "expected_artifact_id": "POL-008"},
        {"id": "md-instructions", "query": "What mandatory attendance percentage is required by school instructions?", "expected_artifact_id": "POL-009"},
    ]
    qrels_path = output_root / "policy_gold_candidate.jsonl"
    qrels_path.write_text("".join(json.dumps(item) + "\n" for item in qrels), encoding="utf-8")
    hits = 0
    for case in qrels:
        vector = next(embedder.embed(["query: " + case["query"]], batch_size=1)).tolist()
        rows = table.search(query_type="hybrid").vector(vector).text(case["query"]).limit(3).to_list()
        hits += int(any(row["artifact_id"] == case["expected_artifact_id"] for row in rows))
    if hits != len(qrels):
        raise RuntimeError(f"Markdown policy retrieval gate failed: {hits}/{len(qrels)} expected artifacts found at 3.")

    manifest = {
        "format_version": 2,
        "status": "DRAFT_ONLY_NOT_RELEASE_ELIGIBLE",
        "source_format": "markdown",
        "table": "policy_markdown_chunks",
        "records": len(indexed_records),
        "source_count": len(source_records),
        "sources": source_records,
        "embedding_model": "BAAI/bge-small-en",
        "embedding_model_package_sha256": _tree_sha256(embedding_path),
        "reranker_model_package_sha256": _tree_sha256(local_models / "ms-marco-minilm-l6"),
        "lancedb_tree_sha256": _tree_sha256(db_root),
        "qrels_sha256": _sha256(qrels_path),
        "policy_content_egress": "none; local model execution only",
    }
    manifest_path = output_root / "policy_index_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    benchmark = {
        "status": "MECHANICS_VERIFIED_ONLY",
        "release_eligible": False,
        "manifest_sha256": _sha256(manifest_path),
        "candidate_cases": len(qrels),
        "source_artifact_recall_at_3": hits / len(qrels),
        "reason": "MD source integrity and retrieval mechanics are verified; named Daanish domain review is still required.",
    }
    (output_root / "policy_benchmark_report.json").write_text(json.dumps(benchmark, indent=2) + "\n", encoding="utf-8")
    return manifest | {"benchmark": benchmark}


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a local-only LanceDB index from approved Markdown policy files.")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model-root", type=Path, required=True)
    args = parser.parse_args()
    result = build_markdown_policy_index(args.source, args.output, args.model_root)
    print(json.dumps({"records": result["records"], "sources": result["source_count"], "status": result["status"]}, indent=2))


if __name__ == "__main__":
    main()


def parse_policy_text_into_chunks(raw_text: str, source_doc: str) -> List[Dict[str, Any]]:
    """
    Parses policy document text into semantic section chunks along section header boundaries.
    Preserves document title, section title, page numbers, and verbatim excerpts.
    """
    sections: List[Dict[str, Any]] = []
    current_section_title = "General Policy"
    current_page = 1
    section_start_page = 1
    current_lines: List[str] = []

    lines = raw_text.splitlines()
    for line in lines:
        page_match = re.search(r"--- Page (\d+) ---", line)
        if page_match:
            current_page = int(page_match.group(1))
            continue

        header_match = re.match(r"^(Section\s+\d+(\.\d+)?\s*[\u2013\-:]\s*.+)$", line.strip(), re.IGNORECASE)
        if header_match:
            if current_lines:
                sections.append(
                    {
                        "section_title": current_section_title,
                        "excerpt": " ".join(current_lines).strip(),
                        "source_document": source_doc,
                        "page": section_start_page,
                    }
                )
                current_lines = []
            current_section_title = header_match.group(1)
            section_start_page = current_page
        else:
            if line.strip():
                current_lines.append(line.strip())

    if current_lines:
        sections.append(
            {
                "section_title": current_section_title,
                "excerpt": " ".join(current_lines).strip(),
                "source_document": source_doc,
                "page": section_start_page,
            }
        )

    return sections
