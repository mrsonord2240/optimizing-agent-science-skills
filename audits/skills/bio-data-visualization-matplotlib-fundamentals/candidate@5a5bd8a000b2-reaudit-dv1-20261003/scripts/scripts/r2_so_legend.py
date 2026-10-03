"""Re-audit 2: is the legend=False on the seaborn.objects example a necessary tradeoff? Try legend on, with default / constrained engine / extent. Usage: py.sh r2_so_legend.py <outdir>"""
import sys, os
from pathlib import Path
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True); os.chdir(out)
import numpy as np, pandas as pd, matplotlib as mpl, matplotlib.pyplot as plt, seaborn as sns, seaborn.objects as so
mpl.rcParams.update({'pdf.fonttype': 42, 'font.sans-serif': ['Arial'], 'font.size': 7, 'axes.labelsize': 7, 'xtick.labelsize': 6, 'ytick.labelsize': 6, 'legend.fontsize': 6, 'axes.linewidth': .5})
rng = np.random.default_rng(0)
df = pd.DataFrame({'log_fc': rng.normal(size=500), 'neg_log_p': rng.exponential(2, size=500), 'significance': rng.choice(['Up','Down','NS'], 500)})
pal = {'NS': '#999999', 'Down': '#0072B2', 'Up': '#D55E00'}
def base(legend=True):
    return (so.Plot(df, x='log_fc', y='neg_log_p').add(so.Dots(pointsize=2), color='significance', legend=legend).scale(color=pal)
            .theme({**sns.axes_style('ticks'), **mpl.rcParams}).label(x='log2 fold change', y='-log10(p)'))
variants = {
 'A_default_legend': base().layout(size=(89/25.4, 70/25.4)),
 'B_constrained_legend': base().layout(size=(89/25.4, 70/25.4), engine='constrained'),
 'C_tight_legend': base().layout(size=(89/25.4, 70/25.4), engine='tight'),
 'D_extent_legend': base().layout(size=(89/25.4, 70/25.4), extent=[0, 0, 0.8, 1]),
}
for k, p in variants.items():
    pl = p.plot(); fig = pl._figure; fig.canvas.draw()
    r = fig._get_renderer(); fb = fig.bbox
    legs = fig.legends
    bb = [l.get_window_extent(r) for l in legs]
    inside = all(b.x0 >= fb.x0-0.5 and b.x1 <= fb.x1+0.5 and b.y0 >= fb.y0-0.5 and b.y1 <= fb.y1+0.5 for b in bb) if bb else None
    print(k, 'legends', len(legs), 'legend bbox', [(round(b.x0),round(b.x1)) for b in bb], 'fig px width', round(fb.x1), 'legend fully inside page:', inside)
    pl.save(f'{k}.pdf'); plt.close(fig)
    import re
    m = re.search(rb"/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]", Path(f'{k}.pdf').read_bytes()); a = list(map(float, m.groups()))
    print('   page mm', round((a[2]-a[0])/72*25.4, 2), round((a[3]-a[1])/72*25.4, 2))

# E: keep the legend but pull it inside the page after plot()
pl = base().layout(size=(89/25.4, 70/25.4), extent=[0, 0, 0.78, 1]).plot(); fig = pl._figure
leg = fig.legends[0]; leg.set_loc('center right'); leg.set_bbox_to_anchor((1.0, 0.5), transform=fig.transFigure)
fig.canvas.draw(); r = fig._get_renderer(); b = leg.get_window_extent(r); fb = fig.bbox
print('E_move_legend bbox x', round(b.x0), round(b.x1), 'page px', round(fb.x1), 'inside:', b.x0 >= 0 and b.x1 <= fb.x1 and b.y0 >= 0 and b.y1 <= fb.y1)
ax = fig.axes[0]; print('E axes right edge px', round(ax.get_window_extent(r).x1), 'legend left px', round(b.x0))
pl.save("E_move_legend.pdf"); plt.close(fig)
