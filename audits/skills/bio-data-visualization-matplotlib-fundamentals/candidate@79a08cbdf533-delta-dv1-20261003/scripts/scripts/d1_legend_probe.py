"""Delta check of the MPL-010 wording: (a) 29-character title ('Differential expression class') with the SHIPPED labels and with longer labels: overflow into the axes in mm;
(b) the public route exactly as the Skill now words it (Plot.on(fig), move fig.legends[0], fig.subplots_adjust(right=0.76) ONLY): legend inside page, clear of axes, axis labels not clipped.
Usage: py.sh d1_legend_probe.py <outdir>"""
import sys, os, re, itertools
from pathlib import Path
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True); os.chdir(out)
import matplotlib as mpl; mpl.use("Agg")
import matplotlib.pyplot as plt, numpy as np, pandas as pd, seaborn as sns, seaborn.objects as so
print('matplotlib', mpl.__version__, 'seaborn', sns.__version__)
mpl.rcParams.update({'pdf.fonttype': 42, 'font.family': 'sans-serif', 'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'], 'font.size': 7, 'axes.labelsize': 7,
                     'axes.titlesize': 7, 'xtick.labelsize': 6, 'ytick.labelsize': 6, 'legend.fontsize': 6, 'savefig.dpi': 300, 'axes.linewidth': 0.5})
rng = np.random.default_rng(0)
def frame(labels, title):
    return pd.DataFrame({'log_fc': rng.normal(size=500), 'neg_log_p': rng.exponential(2, size=500), title: rng.choice(labels, 500)})
OKABE = ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7', '#000000']
W = 89.0
def recipe(tag, labels, title):
    df = frame(labels, title); pal = dict(zip(labels, itertools.cycle(OKABE)))
    plot = (so.Plot(df, x='log_fc', y='neg_log_p').add(so.Dots(pointsize=2), color=title).scale(color=pal)
              .theme({**sns.axes_style('ticks'), **mpl.rcParams}).layout(size=(89 / 25.4, 70 / 25.4), extent=[0, 0, 0.78, 1]).label(x='log2 fold change', y='-log10(p)'))
    p = plot.plot(); fig = p._figure
    legend = fig.legends[0]; legend.set_loc('center right'); legend.set_bbox_to_anchor((1.0, 0.5), transform=fig.transFigure)
    p.save(f'{tag}.pdf'); fig.canvas.draw(); r = fig._get_renderer()
    lb = legend.get_window_extent(r).transformed(fig.transFigure.inverted()); ab = fig.axes[0].get_tightbbox(r).transformed(fig.transFigure.inverted())
    print(f"{tag:34s} title chars {len(title)} | legend x {lb.x0:.3f}-{lb.x1:.3f} | axes tight x1 {ab.x1:.3f} | overlap into axes {max(0, ab.x1 - lb.x0) * W:.1f} mm"); plt.close(fig)
recipe('a1_29char_title_shipped_labels', ['NS', 'Down', 'Up'], 'Differential expression class')
recipe('a2_29char_title_long_labels', ['Not significant', 'Downregulated in treated', 'Upregulated in treated'], 'Differential expression class')
recipe('a3_shipped', ['NS', 'Down', 'Up'], 'significance')
# public route, ONLY right=0.76 as the Skill words it
plt.close('all'); pal = {'NS': '#999999', 'Down': '#0072B2', 'Up': '#D55E00'}
df = frame(['NS', 'Down', 'Up'], 'significance'); fig = plt.figure(figsize=(89 / 25.4, 70 / 25.4))
(so.Plot(df, x='log_fc', y='neg_log_p').add(so.Dots(pointsize=2), color='significance').scale(color=pal).theme({**sns.axes_style('ticks'), **mpl.rcParams}).label(x='log2 fold change', y='-log10(p)').on(fig).plot())
leg = fig.legends[0]; leg.set_loc('center right'); leg.set_bbox_to_anchor((1.0, 0.5), transform=fig.transFigure)
fig.subplots_adjust(right=0.76); fig.savefig('b_public_right076_only.pdf'); fig.canvas.draw(); r = fig._get_renderer()
inv = fig.transFigure.inverted(); lb = leg.get_window_extent(r).transformed(inv); ab = fig.axes[0].get_tightbbox(r).transformed(inv)
print(f"public route right=0.76 only: legend x {lb.x0:.3f}-{lb.x1:.3f} | axes tight x {ab.x0:.3f}-{ab.x1:.3f} y {ab.y0:.3f}-{ab.y1:.3f} | legend inside page {lb.x0>=0 and lb.x1<=1+1e-6} | clear of axes {lb.x0 >= ab.x1 - 1e-3} | axes+labels inside page {ab.x0>=-1e-6 and ab.y0>=-1e-6 and ab.x1<=1+1e-6 and ab.y1<=1+1e-6}")
