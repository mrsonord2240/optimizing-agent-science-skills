"""Independently reproduce the fixed example's retention and inspect its five PDFs."""
from __future__ import annotations

from pathlib import Path
import re

import numpy as np
import scanpy as sc
from sklearn.neighbors import NearestNeighbors

ROOT = Path(r"F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots\run\example")
FIGS = ROOT / "figures"
expected = ["pca.pdf", "scree.pdf", "umap_clusters.pdf", "tsne.pdf", "phate.pdf"]

for name in expected:
    path = FIGS / name
    print(f"{name}: exists={path.is_file()} bytes={path.stat().st_size if path.is_file() else 0}")
    assert path.is_file() and path.stat().st_size > 5_000

adata = sc.read_h5ad(ROOT / "processed.h5ad")
sc.pp.highly_variable_genes(adata, n_top_genes=2_000, flavor="seurat_v3", subset=True)
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.scale(adata, max_value=10)
sc.tl.pca(adata, n_comps=50, random_state=42)
sc.pp.neighbors(adata, n_neighbors=30, n_pcs=50)
sc.tl.umap(adata, min_dist=0.3, random_state=42)

def independent_retention(high: np.ndarray, low: np.ndarray, k: int) -> float:
    hi = NearestNeighbors(n_neighbors=k + 1).fit(high).kneighbors(high, return_distance=False)[:, 1:]
    lo = NearestNeighbors(n_neighbors=k + 1).fit(low).kneighbors(low, return_distance=False)[:, 1:]
    intersections = np.fromiter((len(set(a).intersection(b)) for a, b in zip(hi, lo)), dtype=float)
    return float(np.mean(intersections / k))

retention = independent_retention(adata.obsm["X_pca"][:, :50], adata.obsm["X_umap"], 15)
stdout = (ROOT / "example_stdout.txt").read_text(encoding="utf-8")
match = re.search(r"retained ([0-9.]+)% of 15-nearest", stdout)
assert match, stdout
caption_percent = float(match.group(1))
print(f"independent 15-NN retention={retention:.6f} ({retention:.1%}); caption={caption_percent:.1f}%")
print(f"caption contains N=1200: {'N=1200' in stdout}")
assert abs(retention * 100 - caption_percent) < 0.06
assert "N=1200" in stdout
