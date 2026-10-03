"""SA-003: extract every ```python block from SKILL.md, run the blocks as separate-but-chained cells in one namespace, verbatim."""
import re, sys, time
sys.dont_write_bytecode = True
s = open(r"F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-survival-analysis\SKILL.md", encoding="utf-8").read()
blocks = re.findall(r"```python\n(.*?)```", s, re.S)
print("python blocks:", len(blocks)); g = {}; t0 = time.time()
for i, b in enumerate(blocks, 1):
    print(f"--- block {i} ({len(b.splitlines())} lines)"); exec(compile(b, f"SKILL.md-block-{i}", "exec"), g)
print(f"OK in {time.time()-t0:.1f}s")
for k in ("c_uno", "mean_auc", "ibs", "ibs_km"): print(k, round(float(g[k]), 4))
assert 0.6 < g["c_uno"] < 0.75 and g["ibs"] < g["ibs_km"]
