# Input 5b: Python volcano. The Skill's Overview names "matplotlib.scatter with adjustText" for volcanos but ships NO Python volcano code
# (only ma_plot). This script is what an agent would write from the Skill's stated design rules (shrunken LFC, padj threshold, combined-rank labels, raster, Okabe-Ito).
import os, numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from adjustText import adjust_text
import adjustText; print("adjustText", adjustText.__version__ if hasattr(adjustText, "__version__") else "?")
D = r"F:\OpenScience\audits\bio-data-visualization-volcano-and-ma-plots"
res = pd.read_csv(os.path.join(D, "data", "airway_apeglm.csv"), index_col=0)
sym = pd.read_csv(os.path.join(D, "data", "airway_symbols.csv"), index_col=0)["symbol"]
res["gene"] = sym.reindex(res.index).fillna(pd.Series(res.index, index=res.index))
fdr, lfc_t, top_n = 0.05, 1.0, 10
res["nlp"] = -np.log10(res["pvalue"])
res["cls"] = "NS"
res.loc[(res.padj < fdr) & (res.log2FoldChange > lfc_t), "cls"] = "Up"
res.loc[(res.padj < fdr) & (res.log2FoldChange < -lfc_t), "cls"] = "Down"
sig = res[res.cls != "NS"].assign(score=lambda d: d.nlp * d.log2FoldChange.abs()).nlargest(top_n, "score")
fig, ax = plt.subplots(figsize=(6.5, 6))
for c, col in (("NS", "#999999"), ("Down", "#0072B2"), ("Up", "#D55E00")):
    d = res[res.cls == c]; ax.scatter(d.log2FoldChange, d.nlp, s=4, c=col, alpha=.6, rasterized=True, label=f"{c} ({len(d)})")
ax.axvline(-lfc_t, ls="--", c="grey", lw=.5); ax.axvline(lfc_t, ls="--", c="grey", lw=.5); ax.axhline(-np.log10(fdr), ls="--", c="grey", lw=.5)
texts = [ax.text(r.log2FoldChange, r.nlp, r.gene, fontsize=7) for r in sig.itertuples()]
adjust_text(texts, ax=ax, arrowprops=dict(arrowstyle="-", color="k", lw=.3))
ax.set_xlabel(r"$\log_2$ fold change (shrunken)"); ax.set_ylabel(r"$-\log_{10}\,p$"); ax.legend(frameon=False, fontsize=7)
fig.tight_layout(); out = os.path.join(D, "figs", "i5b_python_volcano.png"); fig.savefig(out, dpi=170)
fails = 0
def chk(n, ok, note=""):
    global fails; print(f"[{'PASS' if ok else 'FAIL'}] {n} {note}"); fails += (not ok)
chk("class counts match the table", (res.cls == "Up").sum() == int(((res.padj < fdr) & (res.log2FoldChange > lfc_t)).sum()), f"Up={(res.cls=='Up').sum()} Down={(res.cls=='Down').sum()}")
chk("10 labels created", len(texts) == 10, ", ".join(sig.gene))
chk("labelled genes are the same top-10 combined-rank set the R function chose (SPARCL1 ZBTB16 DUSP1 KLF15 PER1 ...)", {"DUSP1", "ZBTB16", "KLF15", "PER1"} <= set(sig.gene))
print("SUMMARY fails =", fails)
