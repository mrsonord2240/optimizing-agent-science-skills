"""Classify how each corpus packages its Skills.

Sam's rule: a Skill that is nothing but a SKILL.md is not a bundle candidate — it is at most a source
of inspiration or content to strengthen our own version. A Skill that ships runnable code and
supporting material is a real package, which is the bioSkills shape.

Tiers, by what sits beside SKILL.md:
  packaged   - ships code (.py/.R/.sh/.js/.ipynb) in examples/, scripts/ or anywhere
  resourced  - ships non-code support (references/, assets/, data, templates) but no code
  prose+     - ships only further markdown (usage-guide.md and friends)
  bare       - SKILL.md alone
"""
import json
import os
from collections import Counter, defaultdict

ROOT = "F:/OpenScience/external"
CAT = "F:/OpenScience/catalog"
CODE = {".py", ".r", ".sh", ".js", ".mjs", ".ts", ".ipynb", ".pl", ".rb", ".jl", ".sql", ".nf", ".smk"}
DATA = {".csv", ".tsv", ".json", ".yaml", ".yml", ".txt", ".fasta", ".xlsx", ".rds", ".parquet", ".png", ".jpg", ".pdf"}

DROP = {"K-Dense-AI__claude-scientific-writer"}  # Sam, 2026-09-17: dropped completely

cat = json.load(open(os.path.join(CAT, "catalog.json"), encoding="utf-8"))
skills = [s for s in cat["skills"] if s["repo"] not in DROP]

per_repo = defaultdict(Counter)
per_repo_files = defaultdict(list)
tiers = {}

for s in skills:
    d = os.path.join(ROOT, s["repo"], s["path"])
    code = other = md = 0
    subdirs = set()
    for base, dirs, fns in os.walk(d):
        dirs[:] = [x for x in dirs if x not in (".git", "__pycache__", "node_modules")]
        rel = os.path.relpath(base, d).replace("\\", "/")
        if rel != ".":
            subdirs.add(rel.split("/")[0])
        for f in fns:
            if base == d and f == "SKILL.md":
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext in CODE:
                code += 1
            elif ext == ".md":
                md += 1
            else:
                other += 1
    if code:
        tier = "packaged"
    elif other:
        tier = "resourced"
    elif md:
        tier = "prose+"
    else:
        tier = "bare"
    tiers[(s["repo"], s["path"])] = {"tier": tier, "code": code, "md": md, "other": other,
                                     "subdirs": sorted(subdirs)}
    per_repo[s["repo"]][tier] += 1
    per_repo_files[s["repo"]].append(code + md + other)

json.dump({f"{k[0]}:{k[1]}": v for k, v in tiers.items()},
          open(os.path.join(CAT, "construction.json"), "w", encoding="utf-8"), indent=1)

order = ["packaged", "resourced", "prose+", "bare"]
print(f"{'repo':44s} {'n':>5} {'packaged':>9} {'resourced':>10} {'prose+':>7} {'bare':>5}  {'median files':>12}")
print("-" * 100)
rows = []
for repo, c in per_repo.items():
    n = sum(c.values())
    fl = sorted(per_repo_files[repo])
    med = fl[len(fl) // 2] if fl else 0
    rows.append((c["packaged"] / n, repo, n, c, med))
for frac, repo, n, c, med in sorted(rows, key=lambda r: -r[0]):
    name = repo.split("__")[1][:42]
    print(f"{name:44s} {n:>5} {c['packaged']:>9} {c['resourced']:>10} {c['prose+']:>7} {c['bare']:>5}  {med:>12}")
print("-" * 100)
tot = Counter()
for c in per_repo.values():
    tot.update(c)
n = sum(tot.values())
print(f"{'TOTAL':44s} {n:>5} {tot['packaged']:>9} {tot['resourced']:>10} {tot['prose+']:>7} {tot['bare']:>5}")
print()
print("bundle candidates (packaged):", tot["packaged"])
print("inspiration only (prose+/bare):", tot["prose+"] + tot["bare"])
print()
print("=== most common subdirectory names, by repo ===")
for repo in sorted(per_repo, key=lambda r: -sum(per_repo[r].values()))[:8]:
    sub = Counter()
    for (r, p), v in tiers.items():
        if r == repo:
            sub.update(v["subdirs"])
    top = ", ".join(f"{k}({v})" for k, v in sub.most_common(5)) or "(none)"
    print(f"  {repo.split('__')[1][:40]:42s} {top}")
