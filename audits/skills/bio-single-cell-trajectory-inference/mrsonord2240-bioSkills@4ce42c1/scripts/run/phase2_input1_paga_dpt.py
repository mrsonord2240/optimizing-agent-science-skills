"""Phase 2 Input 1: PAGA topology and DPT from a marker-anchored root."""
import numpy as np
import scanpy as sc

adata = sc.read_h5ad(r"F:\OpenScience\audits\_pre-fix-20260919\bio-single-cell-trajectory-inference\data\paul15_raw.h5ad")
adata.X = adata.X.astype("float64")
sc.pp.recipe_zheng17(adata)
sc.tl.pca(adata, svd_solver="arpack")
sc.pp.neighbors(adata, n_neighbors=15, use_rep="X_pca")
sc.tl.leiden(adata, resolution=1.0, flavor="igraph", n_iterations=2, directed=False)
sc.tl.paga(adata, groups="leiden")
sc.pl.paga(adata, threshold=0.03, show=False)
sc.tl.umap(adata, init_pos="paga")
sc.tl.diffmap(adata, n_comps=15)
roots = np.flatnonzero(adata.obs["paul15_clusters"] == "7MEP")
assert len(roots), "No MEP marker-anchored root was found"
adata.uns["iroot"] = int(roots[0])
sc.tl.dpt(adata, n_dcs=10, n_branchings=0)
means = adata.obs.groupby("paul15_clusters", observed=True)["dpt_pseudotime"].mean()
mep = float(means["7MEP"])
mature = float(means[means.index.isin(["1Ery", "16Neu", "15Mo"])].mean())
print(f"cells={adata.n_obs}; paga_clusters={adata.obs['leiden'].nunique()}")
print(f"MEP_dpt={mep:.4f}; mature_dpt={mature:.4f}")
print(f"ASSERTION marker_anchored_MEP_precedes_mature={mep < mature}")
