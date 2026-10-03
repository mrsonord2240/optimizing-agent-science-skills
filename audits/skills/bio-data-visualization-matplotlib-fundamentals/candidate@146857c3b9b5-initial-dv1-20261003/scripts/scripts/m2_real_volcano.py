"""MPL audit run 2: the Skill's own seaborn volcano recipe (SKILL.md 'seaborn Integration' and scripts/matplotlib_phd.py #5)
applied to REAL airway DESeq2 results. Checks that the colour carries the right class, then an Okabe-Ito dict-palette control.
Usage: py.sh m2_real_volcano.py <outdir>"""
import re, sys
from pathlib import Path
import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
mpl.rcParams.update({'pdf.fonttype': 42, 'font.size': 7, 'savefig.dpi': 300, 'savefig.bbox': 'tight'})
res = pd.read_csv("F:/OpenScience/audit-envs/data-visualization/public-data/differential-expression/airway_dex_deseq2_results.csv")
res = res.dropna(subset=['padj', 'pvalue']).copy()
res['log_fold_change'] = res['log2FoldChange']
res['neg_log_p'] = -np.log10(res['pvalue'])
res['significance'] = np.where((res.padj < .05) & (res.log2FoldChange > 1), 'Up',
                      np.where((res.padj < .05) & (res.log2FoldChange < -1), 'Down', 'NS'))
print("rows", len(res), res.significance.value_counts().to_dict())
GREY, BLUE, ORANGE = '#999999', '#0072B2', '#D55E00'


def chk(label, cond):
    print(f"[{'PASS' if cond else 'FAIL'}] {label}")


def colours_by_class(ax, df):
    """Map each class to the face colours actually drawn (the scatter collection, points in df order after seaborn's grouping)."""
    cols = {}
    for coll in ax.collections:
        fc = coll.get_facecolor()
        if len(fc):
            cols[len(cols)] = mcolors.to_hex(fc[0][:3])
    return cols


# 1. SKILL.md recipe verbatim: palette=['#999999', '#0072B2', '#D55E00'] with hue='significance'
fig, ax = plt.subplots(figsize=(4, 3), layout='constrained')
sns.scatterplot(data=res, x='log_fold_change', y='neg_log_p', hue='significance',
                palette=[GREY, BLUE, ORANGE], s=10, alpha=0.7, ax=ax, rasterized=True)
leg = {t.get_text(): mcolors.to_hex(h.get_color()) if hasattr(h, 'get_color') else None
       for t, h in zip(ax.get_legend().get_texts(), ax.get_legend().legend_handles)}
print("legend colours (SKILL.md palette order grey, blue, orange):", leg)
chk("NS is drawn in the documented grey #999999", leg.get('NS', '').lower() == GREY)
chk("Up is drawn in orange and Down in blue (SKILL's Up/Down/NS colours)", leg.get('Up', '').lower() == ORANGE.lower() and leg.get('Down', '').lower() == BLUE.lower())
fig.savefig(out / 'volcano_skill_palette.png'); fig.savefig(out / 'volcano_skill_palette.pdf'); plt.close(fig)
# 2. control: explicit dict palette + hue_order
fig, ax = plt.subplots(figsize=(4, 3), layout='constrained')
sns.scatterplot(data=res, x='log_fold_change', y='neg_log_p', hue='significance', hue_order=['NS', 'Down', 'Up'],
                palette={'NS': GREY, 'Down': BLUE, 'Up': ORANGE}, s=10, alpha=0.7, edgecolor='none', ax=ax, rasterized=True)
leg2 = {t.get_text(): mcolors.to_hex(h.get_color()) for t, h in zip(ax.get_legend().get_texts(), ax.get_legend().legend_handles)}
print("control legend:", leg2)
chk("dict palette + hue_order gives NS grey / Down blue / Up orange", leg2 == {'NS': GREY, 'Down': BLUE, 'Up': ORANGE} or {k: v.lower() for k, v in leg2.items()} == {'NS': GREY, 'Down': BLUE.lower(), 'Up': ORANGE.lower()})
fig.savefig(out / 'volcano_control.png'); plt.close(fig)
# 3. seaborn.objects recipe verbatim (list scale) on real data
import seaborn.objects as so
p = (so.Plot(res, x='log_fold_change', y='neg_log_p').add(so.Dots(pointsize=2), color='significance')
     .scale(color=[GREY, BLUE, ORANGE]))
fg = p.plot(); fg._figure.savefig(out / 'volcano_objects_skill.png', dpi=150)
# colour assigned to the NS class: find via the plotter's legend
leg3 = {}
for item in fg._legend_contents:
    (name, _), artists, labels = item
    for a, l in zip(artists, labels):
        leg3[l] = mcolors.to_hex(a.get_facecolor()[0][:3] if hasattr(a, 'get_facecolor') and len(a.get_facecolor()) else '#000000')
print("seaborn.objects legend colours:", leg3)
chk("seaborn.objects list scale maps NS to grey", leg3.get('NS', '').lower() == GREY)
# 4. real PCA-style scatter with raster flag + file size
n_pts = len(res)
fig, ax = plt.subplots(figsize=(89 / 25.4, 70 / 25.4), layout='constrained')
ax.scatter(res.log2FoldChange, res.neg_log_p, s=4, c=GREY, edgecolors='none', rasterized=True)
fig.savefig(out / 'raster_89.pdf'); plt.close(fig)
fig, ax = plt.subplots(figsize=(89 / 25.4, 70 / 25.4), layout='constrained')
ax.scatter(res.log2FoldChange, res.neg_log_p, s=4, c=GREY, edgecolors='none')
fig.savefig(out / 'vector_89.pdf'); plt.close(fig)
sz = {f: (out / f).stat().st_size for f in ('raster_89.pdf', 'vector_89.pdf')}
print(f"{n_pts} real points: rasterized pdf {sz['raster_89.pdf']} B vs vector {sz['vector_89.pdf']} B")
chk("rasterized=True shrinks the 19k-point PDF by >2x", sz['vector_89.pdf'] > 2 * sz['raster_89.pdf'])
