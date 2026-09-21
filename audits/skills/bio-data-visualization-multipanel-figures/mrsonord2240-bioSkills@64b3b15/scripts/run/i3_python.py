"""Input 3: SKILL.md matplotlib GridSpec + subfigures blocks (run as written on synthetic data) with content assertions."""
import numpy as np, matplotlib, matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
OUT = r'F:\OpenScience\audits\bio-data-visualization-multipanel-figures\out'
print('matplotlib', matplotlib.__version__)
def chk(label, cond, note=''):
    print(f"[{'PASS' if cond else 'FAIL'}] {label} {note}"); return cond
rng = np.random.default_rng(7)
x = rng.normal(size=300); y = 0.7 * x + rng.normal(scale=.6, size=300)
cats = ['A', 'B', 'C', 'D']; vals = [3, 5, 2, 4]
matrix = rng.normal(size=(20, 20))

print('rcParams pdf.fonttype default =', matplotlib.rcParams['pdf.fonttype'], '; figure.constrained_layout.use default =', matplotlib.rcParams['figure.constrained_layout.use'], '; figure.autolayout =', matplotlib.rcParams['figure.autolayout'])
f0 = plt.figure(); print('default fig layout engine:', f0.get_layout_engine()); plt.close(f0)

# ---------------- block: GridSpec (verbatim) ----------------
fig = plt.figure(figsize=(180/25.4, 120/25.4), constrained_layout=True)
gs = GridSpec(2, 3, figure=fig)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1:])         # top right, spans columns 1-2
ax3 = fig.add_subplot(gs[1, :])           # bottom row, spans all columns
ax1.scatter(x, y, s=4, rasterized=True)
ax2.plot(x[:50], y[:50])
ax3.bar(cats, vals)
ax1.set_title('SCATTER'); ax2.set_title('LINE'); ax3.set_title('BAR')
labels = []
for ax, lbl in zip([ax1, ax2, ax3], 'abc'):
    t = ax.text(-0.15, 1.05, lbl, transform=ax.transAxes, fontsize=10, fontweight='bold', va='top')
    labels.append(t)
fig.savefig(OUT + r'\i3_gridspec.pdf', dpi=300, bbox_inches='tight')
fig.savefig(OUT + r'\i3_gridspec.png', dpi=300, bbox_inches='tight')

# geometry assertions (before tight bbox; figure objects)
fig.canvas.draw(); r = fig.canvas.get_renderer()
b1, b2, b3 = [a.get_position() for a in (ax1, ax2, ax3)]
chk('GridSpec 3 axes created', len(fig.axes) == 3)
chk('ax2 sits right of ax1 and shares its right edge with ax3 (spans cols 1-2)', b2.x0 > b1.x1 and abs(b2.x1 - b3.x1) < 1e-6, f'ax2/ax1 width={b2.width/b1.width:.2f}')
chk('ax3 spans all columns (right edge == ax2 right edge, left == ax1 left)', abs(b3.x1 - b2.x1) < 1e-6 and abs(b3.x0 - b1.x0) < 1e-6)
chk('panel labels attached to their own axes and lowercase a,b,c', [t.get_text() for t in labels] == list('abc') and all(t.get_transform() == a.transAxes for t, a in zip(labels, (ax1, ax2, ax3))))
# label overlap check: label bbox vs its own y-axis tick labels and vs neighbouring axes (tight bboxes)
def overlap(a, b): return not (a.x1 <= b.x0 or b.x1 <= a.x0 or a.y1 <= b.y0 or b.y1 <= a.y0)
for t, ax, nm in zip(labels, (ax1, ax2, ax3), ('a', 'b', 'c')):
    tb = t.get_window_extent(r)
    ticks = [l.get_window_extent(r) for l in ax.get_yticklabels() if l.get_text()]
    hit_ticks = sum(overlap(tb, k) for k in ticks)
    others = [o for o in (ax1, ax2, ax3) if o is not ax]
    hit_other = sum(overlap(tb, o.get_tightbbox(r)) for o in others)
    inside_fig = tb.x0 >= 0 and tb.y1 <= fig.bbox.y1 + 0.5
    print(f'   label {nm}: overlaps own y tick labels={hit_ticks}, overlaps other axes={hit_other}, inside figure canvas={inside_fig} (x0={tb.x0:.1f}px)')
