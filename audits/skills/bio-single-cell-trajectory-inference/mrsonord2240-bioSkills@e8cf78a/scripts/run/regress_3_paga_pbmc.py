import numpy as np
import scanpy as sc

sc.settings.verbosity = 1

print("=" * 70)
print("REGRESSION INPUT 3: PAGA continuum-vs-discrete on real PBMC 1k (mature types)")
print("=" * 70)
pbmc = sc.read_h5ad(r"F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\public-data\pbmc_1k_v3_filtered.h5ad")
pbmc.var_names_make_unique()
sc.pp.filter_cells(pbmc, min_genes=200)
sc.pp.filter_genes(pbmc, min_cells=3)
sc.pp.normalize_total(pbmc, target_sum=1e4)
sc.pp.log1p(pbmc)
sc.pp.highly_variable_genes(pbmc, n_top_genes=2000)
pbmc = pbmc[:, pbmc.var.highly_variable].copy()
sc.pp.scale(pbmc, max_value=10)
sc.tl.pca(pbmc, svd_solver="arpack")
sc.pp.neighbors(pbmc, n_neighbors=15, use_rep="X_pca")
sc.tl.leiden(pbmc, resolution=1.0, flavor="igraph", n_iterations=2, directed=False)
sc.tl.paga(pbmc, groups="leiden")
conn = pbmc.uns["paga"]["connectivities"].toarray()
n_clusters = conn.shape[0]
isolated_003 = [i for i in range(n_clusters) if (conn[i] > 0.03).sum() == 0]
isolated_05 = [i for i in range(n_clusters) if (conn[i] > 0.5).sum() == 0]
print(f"{n_clusters} leiden clusters on real discrete PBMC data")
print("Isolated at threshold=0.03:", len(isolated_003), "/", n_clusters)
print("Isolated at threshold=0.5:", len(isolated_05), "/", n_clusters)
nz = conn[conn > 0]
print("Median nonzero connectivity:", np.median(nz))
print("DONE")
