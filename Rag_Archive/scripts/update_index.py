"""Convenience CLI to run the overlap chunker and rebuild the FAISS index.

Usage examples:
  python scripts/update_index.py --indir docs/08-rag-data-md --chunks data/overlap_chunks.json --index data/faiss_index.idx --meta data/faiss_meta.json
"""
import argparse
import subprocess
import sys


def run(cmd):
    print('Running:', ' '.join(cmd))
    subprocess.check_call(cmd)


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--indir', '-i', default='docs/08-rag-data-md')
    p.add_argument('--chunks', default='data/overlap_chunks.json')
    p.add_argument('--window', type=int, default=6)
    p.add_argument('--overlap', type=int, default=2)
    p.add_argument('--index', default='data/faiss_index.idx')
    p.add_argument('--meta', default='data/faiss_meta.json')
    p.add_argument('--model', default='all-MiniLM-L6-v2')
    args = p.parse_args(argv)

    py = sys.executable
    # 1) create overlapping chunks
    run([py, 'scripts/advanced_chunker.py', '--indir', args.indir, '--out', args.chunks, '--window', str(args.window), '--overlap', str(args.overlap)])

    # 2) build faiss index
    run([py, 'scripts/build_faiss_index.py', '--chunks', args.chunks, '--index', args.index, '--meta', args.meta, '--model', args.model])

    print('Update complete: chunks ->', args.chunks, 'index ->', args.index)


if __name__ == '__main__':
    main()
