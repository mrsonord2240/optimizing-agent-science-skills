"""Re-audit 4: execute references/chart-recipes.md blocks verbatim; test each failure-modes.md claim on matplotlib 3.11.2.
Usage: py.sh r4_recipes_failures.py <skilldir> <outdir>"""
import re, sys, os, warnings
from pathlib import Path
skill, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True); os.chdir(out)
import numpy as np, pandas as pd, matplotlib as mpl, matplotlib.pyplot as plt, seaborn as sns
ok = True


def chk(label, cond):
    global ok
    ok &= bool(cond)
    print(f"[{'PASS' if cond else 'FAIL'}] {label}")
    return cond


def box(p):
    m = re.search(rb"/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]", Path(p).read_bytes())
    a = list(map(float, m.groups()))
    return round((a[2] - a[0]) / 72 * 25.4, 2), round((a[3] - a[1]) / 72 * 25.4, 2)


print("matplotlib", mpl.__version__, "seaborn", sns.__version__)
mpl.rcParams.update({'pdf.fonttype': 42, 'font.size': 7, 'savefig.dpi': 300})
rng = np.random.default_rng(0)

# 1. chart-recipes.md: run every fragment verbatim, each on its own axes of one 2x3 figure
rec = (skill / 'references' / 'chart-recipes.md').read_text(encoding='utf-8')
blocks = re.findall(r"```python\n(.*?)```", rec, re.S)
print(len(blocks), "recipe blocks")
src = "\n".join(blocks)
parts = re.split(r"\n(?=# (?:Scatter|Line|Bar|Box|Histogram|Heatmap|Log scale|Scientific|Date axis|Tick frequency|Grid))", src)
parts = [p for p in parts if p.strip()]
print(len(parts), "recipe snippets:", [p.splitlines()[0][:28] for p in parts])
x = np.linspace(0, 10, 50)
matrix = rng.normal(size=(20, 8))
ns = {'np': np, 'x': x, 'y': rng.normal(size=50), 'values': rng.normal(size=50), 'y1': np.sin(x), 'y2': np.cos(x),
      'y_low': np.sin(x) - .3, 'y_high': np.sin(x) + .3, 'categories': list('ABC'),
      'group_a': rng.normal(size=30), 'group_b': rng.normal(1, 1, 30), 'group_c': rng.normal(2, 1, 30),
      'matrix': matrix, 'vmax': np.quantile(np.abs(matrix), .99)}
fig, axes = plt.subplots(2, 3, figsize=(180 / 25.4, 110 / 25.4), layout='constrained')
k = 0
for p in parts:
    head = p.splitlines()[0]
    if head.startswith('# Scatter'):
        ns['x'], ns['y'], ns['values'] = rng.normal(size=50), rng.normal(size=50), rng.normal(size=50)
    elif head.startswith('# Line'):
        ns['x'] = x
    elif head.startswith('# Bar'):
        ns['values'] = [3, 5, 2]
    elif head.startswith('# Histogram'):
        ns['values'] = rng.normal(size=500)
    elif head.startswith('# Tick frequency'):
        ns['x'] = x
    ax = axes.flat[min(k, 5)]
    ns.update({'ax': ax, 'fig': fig})
    try:
        with warnings.catch_warnings(record=True) as W:
            warnings.simplefilter('always')
            exec(compile(p, 'chart-recipes.md', 'exec'), ns)
        chk(f"snippet '{head[:30]}' ran without warnings; warnings={[str(w.message)[:60] for w in W]}", not W)
    except Exception as e:
        chk(f"snippet '{head[:30]}' ran", False)
        print("    ", type(e).__name__, e)
    if head.startswith(('# Scatter', '# Line', '# Bar', '# Box', '# Histogram', '# Heatmap')):
        k += 1
fig.savefig('recipes.pdf')
chk(f"recipes.pdf page {box('recipes.pdf')} == 180 x 110 mm", abs(box('recipes.pdf')[0] - 180) <= .3 and abs(box('recipes.pdf')[1] - 110) <= .3)
try:
    plt.subplots()[1].boxplot([[1, 2, 3]], labels=['a'])
    r = False
except Exception as e:
    r = True
    print("   labels= ->", type(e).__name__, str(e)[:70])
chk("boxplot(labels=) raises on 3.11.2 as the recipe note says", r)


# 2. Large-N claim
def pdf_size(n, ras):
    f, a = plt.subplots(figsize=(89 / 25.4, 70 / 25.4), layout='constrained')
    r = np.random.default_rng(1)
    a.scatter(r.normal(size=n), r.normal(size=n), s=4, alpha=.6, edgecolors='none', rasterized=ras)
    p = f'n{n}_{"ras" if ras else "vec"}.pdf'
    f.savefig(p)
    plt.close(f)
    return os.path.getsize(p)


