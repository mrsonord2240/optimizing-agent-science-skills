import hashlib, os, sys
root = sys.argv[1]; L = []
for r, d, f in os.walk(root):
    for n in f:
        p = os.path.join(r, n); rel = os.path.relpath(p, root).replace(chr(92), "/")
        b = open(p, "rb").read().replace(b"\r\n", b"\n"); L.append((rel, len(b), hashlib.sha256(b).hexdigest()))
L.sort(key=lambda x: x[0].encode())
m = "\n".join("%s\t%d\t%s" % t for t in L).encode()
print(hashlib.sha256(m).hexdigest(), len(L), "files", sum(t[1] for t in L), "bytes")
