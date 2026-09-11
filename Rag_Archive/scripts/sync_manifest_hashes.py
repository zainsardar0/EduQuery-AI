import hashlib
import json
import os

root = "data/policy_rag_markdown_r4"
manifest_path = os.path.join(root, "policy_index_manifest.json")
benchmark_path = os.path.join(root, "policy_benchmark_report.json")
source_root = os.path.join(root, "source-md")

with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

for s in manifest.get("sources", []):
    fpath = os.path.join(source_root, s["filename"])
    if os.path.exists(fpath):
        with open(fpath, "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest().upper()
            s["source_sha256"] = h

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2)

with open(manifest_path, "rb") as f:
    manifest_hash = hashlib.sha256(f.read()).hexdigest().upper()

with open(benchmark_path, "r", encoding="utf-8") as f:
    benchmark = json.load(f)

benchmark["manifest_sha256"] = manifest_hash

with open(benchmark_path, "w", encoding="utf-8") as f:
    json.dump(benchmark, f, indent=2)

print("Updated hashes successfully.")
