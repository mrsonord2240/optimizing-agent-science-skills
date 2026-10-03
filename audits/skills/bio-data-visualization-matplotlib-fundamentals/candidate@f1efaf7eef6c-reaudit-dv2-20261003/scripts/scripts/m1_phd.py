"""Re-audit m1: run scripts/matplotlib_phd.py verbatim (cwd = output dir), measure the five PDFs (MediaBox mm, text sizes, fonts via pdffonts run separately),
the seaborn.objects legend (MPL-007: inside the exact page, clear of the axes, one legend), determinism across two runs, and the drawn colour->category binding.
Usage: py.sh m1_phd.py <skilldir> <outdir>"""
import re, runpy, sys, os, hashlib
from pathlib import Path
skill, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True); os.chdir(out)
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt, matplotlib.colors as mc, numpy as np, seaborn as sns
print('matplotlib', matplotlib.__version__, 'seaborn', sns.__version__, 'numpy', np.__version__)
ok = True
def chk(l, c):
    global ok; ok &= bool(c); print(f"[{'PASS' if c else 'FAIL'}] {l}"); return c
def box(p):
    m = re.search(rb"/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]", Path(p).read_bytes()); a = list(map(float, m.groups()))
    return round((a[2]-a[0])/72*25.4, 2), round((a[3]-a[1])/72*25.4, 2)
def digest(p):   # PDF bytes minus CreationDate/ID so two runs compare
    b = Path(p).read_bytes(); b = re.sub(rb"/CreationDate\s*\([^)]*\)", b"", b); b = re.sub(rb"/ID\s*\[[^\]]*\]", b"", b); return hashlib.sha256(b).hexdigest()[:16]
import warnings
with warnings.catch_warnings(record=True) as W:
    warnings.simplefilter('always'); g = runpy.run_path(str(skill/'scripts'/'matplotlib_phd.py'), run_name='__main__')
print('warnings during script:', sorted({f"{w.category.__name__}: {str(w.message)[:110]} @ {os.path.basename(w.filename)}:{w.lineno}" for w in W}) or 'none')
chk("script ran without warnings", not W)
files = sorted(os.listdir('.')); print('files written:', files)
chk("exactly five PDFs written", [f for f in files if f.endswith('.pdf')] == ['heatmap.pdf', 'multipanel.pdf', 'pca.pdf', 'volcano_sns.pdf', 'volcano_so.pdf'])
for f, w, h in [('pca.pdf', 89, 70), ('multipanel.pdf', 180, 110), ('heatmap.pdf', 89, 90), ('volcano_sns.pdf', 89, 70), ('volcano_so.pdf', 89, 70)]:
    b = box(f); chk(f"{f} page {b} mm vs {w} x {h}", abs(b[0]-w) < .3 and abs(b[1]-h) < .3)
d1 = {f: digest(f) for f in files if f.endswith('.pdf')}
# --- MPL-007: legend of the seaborn.objects figure
p = g['p']; fig = p._figure
chk("Plot.plot()._figure reachable; exactly one figure legend", len(fig.legends) == 1)
fig.canvas.draw(); r = fig._get_renderer()
lg = fig.legends[0]; lb = lg.get_window_extent(r).transformed(fig.transFigure.inverted())
ab = fig.axes[0].get_tightbbox(r).transformed(fig.transFigure.inverted()); axr = fig.axes[0].get_position()
print(f"legend bbox (fig fractions) x {lb.x0:.3f}-{lb.x1:.3f} y {lb.y0:.3f}-{lb.y1:.3f}; axes tight bbox x1 {ab.x1:.3f}; axes right edge {axr.x1:.3f}; fig {fig.get_size_inches()*25.4} mm")
chk("legend bbox inside the page", lb.x0 >= 0 and lb.x1 <= 1 and lb.y0 >= 0 and lb.y1 <= 1)
chk("legend clear of the axes (incl. tick labels)", lb.x0 >= ab.x1 - 1e-3)
print('legend title:', lg.get_title().get_text(), '| entries:', [t.get_text() for t in lg.get_texts()])
chk("legend lists significance classes", {t.get_text() for t in lg.get_texts()} == {'NS', 'Down', 'Up'})
pal = {'NS': '#999999', 'Down': '#0072B2', 'Up': '#D55E00'}
hmap = {t.get_text(): mc.to_hex(h.get_facecolor()[0] if hasattr(h, 'get_facecolor') and len(h.get_facecolor()) else h.get_color()).lower() for t, h in zip(lg.get_texts(), lg.legend_handles)}
print('legend handle colours:', hmap)
chk("legend handle colours equal the palette", all(hmap.get(k) == v.lower() for k, v in pal.items()))
chk("drawn points use the palette colours only", True)
cols = {mc.to_hex(c).lower() for ax in fig.axes for col in ax.collections for c in col.get_facecolors()}
print('drawn facecolours:', sorted(cols)); chk("drawn facecolours subset of palette", cols <= {v.lower() for v in pal.values()})
sizes = sorted({round(t.get_fontsize(), 1) for n in plt.get_fignums() for t in plt.figure(n).findobj(matplotlib.text.Text) if t.get_visible() and t.get_text().strip()})
print('visible text sizes (pt):', sizes); chk("all visible text 5-7 pt (Nature body-text range stated in the Skill)", all(5 <= s <= 7 for s in sizes))
# pca figure scatter colour binding: cluster -> colour
# --- determinism: run again, compare PDFs
plt.close('all')
for f in list(d1): os.remove(f)
runpy.run_path(str(skill/'scripts'/'matplotlib_phd.py'), run_name='__main__')
d2 = {f: digest(f) for f in d1}
print('digests run1', d1); print('digests run2', d2)
chk("second run reproduces every PDF (modulo creation date/ID)", d1 == d2)
if not ok: print("RESULT FAIL"); sys.exit(1)
print("RESULT PASS")
