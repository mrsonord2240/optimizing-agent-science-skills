"""Independent checks on r3 TOBIAS runs: differential summary vs pandas ranking, biology direction, CTCF dip depth A vs N,
outputs present, and that rc-4 runs still print the differential table before failing."""
import os, re, numpy as np, pandas as pd
W = "/mnt/openscience/audit-envs/bio-atac-seq-footprinting/reaudit-final/rt"; L = "/mnt/openscience/audits/bio-atac-seq-footprinting/reaudit-final-20260930/logs"
ok = True
def check(name, cond, detail=""):
    global ok; ok &= bool(cond); print(("PASS " if cond else "FAIL ") + name, detail)
def table_from_log(run):
    t = open(f"{L}/r3_{run}.log").read().split("=== Top differential motifs")[1].split("\n")[1:]
    return [l.split("\t")[0] for l in t if l.count("\t") == 2]
def agg(run, cond):
    d = {}
    for line in open(f"{W}/{run}/validation/ctcf_{cond}_aggregate.txt"):
        f = line.rstrip("\n").split("\t")
        if len(f) == 3 and not line.startswith("#"): d[(f[0], f[1])] = np.array([float(x) for x in f[2].split(",")])
    return d
for run in ("A", "N", "S", "F"):
    r = pd.read_csv(f"{W}/{run}/bindetect/bindetect_results.txt", sep="\t")
    exp = r[r.cond1_cond2_pvalue <= 0.05].assign(a=lambda x: x.cond1_cond2_change.abs()).sort_values("a", ascending=False).output_prefix.head(20).tolist()
    got = table_from_log(run)
    check(f"{run} printed top table equals pandas |change| ranking (p<=0.05)", got == exp, f"{len(got)} rows, first {got[:2]}")
    g = dict(zip(r.output_prefix, r.cond1_cond2_change))
    check(f"{run} GATA1 < 0 (K562) and IRF4 > 0 (GM12878)", g["GATA1_MA0035.5"] < 0 and g["IRF4_MA1419.2"] > 0, f"GATA1 {g['GATA1_MA0035.5']:.3f} IRF4 {g['IRF4_MA1419.2']:.3f}")
    check(f"{run} validation PDFs and txts for both conditions", all(os.path.getsize(f"{W}/{run}/validation/ctcf_{c}_aggregate.{e}") > 0 for c in ("cond1", "cond2") for e in ("pdf", "txt")))
x = np.arange(-60, 60)
core, flank = np.abs(x) <= 10, np.abs(x) >= 30
for run in ("A", "N"):
    for c in ("cond1", "cond2"):
        d = agg(run, c); fm = {k: d[(k[0], k[1])][flank].mean() - d[(k[0], k[1])][core].mean() for k in [("corrected", "bound"), ("corrected", "unbound"), ("uncorrected", "bound")]}
        print(f"  {run} {c} flank-minus-core: corrected bound {fm[('corrected','bound')]:.2f}, corrected unbound {fm[('corrected','unbound')]:.2f}, uncorrected bound {fm[('uncorrected','bound')]:.2f}")
for run in ("N", "SN", "FN"):
    check(f"{run} (rc 4) still printed the differential table before failing", len(table_from_log(run)) > 0)
print("ALL PASS" if ok else "SOME FAILED")
