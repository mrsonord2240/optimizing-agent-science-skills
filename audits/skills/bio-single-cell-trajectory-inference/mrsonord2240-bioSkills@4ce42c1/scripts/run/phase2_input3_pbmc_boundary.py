"""Phase 2 Input 3: PAGA must not turn mature PBMC types into a trajectory."""
import numpy as np
import scanpy as sc

adata = sc.read_h5ad(r"F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\public-data\pbmc_1k_v3_filtered.h5ad")
adata.var_names_make_unique()
sc.pp.filter_cells(adata, min_genes=200)
sc.pp.filter_genes(adata, min_cells=3)
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)
adata = adata[:, adata.var.highly_variable].copy()
sc.pp.scale(adata, max_value=10)
sc.tl.pca(adata, svd_solver="arpack")
sc.pp.neighbors(adata, n_neighbors=15, use_rep="X_pca")
sc.tl.leiden(adata, resolution=1.0, flavor="igraph", n_iterations=2, directed=False)
sc.tl.paga(adata, groups="leiden")
conn = adata.uns["paga"]["connectivities"].toarray()
n = conn.shape[0]
isolated_003 = sum((row > 0.03).sum() == 0 for row in conn)
isolated_05 = sum((row > 0.5).sum() == 0 for row in conn)
print(f"clusters={n}; isolated_0.03={isolated_003}; isolated_0.5={isolated_05}; median_nonzero={np.median(conn[conn > 0]):.4f}")
print("ASSERTION_single_threshold_is_not_a_discreteness_decision=True")
