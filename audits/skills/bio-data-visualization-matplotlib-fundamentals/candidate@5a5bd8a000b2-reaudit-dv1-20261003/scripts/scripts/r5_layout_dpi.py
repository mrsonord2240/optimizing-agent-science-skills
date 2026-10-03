"""Re-audit 5: (a) failure-modes.md 'fig.set_layout_engine(constrained) after creation' claim; (b) large-N PDF size vs savefig.dpi.
Usage: py.sh r5_layout_dpi.py <outdir>"""
import os
import sys
import warnings
from pathlib import Path
out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
os.chdir(out)
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

print("matplotlib", mpl.__version__)


def build(mode, w_mm, h_mm):
    kw = {'layout': 'constrained'} if mode == 'at_creation' else {}
    f, axs = plt.subplots(1, 2, figsize=(w_mm / 25.4, h_mm / 25.4), **kw)
    if mode == 'engine_before_colorbar':
        f.set_layout_engine('constrained')
    im = axs[1].imshow(np.random.default_rng(0).normal(size=(5, 5)))
    f.colorbar(im, ax=axs[1], label='colorbar label')
    axs[0].set_ylabel('y label')
    axs[1].set_xlabel('x')
    if mode == 'engine_after_colorbar':
        f.set_layout_engine('constrained')
    if mode == 'tight':
        f.tight_layout()
    return f


for mode in ('tight', 'at_creation', 'engine_before_colorbar', 'engine_after_colorbar'):
    for w, h in ((89, 40), (89, 70)):
        f = build(mode, w, h)
        try:
            with warnings.catch_warnings(record=True) as W:
                warnings.simplefilter('always')
                f.canvas.draw()
            r = f.canvas.get_renderer()
            fb = f.bbox
            bxs = [a.get_tightbbox(r) for a in f.axes]
            clipped = any(b.x0 < -1 or b.x1 > fb.x1 + 1 or b.y0 < -1 or b.y1 > fb.y1 + 1 for b in bxs)
            # overlap of the main axes and colorbar axes
            a0, a1 = f.axes[1].get_tightbbox(r), f.axes[2].get_tightbbox(r)
            ov = a0.x1 > a1.x0 + 0.5 and abs(a0.x1 - a1.x1) > 1
            print(f"{mode:24s} {w}x{h} mm: drew OK; clipped={clipped}; warnings={[str(x.message)[:50] for x in W]}")
            f.savefig(f"{mode}_{w}x{h}.png", dpi=150)
        except Exception as e:
            print(f"{mode:24s} {w}x{h} mm: EXCEPTION {type(e).__name__}: {e}")
        plt.close(f)

# (b) large-N size with default raster dpi (figure=100) and with the Skill's savefig.dpi=300
for dpi in ('figure', 300):
    for ras in (False, True):
        with mpl.rc_context({'savefig.dpi': dpi, 'pdf.fonttype': 42}):
            f, a = plt.subplots(figsize=(89 / 25.4, 70 / 25.4), layout='constrained')
            r = np.random.default_rng(0)
            a.scatter(r.normal(size=100000), r.normal(size=100000), s=4, edgecolors='none', rasterized=ras)
            a.set_xlabel('x')
            p = f'n100k_dpi{dpi}_{"ras" if ras else "vec"}.pdf'
            f.savefig(p)
            plt.close(f)
            print(f"savefig.dpi={dpi!s:6s} rasterized={ras!s:5s}: {os.path.getsize(p) / 1e3:.0f} KB")
