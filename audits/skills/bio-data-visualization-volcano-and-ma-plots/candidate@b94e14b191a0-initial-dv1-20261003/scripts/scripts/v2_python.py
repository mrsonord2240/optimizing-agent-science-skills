"""VOL audit run 2: scripts/ma_plot.py on the real shrunken airway table, adjustText volcano (SKILL.md Python route), and the
sanbomics claim ('sanbomics.tools.volcano'). Usage:
  PYTHONPATH=F:/OpenScience/audit-envs/data-visualization/py-extra/sanbomics py.sh v2_python.py <skilldir> <r_outdir> <outdir>"""
import importlib.util, re, sys
from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

skill, rout, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)


def chk(label, cond):
    print(f"[{'PASS' if cond else 'FAIL'}] {label}")


spec = importlib.util.spec_from_file_location("ma_plot", skill / "scripts" / "ma_plot.py"); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
res = pd.read_csv(rout / "airway_shrunk_apeglm.csv")
print("rows", len(res), "baseMean NA", int(res.baseMean.isna().sum()), "padj NA", int(res.padj.isna().sum()), "padj<0.05", int((res.padj < .05).sum()))
ax = m.ma_plot(res); fig = ax.figure
n_orange = len(ax.collections[1].get_offsets()); n_grey = len(ax.collections[0].get_offsets())
print("ma_plot: grey", n_grey, "orange", n_orange)
chk("orange points equal padj < 0.05 count (independent)", n_orange == int((res.padj < .05).sum()))
chk("grey points equal the rest including padj NA", n_grey == len(res) - int((res.padj < .05).sum()))
fig.savefig(out / "ma_plot_py.png", dpi=150); fig.savefig(out / "ma_plot_py_raster.pdf"); plt.close(fig)
# vector control to test the '5MB+' claim by removing rasterized
fig, ax = plt.subplots(figsize=(6, 5)); sig = res.padj < .05
ax.scatter(np.log10(res.loc[~sig, 'baseMean']), res.loc[~sig, 'log2FoldChange'], c='#999999', s=4, alpha=.4)
ax.scatter(np.log10(res.loc[sig, 'baseMean']), res.loc[sig, 'log2FoldChange'], c='#D55E00', s=6, alpha=.7); fig.savefig(out / "ma_plot_py_vector.pdf"); plt.close(fig)
sz = {k: (out / k).stat().st_size for k in ("ma_plot_py_raster.pdf", "ma_plot_py_vector.pdf")}
print("ma_plot PDF sizes:", sz, "| ratio", round(sz["ma_plot_py_vector.pdf"] / sz["ma_plot_py_raster.pdf"], 1))
chk("vector scatter of 29,391 points gives a 5 MB+ PDF (SKILL.md: 'vector scatter creates 5MB+ PDFs')", sz["ma_plot_py_vector.pdf"] > 5e6)
# does ma_plot honour the Skill's fonttype/size conventions? (function uses figsize 6x5 in when ax is None)
fig, ax = plt.subplots(figsize=(89 / 25.4, 70 / 25.4), layout='constrained'); m.ma_plot(res, ax=ax); fig.savefig(out / "ma_plot_89.png", dpi=200); plt.close(fig)
# adjustText volcano
from adjustText import adjust_text
d = res.dropna(subset=['padj', 'pvalue']).copy(); d['nlp'] = -np.log10(d.pvalue)
top = d.assign(score=d.nlp * d.log2FoldChange.abs()).nlargest(12, 'score')
fig, ax = plt.subplots(figsize=(4, 4), layout='constrained'); ax.scatter(d.log2FoldChange, d.nlp, s=2, c='#999999', rasterized=True)
tx = [ax.text(r.log2FoldChange, r.nlp, r.gene, fontsize=6) for r in top.itertuples()]
adjust_text(tx, ax=ax, arrowprops=dict(arrowstyle='-', lw=.3)); fig.savefig(out / "adjusttext_volcano.png", dpi=200)
fig.canvas.draw(); r = fig.canvas.get_renderer(); bbs = [t.get_window_extent(r) for t in tx]
ov = sum(bbs[i].overlaps(bbs[j]) for i in range(len(bbs)) for j in range(i + 1, len(bbs)))
print("adjustText: 12 labels, overlapping label pairs:", ov)
chk("adjustText labels do not overlap each other", ov == 0)
# sanbomics claim
try:
    import sanbomics.tools as t
    print("sanbomics.tools imported; has volcano:", hasattr(t, 'volcano'))
except Exception as e:
    print("import sanbomics.tools ->", type(e).__name__, str(e)[:100])
try:
    import sanbomics.plots as p
    print("sanbomics.plots.volcano exists:", hasattr(p, 'volcano'))
except Exception as e:
    print("import sanbomics.plots ->", type(e).__name__, str(e)[:100])