plt.close(fig)

# measure saved sizes
from PIL import Image
im = Image.open(OUT + r'\i3_gridspec.png'); print('PNG px', im.size, ' expected 180x120 mm @300dpi ->', round(180/25.4*300), round(120/25.4*300))
chk('saved PNG is 180 x 120 mm at 300 dpi (+-1%) despite bbox_inches=tight', abs(im.size[0] - 2126) / 2126 < .01 and abs(im.size[1] - 1417) / 1417 < .01, f'actual {im.size[0]/300*25.4:.1f} x {im.size[1]/300*25.4:.1f} mm')

# ---------------- block: subfigures (verbatim) ----------------
fig = plt.figure(figsize=(180/25.4, 120/25.4), constrained_layout=True)
subfigs = fig.subfigures(1, 2, width_ratios=[2, 1])
axs_left = subfigs[0].subplots(2, 1)
axs_left[0].plot(x[:50], y[:50])
axs_left[1].scatter(x, y, rasterized=True)
ax_right = subfigs[1].subplots(1, 1)
ax_right.imshow(matrix)
subfigs[1].colorbar(ax_right.images[0], ax=ax_right, shrink=0.5)
for a, l in zip([axs_left[0], axs_left[1], ax_right], 'abc'):
    a.set_title(l.upper() + '-panel')
fig.savefig(OUT + r'\i3_subfig.png', dpi=200)
fig.savefig(OUT + r'\i3_subfig.pdf')
fig.canvas.draw()
wl = subfigs[0].bbox.width; wr = subfigs[1].bbox.width
chk('subfigures width ratio 2:1', abs(wl / wr - 2) < 0.02, f'ratio={wl/wr:.3f}')
chk('left subfigure has 2 stacked axes, right has image axes + colorbar axes', len(axs_left) == 2 and len(subfigs[1].axes) == 2, f'right axes={len(subfigs[1].axes)}')
chk('left axes stacked (ax0 above ax1)', axs_left[0].get_position().y0 > axs_left[1].get_position().y1 - 1e-6)
plt.close(fig)

# ---------------- Nature single column 89 mm ----------------
fig = plt.figure(figsize=(89/25.4, 60/25.4), constrained_layout=True)
gs = GridSpec(1, 2, figure=fig)
for i, l in enumerate('ab'):
    a = fig.add_subplot(gs[0, i]); a.scatter(x, y, s=4, rasterized=True); a.text(-0.15, 1.05, l, transform=a.transAxes, fontsize=10, fontweight='bold', va='top')
fig.savefig(OUT + r'\i3_single89.pdf', dpi=300, bbox_inches='tight'); fig.savefig(OUT + r'\i3_single89.png', dpi=300, bbox_inches='tight')
im = Image.open(OUT + r'\i3_single89.png'); print('89 mm block PNG mm =', round(im.size[0]/300*25.4, 1), 'x', round(im.size[1]/300*25.4, 1))
chk('single-column 89 mm figure saved at exactly 89 mm wide (+-1 mm)', abs(im.size[0]/300*25.4 - 89) <= 1)
plt.close(fig)

# ---------------- pdf.fonttype=42 applied? (setting from the usage guide / description) ----------------
matplotlib.rcParams['pdf.fonttype'] = 42
fig, ax = plt.subplots(figsize=(89/25.4, 60/25.4), constrained_layout=True); ax.plot(x[:20], y[:20]); ax.set_title('Type42 test')
fig.savefig(OUT + r'\i3_fonttype42.pdf'); plt.close(fig)
matplotlib.rcParams['pdf.fonttype'] = 3
fig, ax = plt.subplots(figsize=(89/25.4, 60/25.4), constrained_layout=True); ax.plot(x[:20], y[:20]); ax.set_title('Type3 default')
fig.savefig(OUT + r'\i3_fonttype3.pdf'); plt.close(fig)
