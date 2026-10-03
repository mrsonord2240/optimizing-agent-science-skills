"""Re-audit m2 (MPL-007 edge): how robust is the section-7 recipe (extent=[0,0,0.78,1] + moved fig.legends[0]) to a longer legend title, longer labels and more classes,
and is there a public (non-_figure) route? Same recipe text as scripts/matplotlib_phd.py section 7, only the data labels/title change. Usage: py.sh m2_legend_stress.py <outdir>"""
import sys, os, re
from pathlib import Path
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True); os.chdir(out)
import matplotlib as mpl; mpl.use("Agg")
import matplotlib.pyplot as plt, numpy as np, pandas as pd, seaborn as sns, seaborn.objects as so
print('matplotlib', mpl.__version__, 'seaborn', sns.__version__)
mpl.rcParams.update({'pdf.fonttype': 42, 'font.family': 'sans-serif', 'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'], 'font.size': 7, 'axes.labelsize': 7,
                     'axes.titlesize': 7, 'xtick.labelsize': 6, 'ytick.labelsize': 6, 'legend.fontsize': 6, 'savefig.dpi': 300, 'axes.linewidth': 0.5})
rng = np.random.default_rng(0)
def frame(labels):
    return pd.DataFrame({'log_fc': rng.normal(size=500), 'neg_log_p': rng.exponential(2, size=500), 'cls': rng.choice(labels, 500)})
OKABE = ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7', '#000000']
def box(p):
    m = re.search(rb"/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]", Path(p).read_bytes()); a = list(map(float, m.groups())); return round((a[2]-a[0])/72*25.4, 2), round((a[3]-a[1])/72*25.4, 2)
rows = []
def recipe(tag, labels, title, extent_w=0.78):
    df = frame(labels).rename(columns={'cls': title}); import itertools; pal = dict(zip(labels, itertools.cycle(OKABE)))
    plot = (so.Plot(df, x='log_fc', y='neg_log_p').add(so.Dots(pointsize=2), color=title).scale(color=pal)
              .theme({**sns.axes_style('ticks'), **mpl.rcParams}).layout(size=(89 / 25.4, 70 / 25.4), extent=[0, 0, extent_w, 1]).label(x='log2 fold change', y='-log10(p)'))
    p = plot.plot(); fig = p._figure
    legend = fig.legends[0]; legend.set_loc('center right'); legend.set_bbox_to_anchor((1.0, 0.5), transform=fig.transFigure)
    p.save(f'{tag}.pdf')   # the layout extent is applied at save time (m2b_axes_probe.py), so measure after it, as the recipe's final step does
    fig.canvas.draw(); r = fig._get_renderer(); lb = legend.get_window_extent(r).transformed(fig.transFigure.inverted())
    ab = fig.axes[0].get_tightbbox(r).transformed(fig.transFigure.inverted())
    inside = lb.x0 >= -1e-6 and lb.x1 <= 1 + 1e-6 and lb.y0 >= -1e-6 and lb.y1 <= 1 + 1e-6; clear = lb.x0 >= ab.x1 - 1e-3
    pg = box(f'{tag}.pdf')
    print(f"{tag:34s} legend x {lb.x0:.3f}-{lb.x1:.3f} y {lb.y0:.3f}-{lb.y1:.3f} | axes tight x1 {ab.x1:.3f} | inside page {inside} | clear of axes {clear} | page {pg}")
    rows.append((tag, inside, clear, pg)); plt.close(fig)
recipe('A_skill_labels', ['NS', 'Down', 'Up'], 'significance')
recipe('B_long_title', ['NS', 'Down', 'Up'], 'Differential expression class (DESeq2, padj < 0.05)')
recipe('C_long_labels', ['Not significant', 'Downregulated', 'Upregulated'], 'significance')
recipe('D_long_title_long_labels', ['Not significant', 'Downregulated in treated', 'Upregulated in treated'], 'Differential expression class')
recipe('E_eight_classes', [f'cluster {i}' for i in range(8)], 'cluster')
recipe('F_twelve_classes', [f'cluster {i}' for i in range(12)], 'cluster')
recipe('G_long_title_wider_extent_0.70', ['Not significant', 'Downregulated in treated', 'Upregulated in treated'], 'Differential expression class', extent_w=0.70)
print('--- summary')
for t, i, c, pg in rows: print(f"{t:34s} inside={i} clear={c} page={pg}")
# --- public route: Plot.on(fig) with a user-made Figure, legend reached via fig.legends (no private attribute)
fig = plt.figure(figsize=(89 / 25.4, 70 / 25.4))
df = frame(['NS', 'Down', 'Up']).rename(columns={'cls': 'significance'}); pal = {'NS': '#999999', 'Down': '#0072B2', 'Up': '#D55E00'}
pl = (so.Plot(df, x='log_fc', y='neg_log_p').add(so.Dots(pointsize=2), color='significance').scale(color=pal)
        .theme({**sns.axes_style('ticks'), **mpl.rcParams}).label(x='log2 fold change', y='-log10(p)').on(fig))
pl.plot()   # draws into `fig`; no private attribute used below
print('public route: figure legends', len(fig.legends), '| axes', len(fig.axes), '| fig mm', fig.get_size_inches() * 25.4)
fig.savefig('H_public_on_fig.pdf'); fig.canvas.draw(); r = fig._get_renderer()
if fig.legends:
    lb = fig.legends[0].get_window_extent(r).transformed(fig.transFigure.inverted()); print('public route legend bbox x', round(lb.x0, 3), round(lb.x1, 3), 'inside page', lb.x1 <= 1 + 1e-6)
print('public route page', box('H_public_on_fig.pdf'))

# public route, complete: user-made Figure + Plot.on(fig); move the legend and reserve the right margin with subplots_adjust (no private attribute)
plt.close('all')
fig = plt.figure(figsize=(89 / 25.4, 70 / 25.4))
(so.Plot(df, x='log_fc', y='neg_log_p').add(so.Dots(pointsize=2), color='significance').scale(color=pal if False else {'NS': '#999999', 'Down': '#0072B2', 'Up': '#D55E00'})
   .theme({**sns.axes_style('ticks'), **mpl.rcParams}).label(x='log2 fold change', y='-log10(p)').on(fig).plot())
leg = fig.legends[0]; leg.set_loc('center right'); leg.set_bbox_to_anchor((1.0, 0.5), transform=fig.transFigure)
fig.subplots_adjust(left=0.13, bottom=0.17, right=0.76, top=0.97)
fig.savefig('I_public_on_fig_moved.pdf'); fig.canvas.draw(); r = fig._get_renderer()
lb = leg.get_window_extent(r).transformed(fig.transFigure.inverted()); ab = fig.axes[0].get_tightbbox(r).transformed(fig.transFigure.inverted())
print(f"public route complete: legend x {lb.x0:.3f}-{lb.x1:.3f} | axes tight x1 {ab.x1:.3f} | inside page {lb.x1 <= 1 + 1e-6 and lb.x0 >= 0} | clear {lb.x0 >= ab.x1 - 1e-3} | page {box('I_public_on_fig_moved.pdf')}")
