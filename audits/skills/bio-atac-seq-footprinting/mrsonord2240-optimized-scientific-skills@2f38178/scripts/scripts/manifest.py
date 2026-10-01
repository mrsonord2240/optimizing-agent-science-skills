"""sha256-manifest-v1: sha256 of LF-joined 'relpath<TAB>bytes<TAB>sha256' lines, ordinal UTF-8 path order, no trailing LF."""
import hashlib, os, sys
root = sys.argv[1]; rows = []
for dp, dn, fn in os.walk(root):
    for f in fn:
        p = os.path.join(dp, f); b = open(p, "rb").read()
        rows.append((os.path.relpath(p, root).replace(os.sep, "/"), len(b), hashlib.sha256(b).hexdigest()))
rows.sort(key=lambda r: r[0].encode("utf-8"))
print(hashlib.sha256("\n".join(f"{r}\t{b}\t{h}" for r, b, h in rows).encode()).hexdigest(), len(rows), sum(r[1] for r in rows))
for r in rows: print(*r, sep="\t")
