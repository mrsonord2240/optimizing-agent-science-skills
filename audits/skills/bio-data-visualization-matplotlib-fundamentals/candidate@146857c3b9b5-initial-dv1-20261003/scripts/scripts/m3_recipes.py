"""MPL audit run 3: references/chart-recipes.md and failure-modes.md claims, SKILL.md Saving block, executed.
Usage: py.sh m3_recipes.py <outdir>   (PDFs are then inspected with scripts/pdffonts.sh)"""
import datetime, os, re, sys, warnings
from pathlib import Path
import matplotlib as mpl
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.ticker import ScalarFormatter
from PIL import Image

out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True); os.chdir(out)
print("matplotlib", mpl.__version__, "seaborn", sns.__version__)


def chk(label, cond):
    print(f"[{'PASS' if cond else 'FAIL'}] {label}")


rng = np.random.default_rng(0)
x = rng.normal(size=3000); y = 0.5 * x + rng.normal(size=3000)
mpl.rcParams.update({'pdf.fonttype': 42, 'ps.fonttype': 42, 'font.family': 'sans-serif', 'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
                     'font.size': 7, 'axes.labelsize': 7, 'axes.titlesize': 8, 'xtick.labelsize': 6, 'ytick.labelsize': 6, 'legend.fontsize': 6,
                     'figure.dpi': 100, 'savefig.dpi': 300, 'savefig.bbox': 'tight', 'savefig.pad_inches': 0.05,
                     'axes.linewidth': 0.5, 'xtick.major.width': 0.5, 'ytick.major.width': 0.5, 'lines.linewidth': 1.0, 'patch.linewidth': 0.5})
# SKILL 'Standard Setup' rcParams verbatim above (incl. pad_inches 0.05). 89 x 70 mm single-axes figure, Saving block formats
fig, ax = plt.subplots(figsize=(89 / 25.4, 70 / 25.4), layout='constrained')
ax.scatter(x, y, c='#0072B2', s=10, alpha=0.7, edgecolors='none', rasterized=True)
ax.set_xlabel('PC1 (45%)'); ax.set_ylabel('PC2 (12%)'); ax.spines[['top', 'right']].set_visible(False)
for f in ('scatter.pdf', 'figure.png', 'figure.svg', 'figure.eps'):
    with warnings.catch_warnings(record=True) as W:
        warnings.simplefilter('always')
        fig.savefig(f)
    print(f, os.path.getsize(f), 'B', ('| warnings: ' + '; '.join(sorted({str(w.message)[:110] for w in W}))) if W else '')
fig.savefig('figure.tiff', dpi=300, pil_kwargs={'compression': 'tiff_lzw'})
t = Image.open('figure.tiff'); print('tiff', t.size, t.info.get('compression'))
w_px, h_px = Image.open('figure.png').size
print(f"figure.png {w_px} x {h_px} px = {w_px / 300 * 25.4:.1f} x {h_px / 300 * 25.4:.1f} mm (documented 89 x 70 mm; bbox tight + pad 0.05 in)")
chk("Standard Setup rcParams + 89 mm figure save to an 89 mm wide file (within 1 mm)", abs(w_px / 300 * 25.4 - 89) <= 1)
svg = Path('figure.svg').read_text(encoding='utf-8')
n_text = len(re.findall(r'<text[ >]', svg)); print("svg <text> elements:", n_text, "| glyph <path>/<use> in defs:", len(re.findall(r'<use ', svg)), "| svg.fonttype default:", 'none' if n_text else 'path')
chk("SVG save keeps axis text as editable <text> ('SVG for editable vector')", n_text > 0)
# default Type 3
# Type 3 default claim: see m3b_type3_probe.py (stock rcParams -> Type 3; pdf.fonttype=42 -> TrueType)
plt.close(fig)
# --- chart-recipes.md blocks verbatim
fig, axes = plt.subplots(2, 3, figsize=(180 / 25.4, 100 / 25.4), layout='constrained')
a = axes.flat; values = y; categories = ['A', 'B', 'C']
a[0].scatter(x, y, c=values, cmap='viridis', s=8, alpha=0.6, edgecolors='none', rasterized=True)
plt.colorbar(a[0].collections[0], ax=a[0], label='Expression', shrink=0.8)
xs = np.arange(50); y1 = np.sin(xs / 8); y2 = np.cos(xs / 8); y_low, y_high = y1 - .2, y1 + .2
a[1].plot(xs, y1, color='#0072B2', label='Control', linewidth=1); a[1].plot(xs, y2, color='#D55E00', label='Treatment', linewidth=1)
a[1].fill_between(xs, y_low, y_high, color='#0072B2', alpha=0.2); a[1].legend(frameon=False, fontsize=6)
a[2].bar(categories, [3, 5, 2], color='#0072B2', edgecolor='black', linewidth=0.5)
ga, gb, gc = (rng.normal(i, 1, 40) for i in range(3))
a[3].boxplot([ga, gb, gc], tick_labels=['A', 'B', 'C'], patch_artist=True, boxprops=dict(facecolor='#0072B2', alpha=0.7))
a[4].hist(x, bins=30, color='#0072B2', edgecolor='white', linewidth=0.5)
matrix = rng.normal(size=(20, 15)); vmax = np.quantile(np.abs(matrix), .99)
im = a[5].imshow(matrix, cmap='RdBu_r', aspect='auto', vmin=-vmax, vmax=vmax); plt.colorbar(im, ax=a[5], label='Z-score')
a[4].set_yscale('log'); a[2].xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
a[2].set_xticks(np.arange(0, 3, 1)); a[2].set_xticklabels(['A', 'B', 'C'], rotation=45, ha='right'); a[4].grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
fig.savefig('recipes.pdf'); fig.savefig('recipes.png')
bp = a[3].patches[0].get_facecolor(); print("boxplot median of group A line y =", round(float(np.median(ga)), 3), "(drawn via patch_artist; box facecolour alpha", round(bp[3], 2), ")")
chk("Recipes build: scatter+colorbar, line+fill, bar, boxplot(tick_labels=), hist(log), imshow RdBu_r symmetric", True)
fig2, ax2 = plt.subplots(figsize=(89 / 25.4, 70 / 25.4), layout='constrained')
dates = [datetime.date(2024, 1, 1) + datetime.timedelta(days=30 * i) for i in range(12)]
ax2.plot(dates, np.arange(12)); ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m')); fig2.savefig('dates.png')
# boxplot labels= rejected on 3.11 (documented claim)
try:
    with warnings.catch_warnings():
        warnings.simplefilter('error'); plt.subplots()[1].boxplot([ga], labels=['A'])
    print("boxplot(labels=) accepted")
