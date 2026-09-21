"""Input 5 (Stress/adversarial): 'Nature-ready UMAP of 100,000 cells with 12 clusters, 89 mm, Okabe-Ito colours, colorbar for a marker gene; and check the Skill's Common Failure Modes claims.'
SYNTHETIC 100k-point embedding: 12 Gaussian blobs. Each claim in the Failure Modes section is tested."""
import os, sys, warnings, time
os.makedirs('out', exist_ok=True); os.chdir('out'); sys.path.insert(0, '..')
import numpy as np, matplotlib as mpl, matplotlib.pyplot as plt
from blocks import blocks
from pdfcheck import pdf_info
B = blocks(); exec(B[0])
rng = np.random.default_rng(11)
K, N = 12, 100_000
centers = rng.uniform(-10, 10, size=(K, 2)); lab = rng.integers(0, K, N)
xy = centers[lab] + rng.normal(scale=0.7, size=(N, 2)); gene = rng.gamma(2, 1, N) * (1 + (lab == 3))
okabe = ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7', '#000000']

# claim: vector scatter at large N makes a huge PDF; rasterized=True fixes it
sizes = {}
for r in (False, True):
    fig, ax = plt.subplots(figsize=(89/25.4, 70/25.4), constrained_layout=True)
    t = time.time(); ax.scatter(xy[:, 0], xy[:, 1], c=gene, s=1, edgecolors='none', rasterized=r); fig.savefig(f'umap_r{int(r)}.pdf'); sizes[r] = (os.path.getsize(f'umap_r{int(r)}.pdf'), round(time.time()-t, 1))
    plt.close(fig)
print('100k scatter PDF bytes (vector, seconds):', sizes[False], '| rasterized:', sizes[True])
# claim: 12 clusters with the Skill's 8-colour Okabe-Ito palette
cols = [okabe[i % len(okabe)] for i in range(K)]
print('12 clusters, palette has', len(okabe), '-> colours reused for clusters', [i for i in range(K) if cols.index(cols[i]) != i], '(Skill gives no guidance for >8 categories)')
import seaborn as sns
try:
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        fig, ax = plt.subplots(figsize=(89/25.4, 70/25.4), constrained_layout=True)
        import pandas as pd
        d = pd.DataFrame({'u1': xy[:5000, 0], 'u2': xy[:5000, 1], 'cl': lab[:5000].astype(str)})
        sns.scatterplot(data=d, x='u1', y='u2', hue='cl', palette=okabe, s=2, ax=ax, rasterized=True)
        print('sns palette with 8 colours for 12 levels ->', 'no error;', [str(x.message)[:100] for x in w])
        print('distinct legend colours', len({mpl.colors.to_hex(h.get_color()) for h in ax.get_legend().legend_handles}), 'of 12 levels')
except Exception as e: print('sns 12 levels with 8 colours ->', type(e).__name__, str(e)[:120])
# UMAP figure per skill: colorbar with shrink/aspect
fig, ax = plt.subplots(figsize=(89/25.4, 70/25.4), constrained_layout=True)
sc = ax.scatter(xy[:, 0], xy[:, 1], c=gene, cmap='viridis', s=1, edgecolors='none', rasterized=True)
cb = plt.colorbar(sc, ax=ax, shrink=0.6, aspect=20, label='Gene X'); ax.set_xlabel('UMAP1'); ax.set_ylabel('UMAP2'); ax.spines[['top','right']].set_visible(False)
fig.savefig('umap_cb.pdf'); fig.savefig('umap_cb.png')
i = pdf_info('umap_cb.pdf'); print('umap_cb.pdf', {k: i[k] for k in ('bytes', 'size_mm', 'type3_fonts', 'truetype_fonts', 'image_xobjects')})
fig.canvas.draw()
bb_ax = ax.get_position(); bb_cb = cb.ax.get_position(); print('axes right', round(bb_ax.x1, 3), 'cbar left', round(bb_cb.x0, 3), 'overlap:', bb_ax.x1 > bb_cb.x0)
print('colorbar height / axes height', round(bb_cb.height / bb_ax.height, 2), '(shrink=0.6 requested)')
print('colorbar clim', sc.get_clim(), 'gene min/max', gene.min(), gene.max())
# claim: constrained_layout is default in 3.6+ (SKILL.md 'The Three Modern Defaults' #2)
print('rcParams figure.constrained_layout.use default =', mpl.rcParamsDefault['figure.constrained_layout.use'], '(SKILL.md says it is the default in 3.6+)', '| figure.autolayout', mpl.rcParamsDefault['figure.autolayout'])
# claim: tight_layout fails with colorbars
fig, axs = plt.subplots(1, 2, figsize=(4, 2)); im = axs[0].imshow(np.random.rand(5, 5)); axs[0].set_xlabel('long x label here'); c = fig.colorbar(im, ax=axs[0], label='cb')
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always'); fig.tight_layout(); fig.canvas.draw()
r = fig.canvas.get_renderer(); ext = [a.get_tightbbox(r) for a in fig.axes]
print('tight_layout with colorbar: warnings', [str(x.message)[:80] for x in w], '| any tightbbox outside figure?', any(e.x0 < -1 or e.x1 > fig.bbox.width + 1 or e.y0 < -1 for e in ext), '(claim: labels clipped / overlap colorbar)')
# claim: fig.set_constrained_layout(True) after creation
fig = plt.figure()
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always')
    try: fig.set_constrained_layout(True); print('set_constrained_layout(True): ok, warnings', [f'{x.category.__name__}: {str(x.message)[:90]}' for x in w])
    except Exception as e: print('set_constrained_layout ->', type(e).__name__, e)
print('fig.get_layout_engine():', type(fig.get_layout_engine()).__name__)
# claim: fig.set_rasterization_zorder(0) 'globally controls'
fig, ax = plt.subplots(constrained_layout=True); ax.scatter(rng.normal(size=500), rng.normal(size=500), zorder=-1); ax.plot([0, 1], [0, 1], zorder=1)
try:
    fig.set_rasterization_zorder(0)
except AttributeError as e:
    print('fig.set_rasterization_zorder(0) ->', 'AttributeError:', e, '(SKILL.md Failure Modes says to use it)')
ax.set_rasterization_zorder(0); fig.savefig('rz.pdf'); print('ax.set_rasterization_zorder(0) works: images in PDF', pdf_info('rz.pdf')['image_xobjects'])
# claim: default Type-3
plt.rcdefaults(); fig, ax = plt.subplots(); ax.plot([0, 1]); ax.set_xlabel('abc'); fig.savefig('t3.pdf'); print('rcdefaults PDF: type3', pdf_info('t3.pdf')['type3_fonts'], 'truetype', pdf_info('t3.pdf')['truetype_fonts'])
# claim: figsize in inches 89 -> 89 inches
fig = plt.figure(figsize=(89, 70)); print('figsize=(89,70) inches ->', fig.get_size_inches(), 'px at 100 dpi', fig.get_size_inches() * 100)
