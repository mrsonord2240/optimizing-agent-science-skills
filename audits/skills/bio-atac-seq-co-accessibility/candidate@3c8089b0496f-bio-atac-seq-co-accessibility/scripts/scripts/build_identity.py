import hashlib, os, json
root = r'F:\OpenScience\wt\atac-co-accessibility\skills\bio-atac-seq-co-accessibility'
R = r'F:\OpenScience\audits\bio-atac-seq-co-accessibility'
rows = []
for d, _, fs in os.walk(root):
    for f in fs:
        p = os.path.join(d, f); b = open(p, 'rb').read().replace(b'\r\n', b'\n')
        rows.append((os.path.relpath(p, root).replace(chr(92), '/'), len(b), hashlib.sha256(b).hexdigest()))
rows.sort(key=lambda x: x[0].encode())
man = "\n".join(f"{a}\t{b}\t{c}" for a, b, c in rows).encode()
ident = hashlib.sha256(man).hexdigest()
print(ident, len(rows), len(man))
raw = []
for d, _, fs in os.walk(root):
    for f in fs:
        raw.append((os.path.relpath(os.path.join(d,f), root), hashlib.sha256(open(os.path.join(d,f),'rb').read()).hexdigest()))
print(sorted(raw))
