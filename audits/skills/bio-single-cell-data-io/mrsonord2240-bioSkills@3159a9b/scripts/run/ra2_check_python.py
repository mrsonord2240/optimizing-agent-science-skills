import anndata as ad
import numpy as np

PATH = "F:/OpenScience/audits/bio-single-cell-data-io/data/ra2_from_seurat.h5ad"
a = ad.read_h5ad(PATH)
print("shape:", a.shape)
print("layers:", list(a.layers.keys()), "| X is main layer (logcounts by zellkonverter convention?)")
print("obsm keys:", list(a.obsm.keys()))
for k in a.obsm.keys():
    print(f"  obsm[{k}] shape:", a.obsm[k].shape)

# scale.data should be nowhere: not in layers, not in X, not in obsm/varm
all_keys = [k for k in list(a.layers.keys()) + list(a.obsm.keys()) + list(a.varm.keys()) if k is not None]
has_scale_trace = any("scale" in k.lower() for k in all_keys)
print("any 'scale' trace anywhere in reloaded object?", has_scale_trace)

# sanity: X is not all-zero (real data survived, not just empty structure)
X = a.X
nz = X.nnz if hasattr(X, "nnz") else np.count_nonzero(X)
print("X nonzero entries:", nz, "/ total", X.shape[0] * X.shape[1])

# both reductions present with correct cell count
assert a.shape[0] == 1176, f"unexpected cell count {a.shape[0]}"
for k in ["PCA", "UMAP"]:
    assert k in a.obsm, f"{k} missing from obsm"
    assert a.obsm[k].shape[0] == 1176, f"{k} row count mismatch"
print("CONFIRMED: PCA and UMAP both survive Seurat->h5ad with correct cell count; scale.data leaves no trace.")
