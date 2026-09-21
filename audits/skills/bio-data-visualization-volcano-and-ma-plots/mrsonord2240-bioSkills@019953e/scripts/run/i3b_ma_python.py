# Input 3b: SKILL.md block 05 (Python ma_plot) run VERBATIM (exec of the extracted block) on real airway apeglm + raw-MLE tables.
import os, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
D = r"F:\OpenScience\audits\bio-data-visualization-volcano-and-ma-plots"
print("pandas", pd.__version__, "numpy", np.__version__, "matplotlib", matplotlib.__version__)
ns = {}
exec(compile(open(os.path.join(D, "run", "blocks", "skill_block05.py"), encoding="utf-8").read(), "skill_block05.py", "exec"), ns)
ma_plot = ns["ma_plot"]
res = pd.read_csv(os.path.join(D, "data", "airway_apeglm.csv"), index_col=0)
raw = pd.read_csv(os.path.join(D, "data", "airway_raw_mle.csv"), index_col=0)
fails = 0
def chk(name, ok, note=""):
    global fails
    print(f"[{'PASS' if ok else 'FAIL'}] {name} {note}")
    fails += (not ok)
print("rows", len(res), "padj NA", res.padj.isna().sum(), "baseMean min", res.baseMean.min())
fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), sharey=True)
ma_plot(raw, ax=axes[0]); axes[0].set_title("raw MLE (unshrunken)"); axes[0].set_ylabel(r"$\log_2$ fold change (raw MLE)")
ax = ma_plot(res, ax=axes[1]); axes[1].set_title("apeglm shrunken")
fig.tight_layout(); fig.savefig(os.path.join(D, "figs", "i3b_ma_python_raw_vs_apeglm.png"), dpi=150)
# single default call (no ax) as in the Skill
ax2 = ma_plot(res); ax2.figure.savefig(os.path.join(D, "figs", "i3b_ma_python_default.png"), dpi=150)
# assertions on the drawn collections
colls = ax.collections
n_ns, n_sig = len(colls[0].get_offsets()), len(colls[1].get_offsets())
print("drawn: ns", n_ns, "sig", n_sig, "; total", n_ns + n_sig)
chk("sig point count == padj<0.05 count in the table", n_sig == int((res.padj < 0.05).sum()), f"({n_sig} vs {(res.padj<0.05).sum()})")
chk("all rows drawn (NA-padj rows fall in the grey layer)", n_ns + n_sig == len(res))
xs = np.concatenate([c.get_offsets()[:, 0] for c in colls]); ys = np.concatenate([c.get_offsets()[:, 1] for c in colls])
chk("x == log10(baseMean)", np.isclose(np.sort(xs), np.sort(np.log10(res.baseMean))).all())
chk("y == log2FoldChange (shrunken)", np.isclose(np.sort(ys), np.sort(res.log2FoldChange)).all())
chk("layers rasterized", all(c.get_rasterized() for c in colls))
chk("y=0 reference line present", any(abs(l.get_ydata()[0]) < 1e-12 for l in ax.lines))
lo = raw.baseMean < 5
print(f"baseMean<5: n={lo.sum()}, max|LFC| raw={raw.log2FoldChange[lo].abs().max():.2f}, apeglm={res.log2FoldChange[lo].abs().max():.2f}")
chk("shrinkage fan diagnostic: raw max|LFC| at low counts >> apeglm", raw.log2FoldChange[lo].abs().max() > 1.5 * res.log2FoldChange[lo].abs().max())
# rasterization / PDF-size claim: 'vector scatter creates 5MB+ PDFs' for >5000 points
sizes = {}
for rast in (True, False):
    f, a = plt.subplots(figsize=(6, 5))
    for m, c in ((~((res.padj < .05) & res.padj.notna()), "#999999"), (((res.padj < .05) & res.padj.notna()), "#D55E00")):
        a.scatter(np.log10(res.loc[m, "baseMean"]), res.loc[m, "log2FoldChange"], c=c, s=4, alpha=.5, rasterized=rast)
    p = os.path.join(D, "figs", f"i3b_pdf_raster_{rast}.pdf"); f.savefig(p); plt.close(f); sizes[rast] = os.path.getsize(p)
print("PDF size rasterized=True:", sizes[True], "bytes; rasterized=False:", sizes[False], "bytes")
chk("Skill claim: vector scatter of ~33k points >= 5 MB", sizes[False] >= 5e6, f"(measured {sizes[False]/1e6:.2f} MB)")
chk("rasterized PDF is much smaller (<0.5 MB)", sizes[True] < 5e5, f"(measured {sizes[True]/1e3:.0f} KB)")
print("SUMMARY fails =", fails)
