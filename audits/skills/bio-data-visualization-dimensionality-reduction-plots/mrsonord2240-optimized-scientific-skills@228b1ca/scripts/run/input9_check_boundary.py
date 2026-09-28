"""Regression input 9: check the minimum-shape run after palette remediation."""
from __future__ import annotations

from pathlib import Path
import importlib.util

ROOT = Path(r"F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots\run\boundary")
expected = ["pca.pdf", "scree.pdf", "umap_clusters.pdf", "tsne.pdf", "phate.pdf"]
for name in expected:
    path = ROOT / "figures" / name
    print(f"{name}: {path.stat().st_size if path.is_file() else 0} bytes")
    assert path.is_file() and path.stat().st_size > 5_000

spec = importlib.util.spec_from_file_location("embedding_phd_boundary", ROOT / "embedding_phd.py")
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
colors = module.categorical_colors(12)
unique = {tuple(color) for color in colors}
print(f"condition categories=12; PCA recipe colors distinct={len(unique)}")
assert len(unique) == 12
stdout = (ROOT / "boundary_stdout.txt").read_text(encoding="utf-8")
print(f"caption contains N=100: {'N=100' in stdout}")
assert "N=100" in stdout
