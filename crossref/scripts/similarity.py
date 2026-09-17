"""Measure true content similarity for every colliding / near-duplicate pair in the catalog.

difflib.quick_ratio() is a bag-of-characters UPPER BOUND and reported 0.87 for pairs whose real
similarity is 0.03. Everything here uses SequenceMatcher.ratio() on the body text (frontmatter
stripped), plus a word-level Jaccard as a second, independent measure so no conclusion rests on one
metric.
"""
import json
import os
import re
from difflib import SequenceMatcher

ROOT = "F:/OpenScience/external"
CAT = "F:/OpenScience/catalog"

d = json.load(open(os.path.join(CAT, "catalog.json"), encoding="utf-8"))
skills = d["skills"]
cache = {}


def body(m):
    key = (m["repo"], m["path"])
    if key not in cache:
        p = os.path.join(ROOT, m["repo"], m["path"], "SKILL.md")
        t = open(p, encoding="utf-8", errors="replace").read()
        cache[key] = re.sub(r"^---.*?---", "", t, count=1, flags=re.S).strip()
    return cache[key]


def words(t):
    return set(re.findall(r"[a-z0-9]{3,}", t.lower()))


def measure(a, b):
    ta, tb = body(a), body(b)
    if not ta or not tb:
        return None
    ratio = SequenceMatcher(None, ta, tb).ratio()
    wa, wb = words(ta), words(tb)
    jac = len(wa & wb) / len(wa | wb) if (wa or wb) else 0.0
    return {"ratio": round(ratio, 3), "word_jaccard": round(jac, 3),
            "bytes_a": len(ta), "bytes_b": len(tb)}


rows = []
for c in d["collisions"]:
    ms = c["members"]
    for i in range(len(ms)):
        for j in range(i + 1, len(ms)):
            a, b = ms[i], ms[j]
            if a["repo"] == b["repo"]:
                continue
            m = measure(a, b)
            if m:
                rows.append({"kind": "name-collision", "name": c["name"],
                             "a": f'{a["repo"]}:{a["path"]}', "b": f'{b["repo"]}:{b["path"]}',
                             "repo_a": a["repo"], "repo_b": b["repo"], **m})

for n in d["near"]:
    a, b = skills[n["a"]], skills[n["b"]]
    if a["repo"] == b["repo"] or a["name"].lower() == b["name"].lower():
        continue
    m = measure(a, b)
    if m:
        rows.append({"kind": "near-desc", "name": f'{a["name"]} ~ {b["name"]}',
                     "a": f'{a["repo"]}:{a["path"]}', "b": f'{b["repo"]}:{b["path"]}',
                     "repo_a": a["repo"], "repo_b": b["repo"], "desc_jaccard": n["jaccard"], **m})

json.dump(rows, open(os.path.join(CAT, "similarity.json"), "w", encoding="utf-8"), indent=1)

# Buckets chosen so each maps to a different action, not to a pretty distribution.
NEAR = [r for r in rows if r["ratio"] >= 0.80]
SUBST = [r for r in rows if 0.45 <= r["ratio"] < 0.80]
NAME_ONLY = [r for r in rows if r["ratio"] < 0.45 and r["kind"] == "name-collision"]

print(f"pairs measured            : {len(rows)}")
print(f"  near-identical (>=0.80) : {len(NEAR)}   -> pick one, they are the same text")
print(f"  substantial (0.45-0.80) : {len(SUBST)}  -> real overlap, needs a judgement call")
print(f"  name-only (<0.45)       : {len(NAME_ONLY)}  -> same name, different skill entirely")
print()
import collections
print("=== near-identical pairs by repo pair ===")
c = collections.Counter((min(r["repo_a"], r["repo_b"]), max(r["repo_a"], r["repo_b"])) for r in NEAR)
for (a, b), n in c.most_common(10):
    print(f'  {n:3d}  {a.split("__")[1]}  <->  {b.split("__")[1]}')
print()
print("=== substantial-overlap pairs by repo pair ===")
c = collections.Counter((min(r["repo_a"], r["repo_b"]), max(r["repo_a"], r["repo_b"])) for r in SUBST)
for (a, b), n in c.most_common(10):
    print(f'  {n:3d}  {a.split("__")[1]}  <->  {b.split("__")[1]}')
