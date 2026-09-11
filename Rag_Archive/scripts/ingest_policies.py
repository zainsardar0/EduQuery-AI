"""Ingest policy PDF files into semantic chunks for the PolicyRAGEngine.

Usage:
  python scripts/ingest_policies.py --input docs/policies/*.pdf --out data/policy_chunks.json --sample

The script tries PyMuPDF (fitz) first, then pdfplumber, then PyPDF2 to extract per-page text.
"""
import argparse
import glob
import json
import os
from typing import List

from services.query.policy_ingest import parse_policy_text_into_chunks


def extract_text_with_pypdf2(path: str) -> List[str]:
    try:
        from PyPDF2 import PdfReader
    except Exception:
        raise
    reader = PdfReader(path)
    pages = []
    for p in reader.pages:
        try:
            text = p.extract_text() or ""
        except Exception:
            text = ""
        pages.append(text)
    return pages


def extract_text_with_fitx(path: str) -> List[str]:
    import fitz

    doc = fitz.open(path)
    pages = [doc.load_page(i).get_text("text") for i in range(doc.page_count)]
    doc.close()
    return pages


def extract_text_with_pdfplumber(path: str) -> List[str]:
    import pdfplumber

    pages = []
    with pdfplumber.open(path) as pdf:
        for p in pdf.pages:
            pages.append(p.extract_text() or "")
    return pages


def extract_pages(path: str) -> List[str]:
    # Try libraries in order of quality
    for fn in (extract_text_with_fitx, extract_text_with_pdfplumber, extract_text_with_pypdf2):
        try:
            return fn(path)
        except ModuleNotFoundError:
            continue
        except Exception:
            # try next
            continue
    raise RuntimeError("No PDF extraction library available. Install PyMuPDF, pdfplumber, or PyPDF2.")


def pages_to_raw_text(pages: List[str]) -> str:
    out_lines = []
    for i, p in enumerate(pages, start=1):
        out_lines.append(f"--- Page {i} ---")
        out_lines.append(p)
    return "\n".join(out_lines)


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--input", "-i", required=True, help="Input file glob or comma-separated list of files")
    p.add_argument("--out", "-o", default="data/policy_chunks.json", help="Output JSON file path")
    p.add_argument("--sample", action="store_true", help="Run a sample search after ingest")
    args = p.parse_args(argv)

    inputs = []
    for part in args.input.split(","):
        part = part.strip()
        inputs.extend(glob.glob(part))

    if not inputs:
        print("No input files found for pattern:", args.input)
        return

    all_chunks = []
    for fp in inputs:
        print("Processing:", fp)
        pages = extract_pages(fp)
        raw = pages_to_raw_text(pages)
        src = os.path.basename(fp)
        chunks = parse_policy_text_into_chunks(raw, src)
        for c in chunks:
            c.setdefault("category", "policy")
        all_chunks.extend(chunks)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(all_chunks)} chunks to {args.out}")

    if args.sample:
        try:
            from services.query.rag_store import PolicyRAGEngine

            engine = PolicyRAGEngine(all_chunks)
            q = input("Sample query> ").strip()
            results, explanation, status = engine.search(q)
            print("Status:", status)
            print("Explanation:", explanation)
            print("Top results:")
            for r in results:
                print("-", r.get("section_title"), "from", r.get("source_document"), "page", r.get("page"))
        except Exception as e:
            print("Could not run sample search:", e)


if __name__ == "__main__":
    main()
