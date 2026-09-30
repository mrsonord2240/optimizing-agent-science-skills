"""Assertions on scripts/scprinter_footprint.py output: CTCF TOBIAS-bound vs unbound sites (labels from TOBIAS beds, sampled independently of scPrinter)."""
import sys
import numpy as np, pandas as pd
from scipy.stats import mannwhitneyu
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt

W = "/mnt/openscience/audit-envs/bio-atac-seq-footprinting/reaudit-run/scp"
L = "/mnt/openscience/audits/bio-atac-seq-footprinting/reaudit-run"
z = np.load(f"{W}/out/footprints.npz"); S, keys, modes = z["scores"], z["keys"], z["modes"]
lab = pd.read_csv(f"{W}/regions_labels.tsv", sep="\t")
ok = True
def check(name, cond, detail=""):
    global ok; ok &= bool(cond); print(("PASS " if cond else "FAIL ") + name, detail)

check("shape regions x modes x width", S.shape == (400, 99, 200), str(S.shape))
check("all finite", np.isfinite(S).all())
mids = np.array([(int(k.split(":")[1].split("-")[0]) + int(k.split("-")[-1])) // 2 for k in keys])
cls = []
for m in mids:
    hit = lab[(lab.s - m).abs() <= 1]
    cls.append(hit.cls.iloc[0] if len(hit) else "?")
cls = np.array(cls)
check("every region matched to a TOBIAS label", (cls != "?").all(), {c: int((cls == c).sum()) for c in set(cls)})
b, u = cls == "bound", cls == "unbound"
res = {}
for mode in (10, 20, 30, 50):
    i = int(np.where(modes == mode)[0][0])
    cb, cu = S[b][:, i, 90:110].mean(1), S[u][:, i, 90:110].mean(1)
    p = mannwhitneyu(cb, cu, alternative="greater").pvalue
    res[mode] = (cb.mean(), cu.mean(), p)
    print(f"  mode {mode}: centre +/-10bp mean bound={cb.mean():.3f} unbound={cu.mean():.3f} p(bound>unbound)={p:.1e}")
for mode in (10, 20, 30):
    check(f"mode {mode}: bound > unbound (p<1e-5)", res[mode][2] < 1e-5)
i = int(np.where(modes == 10)[0][0]); prof = S[b][:, i].mean(0)
pk = int(np.argmax(prof[80:120])) + 80 - 100
check("mode 10 bound profile peaks within +/-10 bp of motif centre", abs(pk) <= 10, f"peak offset {pk} bp")
fig, ax = plt.subplots(1, 2, figsize=(9, 3.6), dpi=130)
x = np.arange(-100, 100)
for m, a in zip((10, 30), ax):
    i = int(np.where(modes == m)[0][0])
    a.plot(x, S[b][:, i].mean(0), color="#c0392b", label=f"CTCF bound (n={b.sum()})")
    a.plot(x, S[u][:, i].mean(0), color="#2c3e50", label=f"unbound (n={u.sum()})")
    a.set_title(f"scPrinter footprint score, mode {m}"); a.set_xlabel("bp from motif centre"); a.set_ylabel("mean score")
ax[0].legend(fontsize=8); plt.tight_layout(); plt.savefig(f"{L}/out/r3_scprinter_bound_vs_unbound.png")
tsv = pd.read_csv(f"{W}/out/center_by_mode.tsv", sep="\t")
check("center_by_mode.tsv has 99 modes", len(tsv) == 99)
print("ALL PASS" if ok else "SOME FAILED"); sys.exit(0 if ok else 1)
