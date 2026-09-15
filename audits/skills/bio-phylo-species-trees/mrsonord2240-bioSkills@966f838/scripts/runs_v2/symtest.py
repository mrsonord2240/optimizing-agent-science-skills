"""The fixed Skill's asymmetry test: binomial test of f2 against f2+f3 with p = 0.5, applied to the gene-tree-count
analogue it names (gDF1_N vs gDF2_N in cf_g.cf.stat). Auditor implementation of that sentence."""
import sys
from scipy.stats import binomtest
rows, hdr = [], None
for line in open(sys.argv[1], encoding="utf-8"):
    if line.startswith("#") or not line.strip():
        continue
    parts = line.rstrip("\n").split("\t")
    if hdr is None:
        hdr = parts; continue
    rows.append(dict(zip(hdr, parts)))
print("ID  gCF   gDF1_N gDF2_N  p(binomial f2 vs f2+f3)  verdict")
for r in rows:
    if r["gDF1_N"] in ("NA", "") or r["gDF2_N"] in ("NA", ""):
        continue                       # root/trivial branches carry NA in IQ-TREE's cf.stat
    a, b = round(float(r["gDF1_N"])), round(float(r["gDF2_N"]))
    p = binomtest(a, a + b, 0.5).pvalue if a + b else float("nan")
    print(f"{r['ID']:<3} {float(r['gCF']):5.1f} {a:6d} {b:6d}  {p:.2e}  {'ASYMMETRIC' if p < 0.05 else 'symmetric'}")
