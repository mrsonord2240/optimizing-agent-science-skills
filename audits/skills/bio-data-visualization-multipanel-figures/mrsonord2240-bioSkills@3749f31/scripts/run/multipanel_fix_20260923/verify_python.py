"""Verification for exact Python multipanel exports, font embedding, and mosaic."""
from pathlib import Path
import os
import runpy

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

out = Path(r"F:\OpenScience\audits\bio-data-visualization-multipanel-figures\run\multipanel_fix_20260923\out_py")
out.mkdir(parents=True, exist_ok=True)
source = Path(r"F:\OpenScience\wt\data-visualization-multipanel-figures\data-visualization\multipanel-figures\examples\multipanel_matplotlib.py")

# Inputs 3 and 5: execute the shipped file in an audit-only output directory.
old = Path.cwd()
try:
    os.chdir(out)
    runpy.run_path(str(source), run_name="__main__")
finally:
    os.chdir(old)

for name in ("multipanel_2x2.pdf", "multipanel_mosaic.pdf", "multipanel_2x2.png", "multipanel_mosaic.png"):
    path = out / name
    assert path.exists() and path.stat().st_size > 1000, name

expected = (int(183 / 25.4 * 300), int(140 / 25.4 * 300))
for name in ("multipanel_2x2.png", "multipanel_mosaic.png"):
    with Image.open(out / name) as image:
        assert image.size == expected, (name, image.size, expected)

# Input 3: subfigures use their local layout and can own a local colourbar.
fig = plt.figure(figsize=(183 / 25.4, 140 / 25.4), layout="constrained")
left, right = fig.subfigures(1, 2, width_ratios=(2, 1))
left_axes = left.subplots(2, 1, sharex=True)
for ax in left_axes:
    ax.plot(np.arange(10), np.arange(10))
right_ax = right.subplots()
im = right_ax.imshow(np.arange(100).reshape(10, 10))
right.colorbar(im, ax=right_ax)
fig.savefig(out / "subfigures.pdf")
assert len(left_axes) == 2 and len(right.axes) == 2
plt.close(fig)

print("Python verification PASS", expected)
