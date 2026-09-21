"""Input 2 (Variant A): 'Give me a 2x3 multi-panel figure: scatter with colorbar, line+CI, bar, boxplot, histogram, heatmap' -- SKILL.md 'Common Chart Types' block (2) run verbatim, segment by segment.
SYNTHETIC data. Each blank-line-separated segment is exec'd on a fresh Axes in a namespace holding only what the Skill's own blocks define plus data variables named as the snippet expects; np is NOT pre-supplied
unless the snippet imports it (to see what the block needs). Errors and warnings are recorded, not hidden."""
import os, sys, warnings
os.makedirs('out', exist_ok=True); os.chdir('out'); sys.path.insert(0, '..')
import numpy as np, matplotlib as mpl, matplotlib.pyplot as plt
from blocks import blocks
B = blocks()
exec(B[0])  # rcParams block
rng = np.random.default_rng(1)
N = 2000
x = rng.normal(size=N); y = x * 0.5 + rng.normal(size=N); values = np.exp(0.3 * x + rng.normal(scale=0.3, size=N))
xs = np.linspace(0, 10, 50); y1 = np.sin(xs); y2 = np.sin(xs) * 0.6 + 0.4; y_low = y1 - 0.2; y_high = y1 + 0.2
categories = ['Ctl', 'DrugA', 'DrugB']; vals = [3.1, 4.7, 2.2]
group_a, group_b, group_c = rng.normal(0, 1, 40), rng.normal(1, 1, 40), rng.normal(2, 1, 40)
matrix = rng.normal(size=(30, 12))
segs = [s for s in B[2].split('\n\n') if s.strip()]
print(len(segs), 'segments in block 2')
ns_base = dict(plt=plt, np=np, x=xs, y=y, y1=y1, y2=y2, y_low=y_low, y_high=y_high, values=values,
               categories=categories, group_a=group_a, group_b=group_b, group_c=group_c, matrix=matrix)
# scatter needs x,y of equal length N; line needs xs
results = []
for i, s in enumerate(segs):
    fig, ax = plt.subplots(figsize=(89/25.4, 70/25.4), constrained_layout=True)
    ns = dict(ns_base, ax=ax, fig=fig)
    if s.lstrip().startswith('# Scatter'): ns['x'] = x
    if s.lstrip().startswith('# Bar'): ns['values'] = vals
    if s.lstrip().startswith('# Histogram'): ns['values'] = values
    if s.lstrip().startswith('# Line'): ns['x'] = xs; ns['y1'] = y1
    first = s.strip().splitlines()[0]
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        try:
            exec(s, ns)
            status = 'ok'
        except Exception as e:
            status = f'{type(e).__name__}: {e}'
    ws = sorted({f'{ww.category.__name__}: {str(ww.message)[:150]}' for ww in w})
    print(f'SEG{i} [{first[:50]}] -> {status}; warnings={ws}')
    fig.savefig(f'chart{i}.png')
    results.append((i, status))
    plt.close(fig)
# now with the heatmap's undefined vmax defined by the caller
seg = segs[-1]
fig, ax = plt.subplots(figsize=(89/25.4, 70/25.4), constrained_layout=True)
vmax = np.quantile(np.abs(matrix), 0.99)
exec(seg, dict(plt=plt, ax=ax, matrix=matrix, vmax=vmax))
fig.savefig('chart_heat_fixed.png')
print('fixed heatmap: image array shape', ax.images[0].get_array().shape, 'clim', ax.images[0].get_clim(), 'vmax', round(vmax, 3))
# composite 2x3
fig, axs = plt.subplots(2, 3, figsize=(180/25.4, 100/25.4), constrained_layout=True)
sc = axs[0,0].scatter(x, y, c=values, cmap='viridis', s=8, alpha=0.6, edgecolors='none', rasterized=True)
plt.colorbar(axs[0,0].collections[0], ax=axs[0,0], label='Expression', shrink=0.8)
axs[0,1].plot(xs, y1, color='#0072B2', label='Control', linewidth=1); axs[0,1].plot(xs, y2, color='#D55E00', label='Treatment', linewidth=1)
axs[0,1].fill_between(xs, y_low, y_high, color='#0072B2', alpha=0.2); axs[0,1].legend(frameon=False, fontsize=6)
axs[0,2].bar(categories, vals, color='#0072B2', edgecolor='black', linewidth=0.5)
axs[1,0].boxplot([group_a, group_b, group_c], tick_labels=['A','B','C'], patch_artist=True, boxprops=dict(facecolor='#0072B2', alpha=0.7))
axs[1,1].hist(values, bins=30, color='#0072B2', edgecolor='white', linewidth=0.5)
im = axs[1,2].imshow(matrix, cmap='RdBu_r', aspect='auto', vmin=-vmax, vmax=vmax); plt.colorbar(im, ax=axs[1,2], label='Z-score')
for a, t in zip(axs.flat, list('abcdef')): a.text(-0.2, 1.08, t, transform=a.transAxes, fontsize=10, fontweight='bold')
fig.savefig('multi2x3.png'); fig.savefig('multi2x3.pdf')
# numeric asserts
print('bar heights', [round(p.get_height(), 2) for p in axs[0,2].patches], 'expected', vals)
print('hist total count', int(sum(p.get_height() for p in axs[1,1].patches)), 'expected', N)
print('boxplot medians', [round(m.get_ydata()[0], 2) for m in axs[1,0].lines if len(m.get_ydata())==2 and m.get_ydata()[0]==m.get_ydata()[1]][:3], 'np.median', [round(float(np.median(g)), 2) for g in (group_a, group_b, group_c)])
print('xticklabels box', [t.get_text() for t in axs[1,0].get_xticklabels()])
print('bar xticklabels', [t.get_text() for t in axs[0,2].get_xticklabels()])
print('colorbar labels', [a.get_ylabel() for a in fig.axes if a.get_ylabel()])
from pdfcheck import pdf_info; print(pdf_info('multi2x3.pdf'))
