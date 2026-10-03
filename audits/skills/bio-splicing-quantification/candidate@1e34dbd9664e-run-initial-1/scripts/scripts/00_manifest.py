"""Compute the per-file manifest of the audited candidate (identity itself comes from tools/skill_preflight.py)."""
import hashlib, os, json, sys
root = sys.argv[1]
out = []
for r, _, fs in os.walk(root):
    for f in fs:
        p = os.path.join(r, f)
        rel = os.path.relpath(p, root).replace(os.sep, '/')
        b = open(p, 'rb').read()
        out.append({'path': rel, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()})
out.sort(key=lambda x: x['path'])
rec = '\n'.join(f"{o['path']}\t{o['bytes']}\t{o['sha256']}" for o in out)
print(json.dumps(out))
print(hashlib.sha256(rec.encode()).hexdigest(), len(out), sum(o['bytes'] for o in out))
