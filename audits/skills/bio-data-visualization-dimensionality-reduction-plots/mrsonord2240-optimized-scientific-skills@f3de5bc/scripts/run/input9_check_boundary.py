"""Check the minimum-shape run and categorical color distinctness in the fixed example."""
from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(r"F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots\run\boundary")
expected = ["pca.pdf", "scree.pdf", "umap_clusters.pdf", "tsne.pdf", "phate.pdf"]
for name in expected:
    path = ROOT / "figures" / name
    print(f"{name}: {path.stat().st_size if path.is_file() else 0} bytes")
    assert path.is_file() and path.stat().st_size > 5_000

colors = plt.colormaps["tab10"](np.arange(12))[:, :3]
unique = np.unique(np.round(colors, 8), axis=0)
print(f"condition categories=12; PCA recipe colors distinct={len(unique)}")
print(f"categories 10 and 11 equal last tab10 color={np.allclose(colors[10], colors[9]) and np.allclose(colors[11], colors[9])}")
assert len(unique) == 10
stdout = (ROOT / "boundary_stdout.txt").read_text(encoding="utf-8")
print(f"caption contains N=100: {'N=100' in stdout}")
assert "N=100" in stdout
