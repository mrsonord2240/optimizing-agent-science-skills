#!/usr/bin/env python3
"""sha256-manifest-v1: sha256 of LF-joined 'relpath\\tbytes\\tsha256' lines,
files in ordinal UTF-8 path order, no trailing LF. Prints JSON."""
import hashlib, json, os, sys

def manifest(root):
    files = []
    for dp, dns, fns in os.walk(root):
        for fn in fns:
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            data = open(p, "rb").read()
            files.append((rel, len(data), hashlib.sha256(data).hexdigest()))
    files.sort(key=lambda f: f[0].encode("utf-8"))
    body = "\n".join(f"{r}\t{b}\t{h}" for r, b, h in files)
    return {
        "root": root,
        "identity": "sha256-manifest-v1",
        "manifest_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
        "file_count": len(files),
        "total_bytes": sum(f[1] for f in files),
        "files": [{"path": r, "sha256": h, "bytes": b} for r, b, h in files],
    }

if __name__ == "__main__":
    print(json.dumps([manifest(r) for r in sys.argv[1:]], indent=2))
