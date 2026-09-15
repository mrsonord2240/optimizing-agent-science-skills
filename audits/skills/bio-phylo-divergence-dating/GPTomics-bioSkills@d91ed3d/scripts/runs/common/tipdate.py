"""Temporal-signal workflow from the Skill, run on SYNTHETIC heterochronous data.
usage: python tipdate.py TAG OUTDIR NREPS
  1. iqtree2 -s seqs.fa -m GTR+G -T AUTO --prefix rttree       (Skill command; -ntmax 4 added for the shared host)
  2. root-to-tip regression (TempEst is GUI-only): best-fitting root by R^2 over all edges, slope/intercept/R^2/residuals
  3. iqtree2 -s seqs.fa -m GTR+G --date dates.tsv --date-ci 100 --prefix lsd2  (Skill command, as written)
  4. date-randomization test: NREPS shuffled date files, LSD2 on the fixed ML tree, compare rates to real CI
"""
import json
import os
import random
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

import dendropy
import numpy as np

BIN = r"F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\tools\bin"
IQ = os.path.join(BIN, "iqtree2.exe")
tag, out, nreps = sys.argv[1], os.path.abspath(sys.argv[2]), int(sys.argv[3])
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data")
os.makedirs(out, exist_ok=True)
shutil.copy(os.path.join(DATA, f"{tag}_aln.fa"), os.path.join(out, "seqs.fa"))
shutil.copy(os.path.join(DATA, f"{tag}_dates.tsv"), os.path.join(out, "dates.tsv"))
truth = json.load(open(os.path.join(DATA, f"{tag}_truth.json")))


def sh(cmd, log):
    r = subprocess.run(cmd, cwd=out, capture_output=True, text=True)
    with open(os.path.join(out, log), "w", encoding="utf-8") as fh:
        fh.write(" ".join(cmd) + "\n" + r.stdout + r.stderr)
    return r.returncode, r.stdout


rc, _ = sh([IQ, "-s", "seqs.fa", "-m", "GTR+G", "-T", "AUTO", "-ntmax", "4", "--prefix", "rttree", "-redo",
            "--seed", "1"], "step1_iqtree.txt")
print("step1 iqtree2 ML tree exit", rc)

dates = {l.split("\t")[0]: float(l.split("\t")[1]) for l in open(os.path.join(out, "dates.tsv")) if l.strip()}


def rtt(tree):
    xs, ys = [], []
    for leaf in tree.leaf_node_iter():
        ys.append(leaf.distance_from_root())
        xs.append(dates[leaf.taxon.label])
    xs, ys = np.array(xs), np.array(ys)
    slope, icpt = np.polyfit(xs, ys, 1)
    pred = slope * xs + icpt
    r2 = 1 - ((ys - pred) ** 2).sum() / ((ys - ys.mean()) ** 2).sum()
    return slope, icpt, r2, xs, ys - pred


base = dendropy.Tree.get(path=os.path.join(out, "rttree.treefile"), schema="newick", preserve_underscores=True)
best = None
for i, e in enumerate(list(base.postorder_edge_iter())):
    if e.tail_node is None:
        continue
    for frac in (0.1, 0.3, 0.5, 0.7, 0.9):
        t = dendropy.Tree.get(path=os.path.join(out, "rttree.treefile"), schema="newick", preserve_underscores=True)
        ed = list(t.postorder_edge_iter())[i]
        L = ed.length or 0.0
        t.reroot_at_edge(ed, length1=L * frac, length2=L * (1 - frac), update_bipartitions=False,
                         suppress_unifurcations=True)
        s, c, r2, xs, res = rtt(t)
        if best is None or r2 > best[2]:
            best = (s, c, r2, xs, res, t.as_string(schema="newick"))
s, c, r2, xs, res = best[:5]
x_int = -c / s if s != 0 else float("nan")
sd = res.std()
outl = [(n, round(r, 5)) for n, r in zip(sorted(dates, key=lambda k: 0), [])]
print(f"step2 root-to-tip (best-fitting root by R^2): slope={s:.3e} subs/site/yr  x-intercept(TMRCA)={x_int:.2f}  "
      f"R^2={r2:.3f}  |residual|>3sd tips={int((np.abs(res) > 3 * sd).sum())}")

rc, _ = sh([IQ, "-s", "seqs.fa", "-m", "GTR+G", "--date", "dates.tsv", "--date-ci", "100", "--prefix", "lsd2",
            "-redo", "--seed", "1"], "step3_lsd2.txt")
print("step3 LSD2 (Skill command as written) exit", rc)
lsd = open(os.path.join(out, "lsd2.timetree.lsd"), encoding="utf-8", errors="replace").read() \
    if os.path.exists(os.path.join(out, "lsd2.timetree.lsd")) else ""
m = re.search(r"rate\s+([\d.eE+-]+)\s*\[([\d.eE+-]+);\s*([\d.eE+-]+)\],\s*tMRCA\s+([\d.]+)\s*\[([\d.]+);\s*([\d.]+)\]", lsd)
real = tuple(float(x) for x in m.groups()) if m else None
print("step3 LSD2 rate [CI], tMRCA [CI]:", real, "| truth rate", truth["strict_clock_rate"], "tMRCA",
      truth["true_tmrca"])


def rep(k):
    rng = random.Random(1000 + k)
    names = list(dates)
    vals = [dates[n] for n in names]
    rng.shuffle(vals)
    d = os.path.join(out, "dr", f"r{k:02d}")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "dates.tsv"), "w", newline="\n") as fh:
        fh.writelines(f"{n}\t{v}\n" for n, v in zip(names, vals))
    r = subprocess.run([IQ, "-s", os.path.join(out, "seqs.fa"), "-te", os.path.join(out, "rttree.treefile"), "-m",
                        "GTR+G", "--date", "dates.tsv", "--prefix", "r", "-redo", "-T", "1"], cwd=d,
                       capture_output=True, text=True)
    txt = open(os.path.join(d, "r.timetree.lsd"), errors="replace").read() if os.path.exists(
        os.path.join(d, "r.timetree.lsd")) else ""
    mm = re.search(r"rate\s+([\d.eE+-]+)", txt)
    return float(mm.group(1)) if mm else None


with ThreadPoolExecutor(4) as ex:
    reps = [x for x in ex.map(rep, range(nreps)) if x is not None]
reps = np.array(reps)
lo, hi = np.percentile(reps, [2.5, 97.5])
print(f"step4 date-randomization: {len(reps)} reps, randomized rate 95% range [{lo:.3e}, {hi:.3e}] max {reps.max():.3e}")
if real:
    overlap = real[1] <= hi
    print(f"step4 real rate {real[0]:.3e} CI [{real[1]:.3e}, {real[2]:.3e}] -> "
          f"{'OVERLAPS randomized cloud: NO temporal signal, do not date' if overlap else 'outside randomized cloud: temporal signal PASSES'}")
json.dump({"rtt": {"slope": s, "x_intercept": x_int, "r2": r2}, "lsd2": real, "dr_reps": reps.tolist(),
           "truth": truth}, open(os.path.join(out, "tipdate_results.json"), "w"), indent=1)
