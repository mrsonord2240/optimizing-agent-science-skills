"""Re-audit m5: SKILL.md / usage-guide / recipe claims not covered by the staged failure-mode script: layout defaults, boxplot labels rename, rasterization inside the
shipped example PDFs (seaborn pass-through), EPS Type 42, panel tags inside the page, text and spines. Usage: py.sh m5_claims.py <phd-outdir (PDFs from m1)> <outdir>"""
import re, sys, os, warnings, zlib
from pathlib import Path
phd, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True); os.chdir(out)
import matplotlib as mpl; mpl.use("Agg")
import matplotlib.pyplot as plt, numpy as np
print('matplotlib', mpl.__version__)
ok = True
def chk(l, c):
    global ok; ok &= bool(c); print(f"[{'PASS' if c else 'FAIL'}] {l}"); return c
# layout claims
f, a = plt.subplots(); chk("default layout engine is None (opt-in claim)", f.get_layout_engine() is None); plt.close(f)
with warnings.catch_warnings(record=True) as W:
    warnings.simplefilter('always'); f, a = plt.subplots(constrained_layout=True)
print('constrained_layout=True ->', type(f.get_layout_engine()).__name__, '| warnings:', [str(w.message)[:80] for w in W]); chk("legacy constrained_layout=True still works and gives the same engine", type(f.get_layout_engine()).__name__ == 'ConstrainedLayoutEngine'); plt.close(f)
# boxplot labels rename
f, a = plt.subplots()
try:
    a.boxplot([[1, 2, 3], [2, 3, 4]], labels=['A', 'B']); r = 'accepted'
except Exception as e:
    r = f"{type(e).__name__}: {str(e)[:70]}"
print('boxplot(labels=) ->', r); chk("boxplot(labels=) is rejected on 3.11 (claim in SKILL.md and chart-recipes.md)", r.startswith('TypeError'))
a.cla(); a.boxplot([[1, 2, 3], [2, 3, 4]], tick_labels=['A', 'B']); chk("boxplot(tick_labels=) works", [t.get_text() for t in a.get_xticklabels()] == ['A', 'B']); plt.close(f)
# rasterization inside the shipped example PDFs: image XObjects present, text still fonts
for name in ['pca.pdf', 'volcano_sns.pdf', 'volcano_so.pdf', 'multipanel.pdf', 'heatmap.pdf']:
    b = (phd/name).read_bytes(); n_img = len(re.findall(rb"/Subtype\s*/Image", b)); n_font = len(re.findall(rb"/Type\s*/Font\b", b))
    print(f"{name:18s} {len(b)/1e3:7.1f} KB | image XObjects {n_img} | font objects {n_font}")
    if name in ('pca.pdf', 'volcano_sns.pdf', 'multipanel.pdf', 'heatmap.pdf'): chk(f"{name}: raster image present (rasterized=True took effect) and fonts embedded", n_img >= 1 and n_font >= 1)
so = (phd/'volcano_so.pdf').read_bytes(); print('volcano_so.pdf images', len(re.findall(rb"/Subtype\s*/Image", so)), '(so.Dots is vector by design, 500 points)')
import seaborn as sns, pandas as pd
rng = np.random.default_rng(0); d = pd.DataFrame({'x': rng.normal(size=20000), 'y': rng.normal(size=20000), 'h': rng.choice(['a', 'b'], 20000)})
sz = {}
for ras in (False, True):
    f, a = plt.subplots(figsize=(89 / 25.4, 70 / 25.4), layout='constrained'); sns.scatterplot(data=d, x='x', y='y', hue='h', s=8, alpha=.7, ax=a, rasterized=ras); f.savefig(f'sns_{ras}.pdf'); plt.close(f)
    b = Path(f'sns_{ras}.pdf').read_bytes(); sz[ras] = (len(b), len(re.findall(rb"/Subtype\s*/Image", b)))
print('seaborn.scatterplot 20000 pts, rasterized False/True -> (bytes, images):', sz)
chk("seaborn passes rasterized=True through: images appear and the PDF shrinks", sz[True][1] >= 1 and sz[False][1] == 0 and sz[True][0] < sz[False][0] / 2)
# EPS Type 42
f, a = plt.subplots(figsize=(89 / 25.4, 70 / 25.4)); a.set_xlabel('abc'); a.set_title('title')
with mpl.rc_context({'ps.fonttype': 42, 'font.family': 'sans-serif', 'font.sans-serif': ['Arial', 'DejaVu Sans']}): f.savefig('t42.eps')
with mpl.rc_context({'ps.fonttype': 3}): f.savefig('t3.eps')
e42, e3 = Path('t42.eps').read_bytes(), Path('t3.eps').read_bytes()
print('EPS fonttype 42 has Type42 resource:', b'Type42' in e42 or b'FontType 42' in e42 or b'/FontType 42' in e42, '| fonttype 3 has "FontType 3":', b'FontType 3' in e3)
chk("ps.fonttype=42 changes EPS font embedding vs 3", e42 != e3 and (b'42' in e42))
plt.close(f)
# panel tags stay inside the page in the 2x3 grid (text positions)
import runpy
plt.close('all')
os.makedirs('mp', exist_ok=True); os.chdir('mp')
import contextlib, io
SK = Path(sys.argv[3]) if len(sys.argv) > 3 else None
if SK:
    g = runpy.run_path(str(SK/'scripts'/'matplotlib_phd.py'), run_name='__main__')
    figs = [plt.figure(n) for n in plt.get_fignums()]
    grid = [fg for fg in figs if len(fg.axes) == 6]
    chk("2x3 grid figure present", len(grid) == 1)
    fg = grid[0]; fg.canvas.draw(); r = fg._get_renderer(); fb = fg.bbox
    tags = [t for ax in fg.axes for t in ax.texts]
    bad = [t.get_text() for t in tags if not (t.get_window_extent(r).x0 >= fb.x0 - 1 and t.get_window_extent(r).x1 <= fb.x1 + 1 and t.get_window_extent(r).y1 <= fb.y1 + 1)]
    print('panel tags', [t.get_text() for t in tags], 'outside page:', bad); chk("every panel tag lies inside the page", not bad)
    ov = []
    for ax in fg.axes:
        tb = ax.get_tightbbox(r);
        for ax2 in fg.axes:
            if ax2 is not ax and tb.overlaps(ax2.get_window_extent(r)) and tb.x1 > ax2.get_window_extent(r).x0 + 1: ov.append((ax, ax2))
    chk("no axes tight box overlaps another axes (constrained layout)", not ov)
print("RESULT", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