v, r_ = pdf_size(100000, False), pdf_size(100000, True)
print(f"100k points: vector {v / 1e6:.2f} MB, rasterised {r_ / 1e3:.1f} KB, ratio {v / r_:.0f}x")
print("(note: this block sets savefig.dpi=300 and alpha=.6; r5 reproduces 24 KB at default dpi without alpha)")
chk("claim '100000 points = 1.5 MB vector vs 24 KB raster (63x)' reproduced under THIS block's settings (dpi 300, alpha .6)", abs(v / 1e6 - 1.5) < .3 and abs(r_ / 1e3 - 24) < 5)

# 3. set_rasterization_zorder
f, a = plt.subplots(figsize=(89 / 25.4, 70 / 25.4), layout='constrained')
r = np.random.default_rng(1)
a.scatter(r.normal(size=20000), r.normal(size=20000), s=4, zorder=0)
a.set_xlabel('x label')
a.set_rasterization_zorder(1)
f.savefig('zorder.pdf')
b = Path('zorder.pdf').read_bytes()
ni = len(re.findall(rb"/Subtype\s*/Image", b))
print("zorder.pdf bytes", len(b), "image objects:", ni)
chk("ax.set_rasterization_zorder(1) rasterises zorder<1 artists (>=1 image, small pdf)", ni >= 1 and len(b) < 100e3)
f2, a2 = plt.subplots()
a2.scatter([1, 2], [1, 2], zorder=0)
f2.savefig('nozorder.pdf')
chk("control: no set_rasterization_zorder -> no image object", len(re.findall(rb"/Subtype\s*/Image", Path('nozorder.pdf').read_bytes())) == 0)
chk("fig.set_rasterization_zorder does not exist", not hasattr(f, 'set_rasterization_zorder'))


# 4. tight_layout vs constrained with colorbar
def clipped(engine):
    f, axs = plt.subplots(1, 2, figsize=(89 / 25.4, 40 / 25.4))
    im = axs[1].imshow(np.random.default_rng(0).normal(size=(5, 5)))
    f.colorbar(im, ax=axs[1], label='A long colorbar label')
    axs[0].set_ylabel('A fairly long y label')
    axs[1].set_xlabel('x')
    with warnings.catch_warnings(record=True) as W:
        warnings.simplefilter('always')
        if engine == 'tight':
            f.tight_layout()
        else:
            f.set_layout_engine('constrained')
        f.canvas.draw()
    rr = f.canvas.get_renderer()
    fb = f.bbox
    bxs = [aa.get_tightbbox(rr) for aa in f.axes]
    return any(bb.x0 < -1 or bb.x1 > fb.x1 + 1 or bb.y0 < -1 or bb.y1 > fb.y1 + 1 for bb in bxs), [str(w.message)[:80] for w in W]


print("tight_layout + colorbar -> clipped, warnings:", clipped('tight'))
try:
    res_after = clipped('constrained')
except Exception as e:
    res_after = f"{type(e).__name__}: {e}"
print("set_layout_engine('constrained') after the colorbar exists ->", res_after)
chk("failure-modes.md 'or fig.set_layout_engine(constrained) after creation' works with a colorbar present (r6 isolates it)", isinstance(res_after, tuple) and res_after[0] is False)

# 5. FacetGrid
g = sns.displot(pd.DataFrame({'v': rng.normal(size=50)}), x='v')
try:
    g.set_xlabel('x')
    r = False
except AttributeError as e:
    r = True
    print("   ", e)
chk("FacetGrid.set_xlabel raises AttributeError", r)
g.set_axis_labels('x', 'y')
chk("FacetGrid.set_axis_labels works", g.axes.flat[0].get_xlabel() == 'x')

# 6. bbox_inches='tight' page size
for lbl, kw in (("no bbox", {}), ("bbox_inches='tight'", {'bbox_inches': 'tight'})):
    f, a = plt.subplots(figsize=(89 / 25.4, 70 / 25.4), layout='constrained')
    a.scatter([1, 2], [1, 2])
    a.set_xlabel('x')
    f.savefig(f'bb_{len(kw)}.pdf', **kw)
    print(lbl, box(f'bb_{len(kw)}.pdf'))
chk("bbox tight gives ~92 mm (claim '~92 mm')", 91 < box('bb_1.pdf')[0] < 93.5)
chk("without it exactly 89", abs(box('bb_0.pdf')[0] - 89) < .3)

# 7. fonttype 3 vs 42 controls (pdffonts is run separately in WSL)
with mpl.rc_context({'pdf.fonttype': 3}):
    f, a = plt.subplots()
    a.set_xlabel('abc')
    f.savefig('type3.pdf')
with mpl.rc_context({'pdf.fonttype': 42}):
    f, a = plt.subplots()
    a.set_xlabel('abc')
    f.savefig('type42.pdf')
print("RESULT", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
