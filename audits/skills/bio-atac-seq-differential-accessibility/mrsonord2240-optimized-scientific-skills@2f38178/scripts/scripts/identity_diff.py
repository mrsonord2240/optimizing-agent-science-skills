"""Delta re-audit helper: sha256-manifest-v1 identity of candidate and shelf, plus unified diff.

Usage: python identity_diff.py <skill_id> <candidate_dir> <shelf_dir> <out_json>
Identity = sha256 of LF-joined "relpath\tbytes\tsha256" lines, ordinal UTF-8 path order, no trailing LF.
"""
import difflib
import hashlib
import json
import os
import sys


def manifest(root):
    files = []
    for dp, dn, fn in os.walk(root):
        for f in fn:
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, root).replace(os.sep, "/")
            b = open(p, "rb").read()
            files.append({"path": rel, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()})
    files.sort(key=lambda x: x["path"].encode("utf-8"))
    text = "\n".join(f"{x['path']}\t{x['bytes']}\t{x['sha256']}" for x in files)
    return hashlib.sha256(text.encode("utf-8")).hexdigest(), files


def main():
    sid, cand, shelf, out = sys.argv[1:5]
    cid, cfiles = manifest(cand)
    sid_, sfiles = manifest(shelf)
    cmap = {f["path"]: f for f in cfiles}
    smap = {f["path"]: f for f in sfiles}
    changed = sorted(p for p in cmap if p in smap and cmap[p]["sha256"] != smap[p]["sha256"])
    added = sorted(set(cmap) - set(smap))
    removed = sorted(set(smap) - set(cmap))
    print(f"skill {sid}")
    print(f"candidate identity {cid} files={len(cfiles)} bytes={sum(f['bytes'] for f in cfiles)}")
    print(f"shelf identity     {sid_} files={len(sfiles)} bytes={sum(f['bytes'] for f in sfiles)}")
    print(f"changed={changed} added={added} removed={removed}")
    for p in changed + added + removed:
        a = open(os.path.join(shelf, p), encoding="utf-8").read().splitlines(True) if p in smap else []
        b = open(os.path.join(cand, p), encoding="utf-8").read().splitlines(True) if p in cmap else []
        sys.stdout.writelines(difflib.unified_diff(a, b, "shelf/" + p, "candidate/" + p))
    json.dump({"candidate_identity": cid, "candidate_files": cfiles, "shelf_identity": sid_,
               "shelf_files": sfiles, "changed": changed, "added": added, "removed": removed},
              open(out, "w", encoding="utf-8"), indent=2)


if __name__ == "__main__":
    main()
