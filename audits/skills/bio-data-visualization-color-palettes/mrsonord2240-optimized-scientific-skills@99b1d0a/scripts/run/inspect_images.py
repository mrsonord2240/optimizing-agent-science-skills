"""Machine-check all audit PNGs after manual visual inspection."""

from pathlib import Path
import sys

import numpy as np
from PIL import Image


if len(sys.argv) != 2:
    raise SystemExit("usage: inspect_images.py <fig-dir>")
fig_dir = Path(sys.argv[1])
files = sorted(fig_dir.glob("*.png"))
assert len(files) >= 9
for path in files:
    with Image.open(path) as image:
        rgb = np.asarray(image.convert("RGB"))
    nonwhite = float(np.mean(np.any(rgb < 250, axis=2)))
    unique = len(np.unique(rgb.reshape(-1, 3), axis=0))
    assert rgb.shape[0] >= 400 and rgb.shape[1] >= 600
    assert nonwhite > 0.01
    assert unique > 100
    print(path.name, "pixels", rgb.shape[1], "x", rgb.shape[0],
          "nonwhite", round(nonwhite, 4), "unique_rgb", unique)
print("PNG INSPECTION CHECKS PASS", len(files))
