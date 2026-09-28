"""Regression input 3: fixed raw-HVG Scanpy UMAP/Leiden/exact-save workflow."""
from __future__ import annotations

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import numpy as np
import scanpy as sc
from sklearn.metrics import adjusted_rand_score
from sklearn.neighbors import NearestNeighbors

AUDIT = Path(r"F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots")
adata = sc.read_h5ad(AUDIT / "data" / "sc_synth4.h5ad")
raw_is_integer = np.allclose(adata.X, np.round(adata.X))
sc.pp.highly_variable_genes(adata, n_top_genes=500, flavor="seurat_v3", subset=True)
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.scale(adata, max_value=10)
sc.tl.pca(adata, n_comps=50, random_state=42)
sc.pp.neighbors(adata, n_neighbors=30, n_pcs=50)
sc.tl.umap(adata, min_dist=0.3, random_state=42)
sc.tl.leiden(adata, resolution=0.5, random_state=42, flavor="igraph", n_iterations=2, directed=False)
ax = sc.pl.umap(adata, color="leiden", palette="tab20", legend_loc="on data", show=False)
out = AUDIT / "figs" / "input3_umap_clusters.pdf"
ax.figure.savefig(out, dpi=300, bbox_inches="tight")

copy = adata.copy()
sc.tl.umap(copy, min_dist=0.3, random_state=42)
identical = np.array_equal(adata.obsm["X_umap"], copy.obsm["X_umap"])
ari = adjusted_rand_score(adata.obs["cluster_true"], adata.obs["leiden"])

def retention(high: np.ndarray, low: np.ndarray, k: int = 15) -> float:
    hi = NearestNeighbors(n_neighbors=k + 1).fit(high).kneighbors(high, return_distance=False)[:, 1:]
    lo = NearestNeighbors(n_neighbors=k + 1).fit(low).kneighbors(low, return_distance=False)[:, 1:]
    return float(np.mean([len(set(a) & set(b)) / k for a, b in zip(hi, lo)]))

kept = retention(adata.obsm["X_pca"][:, :50], adata.obsm["X_umap"])
print(f"raw integer source={raw_is_integer}; HVG retained={adata.n_vars}")
print(f"igraph Leiden clusters={adata.obs['leiden'].nunique()}, ARI={ari:.3f}")
print(f"seeded UMAP bit-identical={identical}")
print(f"15-NN retention={kept:.3f}")
print(f"exact output={out}, bytes={out.stat().st_size}")
assert raw_is_integer and adata.n_vars == 500
assert ari > 0.95
assert identical
assert out.stat().st_size > 5_000
