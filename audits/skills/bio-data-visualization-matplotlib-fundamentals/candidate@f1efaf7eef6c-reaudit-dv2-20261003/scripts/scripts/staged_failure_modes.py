"""Reproduce every failure-modes.md entry's Trigger/Symptom/Fix on matplotlib 3.11.2. Usage: f2 <outdir>"""
import re, sys, os, warnings
from pathlib import Path
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True); os.chdir(out)
import numpy as np, pandas as pd, matplotlib as mpl, matplotlib.pyplot as plt, seaborn as sns
ok = True


def chk(label, cond):
    global ok
    ok &= bool(cond)
    print(f"[{'PASS' if cond else 'FAIL'}] {label}")


def box(p):
    m = re.search(rb"/MediaBox\s*\[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\]", Path(p).read_bytes())
    a = list(map(float, m.groups()))
    return round((a[2] - a[0]) / 72 * 25.4, 2), round((a[3] - a[1]) / 72 * 25.4, 2)


def clipped(f):
    f.canvas.draw()
    rr = f.canvas.get_renderer()
    fb = f.bbox
    for a in f.axes:
        b = a.get_tightbbox(rr)
        if b.x0 < -1 or b.x1 > fb.x1 + 1 or b.y0 < -1 or b.y1 > fb.y1 + 1:
            return True
    return False


print('matplotlib', mpl.__version__)
# FM1 Type 3 vs 42 (pdffonts run separately)
for ft in (3, 42):
    with mpl.rc_context({'pdf.fonttype': ft, 'ps.fonttype': ft}):
        f, a = plt.subplots()
        a.set_xlabel('abc')
        f.savefig(f'type{ft}.pdf')
        plt.close(f)


# FM2 tight_layout is one-shot; constrained recomputes
def case(eng, resize):
    f, ax = plt.subplots(figsize=(89 / 25.4, 60 / 25.4), layout=None if eng == 'tight_layout()' else eng)
    ax.set_ylabel('y')
    if eng == 'tight_layout()':
        f.tight_layout()
    f.canvas.draw()
    ax.set_ylabel('Mean expression (log2 CPM)\nsecond line')
    ax.set_xlabel('time')
    if resize:
        f.set_size_inches(50 / 25.4, 60 / 25.4)
    r = clipped(f)
    plt.close(f)
    return r


chk("tight_layout() then longer label: clipped", case('tight_layout()', False))
chk("tight_layout() then resize: clipped", case('tight_layout()', True))
chk("layout='constrained' at creation: not clipped after label change or resize", not case('constrained', False) and not case('constrained', True))
f, ax = plt.subplots()
im = ax.imshow(np.zeros((3, 3)))
f.colorbar(im, ax=ax)
try:
    f.set_layout_engine('constrained')
    f.canvas.draw()
    r = None
except ZeroDivisionError as e:
    r = e
chk("set_layout_engine('constrained') after a colorbar exists raises ZeroDivisionError", r is not None)
plt.close(f)
f, ax = plt.subplots(figsize=(89 / 25.4, 60 / 25.4))
f.set_layout_engine('constrained')
im = ax.imshow(np.zeros((3, 3)))
f.colorbar(im, ax=ax, label='long colorbar label')
chk("set_layout_engine('constrained') before the colorbar works, not clipped", not clipped(f))
plt.close(f)
f, (a, b) = plt.subplots(1, 2, figsize=(89 / 25.4, 60 / 25.4))
im = a.imshow(np.zeros((3, 3)))
f.colorbar(im, ax=[a, b])
with warnings.catch_warnings(record=True) as W:
    warnings.simplefilter('always')
    f.tight_layout()
chk("multi-axes colorbar + tight_layout warns 'not compatible with tight_layout'", any('not compatible with tight_layout' in str(w.message) for w in W))
plt.close(f)
f, ax = plt.subplots(figsize=(89 / 25.4, 60 / 25.4))
im = ax.imshow(np.zeros((3, 3)))
f.colorbar(im, ax=ax, label='long colorbar label')
ax.set_ylabel('y')
f.tight_layout()
chk("single colorbar on one axes + tight_layout: not clipped (entry says so)", not clipped(f))
plt.close(f)
# FM3 pyplot state machine
f, axs = plt.subplots(2, 3)
plt.xlabel('X')
chk("plt.xlabel after plt.subplots(2,3) labels the last axes only", axs.flat[-1].get_xlabel() == 'X' and all(a.get_xlabel() == '' for a in axs.flat[:-1]))
plt.close(f)


