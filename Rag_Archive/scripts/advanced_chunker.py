"""Create overlapping sentence-window chunks from markdown files for better RAG recall.
Outputs JSON array of chunks to `data/overlap_chunks.json` by default.
"""
import os
import glob
import json
import argparse
import re
from typing import List


def split_into_sentences(text: str) -> List[str]:
    # naive sentence splitter
    sentences = re.split(r'(?<=[.!?])\s+', text.replace('\n', ' ').strip())
    return [s.strip() for s in sentences if s.strip()]


def make_overlapping_chunks(sentences: List[str], window: int = 6, overlap: int = 2) -> List[str]:
    chunks = []
    i = 0
    n = len(sentences)
    if n == 0:
        return []
    while i < n:
        window_end = min(i + window, n)
        chunk = ' '.join(sentences[i:window_end])
        chunks.append(chunk)
        if window_end == n:
            break
        i += window - overlap
    return chunks


def process_markdown_dir(indir: str, outpath: str, window: int = 6, overlap: int = 2):
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    md_files = glob.glob(os.path.join(indir, '*.md'))
    all_chunks = []
    for fp in md_files:
        name = os.path.basename(fp)
        with open(fp, 'r', encoding='utf-8') as f:
            text = f.read()
        # split by page markers if present
        pages = re.split(r'---\s*Page\s+\d+\s*---', text)
        for pi, page_text in enumerate(pages, start=1):
            sents = split_into_sentences(page_text)
            for ci, chunk in enumerate(make_overlapping_chunks(sents, window, overlap)):
                all_chunks.append({
                    'source': name,
                    'page': pi,
                    'chunk_id': f'{name}::p{pi}::c{ci}',
                    'text': chunk,
                })

    with open(outpath, 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)
    print(f'Wrote {len(all_chunks)} chunks to {outpath}')


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--indir', '-i', default='docs/08-rag-data-md')
    p.add_argument('--out', '-o', default='data/overlap_chunks.json')
    p.add_argument('--window', type=int, default=6)
    p.add_argument('--overlap', type=int, default=2)
    args = p.parse_args(argv)
    process_markdown_dir(args.indir, args.out, args.window, args.overlap)


if __name__ == '__main__':
    main()