except Exception as e:
    print("boxplot(labels=) ->", type(e).__name__, str(e)[:90])
# --- failure-modes claims
g = sns.displot(x=x[:200], col=np.repeat(['p', 'q'], 100))
try:
    g.set_xlabel('x'); print("FacetGrid.set_xlabel accepted")
except AttributeError as e:
    print("FacetGrid.set_xlabel ->", "AttributeError", str(e)[:60])
g.set_axis_labels('x', 'n')
# tight_layout vs constrained with colorbar+shared axes: does any label fall outside the figure canvas?
def clipped(layout):
    fg = plt.figure(figsize=(89 / 25.4, 70 / 25.4), **({'layout': 'constrained'} if layout == 'constrained' else {})); axs = fg.subplots(2, 2, sharex=True)
    for k, axx in enumerate(axs.flat):
        im = axx.imshow(rng.normal(size=(5, 5)), aspect='auto'); axx.set_ylabel('Gene symbol long label'); axx.set_xlabel('Sample label')
    fg.colorbar(im, ax=axs.ravel().tolist(), label='Z-score')
    if layout == 'tight':
        fg.tight_layout()
    fg.canvas.draw(); r = fg.canvas.get_renderer(); W, H = fg.get_size_inches() * fg.dpi
    bad = 0
    for axx in axs.flat:
        for art in (axx.xaxis.label, axx.yaxis.label):
            bb = art.get_window_extent(r)
            bad += bb.x0 < -1 or bb.y0 < -1 or bb.x1 > W + 1 or bb.y1 > H + 1
    ov = 0
    cbax = [c for c in fg.axes if c not in axs.flat][0]
    for axx in axs.flat:
        b1, b2 = axx.get_tightbbox(r), cbax.get_tightbbox(r); ov += b1.overlaps(b2)
    plt.close(fg); return bad, ov
print("tight_layout  (clipped labels, axes/colorbar overlaps):", clipped('tight'))
print("constrained   (clipped labels, axes/colorbar overlaps):", clipped('constrained'))
# rasterization zorder claim (failure-modes.md: `fig.set_rasterization_zorder(0)`)
fz, az = plt.subplots(figsize=(3, 2)); az.scatter(x[:2000], y[:2000], s=3, zorder=-1)
print("Figure has set_rasterization_zorder:", hasattr(fz, 'set_rasterization_zorder'), "| Axes has set_rasterization_zorder:", hasattr(az, 'set_rasterization_zorder'))
chk("failure-modes.md `fig.set_rasterization_zorder(0)` exists on Figure", hasattr(fz, 'set_rasterization_zorder'))
az.set_rasterization_zorder(0); fz.savefig('zorder.pdf')
raw = Path('zorder.pdf').read_bytes(); print("ax.set_rasterization_zorder(0): image XObjects", len(re.findall(rb'/Subtype\s*/Image', raw)))
# EPS of the 6-panel recipes figure (alpha scatter, fill_between alpha, boxplot alpha): does the PostScript backend warn?
with warnings.catch_warnings(record=True) as W:
    warnings.simplefilter('always'); fig.savefig('recipes.eps')
print("recipes.eps warnings:", sorted({str(w.message)[:120] for w in W}) or "none")
# Lead check: EPS + transparency. SKILL.md has no EPS save recipe (only ps.fonttype); test the plain alpha case separately.
fe, ae = plt.subplots(figsize=(3, 2)); ae.scatter(x[:200], y[:200], alpha=0.5)
with warnings.catch_warnings(record=True) as W:
    warnings.simplefilter('always'); fe.savefig('alpha_plain.eps')
print("non-rasterized alpha scatter -> .eps warnings:", sorted({str(w.message)[:130] for w in W}) or "none")
