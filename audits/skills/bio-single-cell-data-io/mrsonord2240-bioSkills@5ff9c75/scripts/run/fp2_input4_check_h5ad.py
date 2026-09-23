"""Phase-2 Input 4 independent Python reload assertion."""
import anndata as ad
import numpy as np
path = "F:/OpenScience/audits/bio-single-cell-data-io/data/fp2_from_seurat.h5ad"
a = ad.read_h5ad(path)
keys = list(a.obsm.keys())
all_keys = list(a.layers.keys()) + keys + list(a.varm.keys())
print("shape", a.shape, "layers", list(a.layers.keys()), "obsm", keys)
print("obsm_shapes", {k: tuple(a.obsm[k].shape) for k in keys})
print("scale_trace", any("scale" in str(k).lower() for k in all_keys), "nonzero", a.X.nnz if hasattr(a.X, "nnz") else np.count_nonzero(a.X))
assert a.shape[0] == 1176
assert "PCA" in a.obsm and "UMAP" in a.obsm
assert a.obsm["PCA"].shape == (1176, 10) and a.obsm["UMAP"].shape == (1176, 2)
assert not any("scale" in str(k).lower() for k in all_keys)
print("PASS input4_Python")
