"""Aggregate CTCF profiles: bound / unbound / all sites, corrected vs uncorrected signal, and bound sites derived from UNCORRECTED footprints.
Usage: a7b_qc_profiles.py <a1 dir> <a7 dir> <png>"""
import sys, numpy as np, pyBigWig
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
a1, a7, png = sys.argv[1:4]
B = f"{a1}/out/bindetect/CTCF_MA0139.2/beds/CTCF_MA0139.2_"
U = f"{a7}/bd_unc/CTCF_MA0139.2/beds/CTCF_MA0139.2_"
def sites(p): return [l.split("\t")[:3] for l in open(p) if l.strip()]
def prof(bwp, S, maxn=5000):
    bw = pyBigWig.open(bwp); acc = []
    for c, s, e in S[:maxn]:
        m = (int(s)+int(e))//2
        if m-100 < 0: continue
        acc.append(np.nan_to_num(np.array(bw.values(c, m-100, m+100))))
    return np.mean(acc, 0), len(acc)
def depth(p): return float(np.r_[p[:40], p[-40:]].mean() - p[90:110].mean())   # flank - core
sets = {"corrected-pipeline bound (cond1)": sites(B+"cond1_bound.bed"),
        "corrected-pipeline unbound (cond1)": sites(B+"cond1_unbound.bed"),
        "all CTCF motif sites in peaks": sites(B+"all.bed"),
        "uncorrected-pipeline bound (cond1)": sites(U+"cond1_bound.bed"),
        "uncorrected-pipeline unbound (cond1)": sites(U+"cond1_unbound.bed")}
sigs = {"corrected": f"{a1}/out/cond1/cond1_corrected.bw", "uncorrected": f"{a1}/out/cond1/cond1_uncorrected.bw", "expected(bias)": f"{a1}/out/cond1/cond1_expected.bw"}
fig, axes = plt.subplots(1, 3, figsize=(13, 3.6), sharex=True)
print(f"{'site set':42s} {'signal':15s} n     flank-core   core/flank")
for ax, (sn, sp) in zip(axes, sigs.items()):
    for name, S in sets.items():
        p, n = prof(sp, S); ax.plot(np.arange(-100, 100), p, label=f"{name} (n={n})", lw=1)
        fl = np.r_[p[:40], p[-40:]].mean(); co = p[90:110].mean()
        print(f"{name:42s} {sn:15s} {n:5d} {depth(p):10.3f} {co/fl if fl else float('nan'):10.3f}")
    ax.set_title(f"cond1 {sn} signal at CTCF MA0139.2"); ax.set_xlabel("bp from motif centre")
axes[0].legend(fontsize=6); fig.tight_layout(); fig.savefig(png, dpi=110)
