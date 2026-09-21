"""Input 3 (Edge): 'Volcano-style scatter of my DE results into a pre-created Axes with seaborn, Okabe-Ito colors for Up/Down/NS; then the same with seaborn.objects; and a displot to confirm the FacetGrid gotcha.'
SYNTHETIC DE table (5000 genes, planted 200 up / 200 down). SKILL.md block 3 exec'd verbatim."""
import os, sys, warnings
os.makedirs('out', exist_ok=True); os.chdir('out'); sys.path.insert(0, '..')
import numpy as np, pandas as pd, matplotlib as mpl, matplotlib.pyplot as plt
from blocks import blocks
B = blocks(); exec(B[0])
rng = np.random.default_rng(7)
n = 5000
lfc = rng.normal(0, 0.6, n); lfc[:200] += 2.5; lfc[200:400] -= 2.5
p = np.clip(10 ** (-np.abs(lfc) * 2.0 - rng.exponential(0.5, n)), 1e-300, 1)
df = pd.DataFrame({'log_fold_change': lfc, 'neg_log_p': -np.log10(p)})
df['significance'] = np.where((df.neg_log_p > 2) & (df.log_fold_change > 1), 'Up',
                      np.where((df.neg_log_p > 2) & (df.log_fold_change < -1), 'Down', 'NS'))
print(df.significance.value_counts().to_dict(), '| planted up/down 200/200')
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always')
    exec(B[3])
    print('block 3 ran; warnings:', sorted({f'{x.category.__name__}: {str(x.message)[:120]}' for x in w}))
fig = plt.gcf(); ax = fig.axes[0]
ax.set_xlabel('log2FC'); ax.set_ylabel('-log10 p')
fig.savefig('volcano_sns.png'); fig.savefig('volcano_sns.pdf')
# what colour did each category actually get?
cols = {}
for coll in ax.collections:
    fc = coll.get_facecolor(); print('collection n =', len(coll.get_offsets()), 'rgb0', mpl.colors.to_hex(fc[0]))
print('legend labels', [t.get_text() for t in ax.get_legend().get_texts()], 'legend colours', [mpl.colors.to_hex(h.get_color()) for h in ax.get_legend().legend_handles])
ol = {c: mpl.colors.to_hex(coll.get_facecolor()[0]) for c, coll in zip(sorted(df.significance.unique()), ax.collections)}
print('category -> colour (sorted order, as seaborn assigns for a list palette):', ol)
print('intended by usage-guide "Up/Down/NS" and by the list [grey, blue, orange]: NS grey #999999, Up blue #0072B2, Down orange #D55E00')
# same with explicit dict => correct mapping
fig2, ax2 = plt.subplots(figsize=(89/25.4, 70/25.4), constrained_layout=True)
import seaborn as sns
sns.scatterplot(data=df, x='log_fold_change', y='neg_log_p', hue='significance', palette={'NS': '#999999', 'Up': '#0072B2', 'Down': '#D55E00'}, s=10, alpha=0.7, ax=ax2, rasterized=True)
fig2.savefig('volcano_dict.png')
# seaborn.objects (verbatim tail of block 3) rendered
import seaborn.objects as so
pl = (so.Plot(df, x='log_fold_change', y='neg_log_p').add(so.Dots(pointsize=2), color='significance').scale(color=['#999999', '#0072B2', '#D55E00']))
print('so.Plot type', type(pl).__name__, '(block 3 never calls .plot()/.save()/.show(): nothing rendered by itself)')
pl.save('volcano_so.png'); print('so saved')
# FacetGrid gotcha
g = sns.displot(df, x='log_fold_change')
print('displot returns', type(g).__name__, '| has set_xlabel:', hasattr(g, 'set_xlabel'), '| has set_axis_labels:', hasattr(g, 'set_axis_labels'))
try: g.set_xlabel('x')
except Exception as e: print('g.set_xlabel ->', type(e).__name__, e)
g.set_axis_labels('log2FC', 'count'); print('set_axis_labels ok:', g.ax.get_xlabel())
ax3 = sns.scatterplot(data=df, x='log_fold_change', y='neg_log_p'); print('scatterplot returns', type(ax3).__name__)
# hit counts in the figure vs input
n_pts = sum(len(c.get_offsets()) for c in ax.collections); print('points drawn', n_pts, 'input rows', len(df))
