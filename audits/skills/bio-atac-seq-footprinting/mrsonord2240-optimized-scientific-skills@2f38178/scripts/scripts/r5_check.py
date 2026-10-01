"""Independent assertions on r5 scPrinter outputs. Labels: this re-audit's TOBIAS run A cond1 CTCF bound/unbound (labels.tsv)."""
import numpy as np, pandas as pd
from scipy.stats import mannwhitneyu
W = "/mnt/openscience/audit-envs/bio-atac-seq-footprinting/reaudit-final/scp"
lab = pd.read_csv(f"{W}/labels.tsv", sep="\t"); ok = True
def check(name, cond, detail=""):
    global ok; ok &= bool(cond); print(("PASS " if cond else "FAIL ") + name, detail)
def labels(keys):
    mids = np.array([(int(k.split(":")[1].split("-")[0]) + int(k.split("-")[-1])) // 2 for k in keys]); out = []
    for m in mids:
        hit = lab[(lab.s - m).abs() <= 1]; out.append(hit.cls.iloc[0] if len(hit) else "?")
    return np.array(out)
def contrast(S, modes, mode, b, u):
    i = int(np.where(modes == mode)[0][0]); cb, cu = S[b][:, i, 90:110].mean(1), S[u][:, i, 90:110].mean(1)
    return cb.mean(), cu.mean(), mannwhitneyu(cb, cu, alternative="greater").pvalue
res = {}
for run in ("B0", "B45"):
    z = np.load(f"{W}/{run}/footprints.npz"); S, modes = z["scores"], z["modes"]; cls = labels(z["keys"]); b, u = cls == "bound", cls == "unbound"
    check(f"{run} shape regions x modes x width", S.shape == (400, 99, 200), str(S.shape))
    check(f"{run} finite, all regions labelled", np.isfinite(S).all() and (cls != "?").all(), {c: int((cls == c).sum()) for c in set(cls)})
    for mode in (10, 20, 30, 50):
        cb, cu, p = contrast(S, modes, mode, b, u); res[(run, mode)] = (cb, cu, p); print(f"  {run} mode {mode}: bound {cb:.3f} unbound {cu:.3f} p {p:.1e}")
    i10 = int(np.where(modes == 10)[0][0]); prof = S[b][:, i10].mean(0); pk = int(np.argmax(prof)) - 100
    print(f"  {run} mode-10 bound profile argmax offset from centre: {pk} bp; centre/flank ratio {prof[90:110].mean() / np.r_[prof[:60], prof[140:]].mean():.2f}")
    res[(run, "pk")] = pk
    t = pd.read_csv(f"{W}/{run}/center_by_mode.tsv", sep="\t")
    check(f"{run} center_by_mode.tsv 99 rows; centre column equals npz recomputation", len(t) == 99 and np.allclose(t.center_pm10bp_mean.values, S[:, :, 90:110].mean(2).mean(0), atol=1e-5))
check("B0 (raw fragments, --shift 0,0): bound > unbound at modes 10-30, p < 1e-5", all(res[("B0", m)][2] < 1e-5 for m in (10, 20, 30)))
check("B0 mode 50 does not separate (SKILL.md claim)", res[("B0", 50)][0] <= res[("B0", 50)][1] or res[("B0", 50)][2] > 0.05, str(res[("B0", 50)]))
print("  wrong-shift comparison (B45 = Cell Ranger setting on raw fragments):",
      {m: f"B0 diff {res[('B0', m)][0]-res[('B0', m)][1]:.3f} vs B45 diff {res[('B45', m)][0]-res[('B45', m)][1]:.3f}" for m in (10, 20, 30)})
for run in ("C", "CA"):
    z = np.load(f"{W}/{run}/footprints.npz"); S4, modes, groups = z["scores"], z["modes"], z["groups"]; cls = labels(z["keys"]); b, u = cls == "bound", cls == "unbound"
    check(f"{run} shape regions x groups x modes x width", S4.shape == (400, 5, 4, 200), str(S4.shape))
    check(f"{run} finite, all labelled", np.isfinite(S4).all() and (cls != "?").all())
    rows = []
    for gi, g in enumerate(groups):
        for mode in modes:
            cb, cu, p = contrast(S4[:, gi], modes, mode, b, u); rows.append((g, int(mode), cb, cu, p))
    T = pd.DataFrame(rows, columns=["group", "mode", "bound", "unbound", "p_greater"])
    if run == "C": print(T.round(4).to_string(index=False)); T.to_csv("/mnt/openscience/audits/bio-atac-seq-footprinting/reaudit-final-20260930/out/r5_C_cluster_contrast.tsv", sep="\t", index=False)
    print(f"  {run}: bound > unbound in {int((T.bound > T.unbound).sum())}/{len(T)} group x mode cells; p < 0.05 in {int((T.p_greater < 0.05).sum())}")
    prof = S4[b][:, :, list(modes).index(10)].mean(0); rr = np.corrcoef(prof); off = rr[~np.eye(len(rr), dtype=bool)]
    print(f"  {run}: cross-group r of mode-10 bound profiles {off.min():.2f}..{off.max():.2f}")
    t = pd.read_csv(f"{W}/{run}/center_by_mode.tsv", sep="\t"); check(f"{run} center_by_mode rows = groups x modes", len(t) == 20, str(len(t)))
    sub = t[(t.group == groups[0])].center_pm10bp_mean.values
    check(f"{run} center_by_mode matches npz for first group", np.allclose(sub, S4[:, 0, :, 90:110].mean(2).mean(0), atol=1e-5))
print("ALL PASS" if ok else "SOME FAILED")