# FM4 vector size
def sz(ras):
    f, a = plt.subplots(figsize=(89 / 25.4, 70 / 25.4), layout='constrained')
    r = np.random.default_rng(1)
    a.scatter(r.normal(size=100000), r.normal(size=100000), s=4, edgecolors='none', rasterized=ras)
    p = f'n_{ras}.pdf'
    f.savefig(p)
    plt.close(f)
    return os.path.getsize(p)


v, r_ = sz(False), sz(True)
print(f"   vector {v / 1e6:.2f} MB raster {r_ / 1e3:.1f} KB ratio {v / r_:.0f}x")
chk("100000 pts: 1.5 MB vs 24 KB (63x) at default dpi", abs(v / 1e6 - 1.5) < .2 and abs(r_ / 1e3 - 24) < 4)
# FM5 FacetGrid
g = sns.displot(pd.DataFrame({'v': np.arange(20.)}), x='v')
try:
    g.set_xlabel('x')
    r = False
except AttributeError:
    r = True
g.set_axis_labels('x', 'y')
chk("FacetGrid.set_xlabel AttributeError; set_axis_labels works", r and g.axes.flat[0].get_xlabel() == 'x')
f, a = plt.subplots()
sns.histplot(pd.DataFrame({'v': np.arange(20.)}), x='v', ax=a)
a.set_xlabel('x')
chk("axes-level histplot(ax=) + set_xlabel works", a.get_xlabel() == 'x')
plt.close(f)
# FM6 figsize
f = plt.figure(figsize=(89, 70))
chk("figsize=(89,70) is 89 inches wide", f.get_size_inches()[0] == 89)
plt.close(f)
f = plt.figure(figsize=(89 / 25.4, 70 / 25.4))
f.savefig('mm.pdf')
chk("89/25.4 gives 89 mm page", abs(box('mm.pdf')[0] - 89) < .3)
plt.close(f)
# FM7 colorbar
f, a = plt.subplots(layout='constrained')
im = a.imshow(np.zeros((5, 5)))
cb = f.colorbar(im, ax=a)
f.canvas.draw()
h0 = cb.ax.get_position().height
f2, a2 = plt.subplots(layout='constrained')
im2 = a2.imshow(np.zeros((5, 5)))
cb2 = f2.colorbar(im2, ax=a2, shrink=0.6, aspect=20)
f2.canvas.draw()
print('   colorbar height default', round(h0, 3), 'shrink 0.6', round(cb2.ax.get_position().height, 3))
chk("shrink=0.6 aspect=20 gives a shorter colorbar than default", cb2.ax.get_position().height < h0 * 0.8)
plt.close('all')
# FM8 rasterization zorder
f, a = plt.subplots(figsize=(89 / 25.4, 70 / 25.4), layout='constrained')
r = np.random.default_rng(1)
a.scatter(r.normal(size=20000), r.normal(size=20000), s=4, zorder=0)
a.set_xlabel('x label')
a.set_rasterization_zorder(1)
f.savefig('zorder.pdf')
b = Path('zorder.pdf').read_bytes()
chk("ax.set_rasterization_zorder(1): image object, small PDF", len(re.findall(rb"/Subtype\s*/Image", b)) >= 1 and len(b) < 100e3)
chk("Figure has no set_rasterization_zorder", not hasattr(f, 'set_rasterization_zorder'))
plt.close('all')
# Table rows
for lbl, kw in (("none", {}), ("tight", {'bbox_inches': 'tight'})):
    f, a = plt.subplots(figsize=(89 / 25.4, 70 / 25.4), layout='constrained')
    a.scatter([1, 2], [1, 2])
    a.set_xlabel('x')
    f.savefig(f'bb_{lbl}.pdf', **kw)
    plt.close(f)
chk("bbox_inches='tight' page ~92 mm, without it 89 mm", 91 < box('bb_tight.pdf')[0] < 93.5 and abs(box('bb_none.pdf')[0] - 89) < .3)
for ft in ('path', 'none'):
    with mpl.rc_context({'svg.fonttype': ft}):
        f, a = plt.subplots()
        a.set_xlabel('abc')
        f.savefig(f'{ft}.svg')
        plt.close(f)
chk("svg.fonttype none keeps <text>; path (default) does not", b'<text' in Path('none.svg').read_bytes() and b'<text' not in Path('path.svg').read_bytes())
f, a = plt.subplots()
a.spines[['top', 'right']].set_visible(False)
chk("ax.spines[['top','right']].set_visible(False)", not a.spines['top'].get_visible() and not a.spines['right'].get_visible())
plt.close(f)
f, axs = plt.subplots(2, 2, layout='constrained')
chk("plt.subplots(layout='constrained') gives ConstrainedLayoutEngine", type(f.get_layout_engine()).__name__ == 'ConstrainedLayoutEngine')
print('RESULT', 'PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
