"""Chunk markdown files into fixed-size text chunks and save as JSON for RAG."""
import os
import glob
import json
import argparse
from typing import List


def chunk_text(text: str, max_words: int = 250) -> List[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i : i + max_words])
        chunks.append(chunk)
    return chunks


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--indir", "-i", default="docs/08-rag-data-md")
    p.add_argument("--out", "-o", default="data/rag_chunks.json")
    p.add_argument("--words", "-w", type=int, default=250)
    args = p.parse_args(argv)

    paths = glob.glob(os.path.join(args.indir, "*.md"))
    if not paths:
        print("No markdown files in", args.indir)
        return

    all_chunks = []
    for fp in paths:
        name = os.path.basename(fp)
        with open(fp, "r", encoding="utf-8") as f:
            md = f.read()
        # split by page markers
        pages = md.split("--- Page ")
        for p in pages:
            if not p.strip():
                continue
            # p starts like '1 ---\n...'
            try:
                header, body = p.split("---", 1)
                page_num = int(header.strip())
            except Exception:
                page_num = 0
                body = p
            body = body.strip()
            for i, chunk in enumerate(chunk_text(body, args.words)):
                all_chunks.append({
                    "source": name,
                    "page": page_num,
                    "chunk_id": f"{name}::p{page_num}::c{i}",
                    "text": chunk,
                })

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)
    print("Wrote", len(all_chunks), "chunks to", args.out)


if __name__ == "__main__":
    main()
