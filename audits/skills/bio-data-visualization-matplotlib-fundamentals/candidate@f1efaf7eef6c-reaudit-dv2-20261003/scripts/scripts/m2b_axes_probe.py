"""Diagnose the axes-vs-legend measurement difference between m1 (0.750) and m2 (0.900). Usage: py.sh m2b_axes_probe.py <outdir>"""
import sys, os
from pathlib import Path
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True); os.chdir(out)
import matplotlib as mpl; mpl.use("Agg")
import matplotlib.pyplot as plt, numpy as np, pandas as pd, seaborn as sns, seaborn.objects as so
mpl.rcParams.update({'pdf.fonttype': 42, 'font.family': 'sans-serif', 'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'], 'font.size': 7, 'axes.labelsize': 7, 'axes.titlesize': 7, 'xtick.labelsize': 6, 'ytick.labelsize': 6, 'legend.fontsize': 6, 'savefig.dpi': 300, 'axes.linewidth': 0.5})
rng = np.random.default_rng(0)
df = pd.DataFrame({'log_fc': rng.normal(size=500), 'neg_log_p': rng.exponential(2, size=500), 'significance': rng.choice(['NS','Down','Up'], 500)})
pal = {'NS': '#999999', 'Down': '#0072B2', 'Up': '#D55E00'}
plot = (so.Plot(df, x='log_fc', y='neg_log_p').add(so.Dots(pointsize=2), color='significance').scale(color=pal).theme({**sns.axes_style('ticks'), **mpl.rcParams})
        .layout(size=(89 / 25.4, 70 / 25.4), extent=[0, 0, 0.78, 1]).label(x='log2 fold change', y='-log10(p)'))
p = plot.plot(); fig = p._figure
print('layout engine:', type(fig.get_layout_engine()).__name__)
ax = fig.axes[0]
def report(tag):
    fig.canvas.draw(); r = fig._get_renderer()
    ab = ax.get_tightbbox(r).transformed(fig.transFigure.inverted()); pos = ax.get_position(); lb = fig.legends[0].get_window_extent(r).transformed(fig.transFigure.inverted())
    print(f"{tag:40s} axes pos x {pos.x0:.3f}-{pos.x1:.3f} | axes tight x {ab.x0:.3f}-{ab.x1:.3f} | legend x {lb.x0:.3f}-{lb.x1:.3f}")
report('after plot(), legend not moved')
leg = fig.legends[0]; leg.set_loc('center right'); leg.set_bbox_to_anchor((1.0, 0.5), transform=fig.transFigure)
report('after move, first draw')
p.save('probe.pdf'); report('after save + draw')
fig.savefig('probe2.pdf'); report('after 2nd savefig + draw')
