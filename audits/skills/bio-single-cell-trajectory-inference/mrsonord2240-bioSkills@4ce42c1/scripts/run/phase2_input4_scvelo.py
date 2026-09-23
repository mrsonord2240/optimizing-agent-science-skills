"""Phase 2 Input 4: exact documented deterministic scVelo core workflow."""
import numpy as np
import scanpy as sc
import scvelo as scv

adata = sc.read_h5ad(r"F:\OpenScience\audits\_pre-fix-20260919\bio-single-cell-trajectory-inference\data\pancreas_raw.h5ad")
scv.pp.filter_and_normalize(adata, min_shared_counts=20)
adata.layers["normalized_X"] = adata.X.copy()
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)
adata = adata[:, adata.var["highly_variable"]].copy()
adata.X = adata.layers.pop("normalized_X")
scv.pp.moments(adata, n_pcs=30, n_neighbors=30)
scv.tl.velocity(adata, mode="deterministic")
scv.tl.velocity_graph(adata, n_jobs=1, show_progress_bar=False)
scv.tl.velocity_confidence(adata)
scv.tl.velocity_pseudotime(adata)
means = adata.obs.groupby("clusters", observed=True)["velocity_pseudotime"].mean().sort_values()
ductal = float(means["Ductal"])
confidence = float(adata.obs["velocity_confidence"].mean())
print(f"shape={adata.shape}; confidence={confidence:.4f}; ductal_pt={ductal:.4f}; minimum_cluster={means.index[0]}")
print(f"ASSERTION_deterministic_velocity_runs_and_ductal_is_earliest={means.index[0] == 'Ductal'}")
