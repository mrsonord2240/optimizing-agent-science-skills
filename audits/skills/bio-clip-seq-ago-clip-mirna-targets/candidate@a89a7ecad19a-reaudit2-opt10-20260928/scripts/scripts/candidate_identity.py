#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path("/mnt/openscience/audits/bio-clip-seq-ago-clip-mirna-targets/reaudit2-opt10-20260928")
CANDIDATE = Path("/mnt/openscience/wt/opt10-ago-clip/skills/bio-clip-seq-ago-clip-mirna-targets")
rows, files = [], []
for path in sorted((p for p in CANDIDATE.rglob("*") if p.is_file()), key=lambda p: p.relative_to(CANDIDATE).as_posix()):
    raw = path.read_bytes()
    rel = path.relative_to(CANDIDATE).as_posix()
    digest = hashlib.sha256(raw).hexdigest()
    files.append({"path": rel, "bytes": len(raw), "sha256": digest})
    rows.append(f"{rel}\t{len(raw)}\t{digest}")
manifest = "\n".join(rows).encode("utf-8")
(ROOT / "candidate-manifest.tsv").write_bytes(manifest)
identity = hashlib.sha256(manifest).hexdigest()
assert identity == "a89a7ecad19a3cc207ab6b82bc0910b126b663e32e7c74c3c2b74dc105d780fa", identity
print(json.dumps({"identity": identity, "file_count": len(files), "manifest_bytes": len(manifest), "files": files}, indent=2, sort_keys=True))
