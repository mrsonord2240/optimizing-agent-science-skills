"""delta-cat2: verify identity, compare per-file manifest with the delta-cat-20260930 candidate manifest,
and show the content diff of changed files against the shelf (ea3b976) copy.
Usage: python delta2_diff.py <skill_id> <candidate_dir> <expected_identity>"""
import difflib, json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
sid, cand, exp = sys.argv[1:4]
from identity_diff import manifest
cid, files = manifest(cand)
prev = json.load(open(f"F:/OpenScience/audits/{sid}/delta-cat-20260930/logs/identity.json", encoding="utf-8"))
print(f"candidate identity {cid} expected {exp} match={cid == exp} files={len(files)} bytes={sum(f['bytes'] for f in files)}")
print(f"previous delta-cat identity {prev['candidate_identity']}")
pm = {f['path']: f for f in prev['candidate_files']}; cm = {f['path']: f for f in files}
changed = sorted(p for p in cm if p in pm and cm[p]['sha256'] != pm[p]['sha256'])
print(f"vs delta-cat: changed={changed} added={sorted(set(cm)-set(pm))} removed={sorted(set(pm)-set(cm))}")
shelf = f"F:/optimized-scientific-skills/skills/{sid}"
for p in changed:
    a = open(os.path.join(shelf, p), encoding='utf-8').read().splitlines(True)
    b = open(os.path.join(cand, p), encoding='utf-8').read().splitlines(True)
    sys.stdout.writelines(difflib.unified_diff(a, b, 'shelf/' + p, 'candidate/' + p))
json.dump({"candidate_identity": cid, "candidate_files": files, "previous_identity": prev['candidate_identity'],
           "shelf_identity": prev['shelf_identity'], "changed_vs_previous": changed},
          open(f"F:/OpenScience/audits/{sid}/delta-cat2-20260930/logs/identity.json", "w", encoding="utf-8"), indent=2)
