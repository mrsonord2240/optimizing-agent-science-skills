"""Does the Skill's public route as worded (right=0.76 only) put any ink on the page edge? Renders to PNG at 300 dpi and reports ink rows nearest the edges.
Usage: py.sh d1_ink_probe.py <outdir>"""
import sys, os
from pathlib import Path
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True); os.chdir(out)
import matplotlib as mpl; mpl.use("Agg")
import matplotlib.pyplot as plt, numpy as np, pandas as pd, seaborn as sns, seaborn.objects as so
mpl.rcParams.update({'pdf.fonttype': 42, 'font.family': 'sans-serif', 'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'], 'font.size': 7, 'axes.labelsize': 7,
                     'axes.titlesize': 7, 'xtick.labelsize': 6, 'ytick.labelsize': 6, 'legend.fontsize': 6, 'savefig.dpi': 300, 'axes.linewidth': 0.5})
rng = np.random.default_rng(0)
df = pd.DataFrame({'log_fc': rng.normal(size=500), 'neg_log_p': rng.exponential(2, size=500), 'significance': rng.choice(['NS', 'Down', 'Up'], 500)})
pal = {'NS': '#999999', 'Down': '#0072B2', 'Up': '#D55E00'}
for tag, kw in (('right076_only', dict(right=0.76)), ('measured_args', dict(left=0.13, bottom=0.17, right=0.76, top=0.97))):
    fig = plt.figure(figsize=(89 / 25.4, 70 / 25.4))
    (so.Plot(df, x='log_fc', y='neg_log_p').add(so.Dots(pointsize=2), color='significance').scale(color=pal).theme({**sns.axes_style('ticks'), **mpl.rcParams}).label(x='log2 fold change', y='-log10(p)').on(fig).plot())
    leg = fig.legends[0]; leg.set_loc('center right'); leg.set_bbox_to_anchor((1.0, 0.5), transform=fig.transFigure)
    fig.subplots_adjust(**kw); fig.savefig(f'{tag}.png', dpi=300); plt.close(fig)
    a = plt.imread(f'{tag}.png')[..., :3]; ink = (a < 0.97).any(axis=2)
    rows = np.where(ink.any(axis=1))[0]; cols = np.where(ink.any(axis=0))[0]; h, w = ink.shape
    print(f"{tag:16s} px {w}x{h} | ink rows {rows.min()}..{rows.max()} (bottom margin {h-1-rows.max()} px) | ink cols {cols.min()}..{cols.max()} (right margin {w-1-cols.max()} px, left {cols.min()} px) | top margin {rows.min()} px")
