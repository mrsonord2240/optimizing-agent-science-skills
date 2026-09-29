#!/usr/bin/env python3
import hashlib
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
out = pathlib.Path(sys.argv[2])
rows = []
paths = [p for p in root.rglob("*") if p.is_file()]
paths.sort(key=lambda p: p.relative_to(root).as_posix().encode("utf-8"))
for path in paths:
    data = path.read_bytes()
    rel = path.relative_to(root).as_posix()
    rows.append(f"{rel}\t{len(data)}\t{hashlib.sha256(data).hexdigest()}")
manifest = "\n".join(rows).encode()
out.write_bytes(manifest)
print(hashlib.sha256(manifest).hexdigest())

