import scanpy as sc
import numpy as np
adata = sc.read_h5ad('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/public-data/pbmc_1k_v3_filtered.h5ad')
sc.pp.filter_cells(adata, min_genes=200)
sc.pp.filter_genes(adata, min_cells=3)
adata.var['mt'] = adata.var_names.str.startswith('MT-')
sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], inplace=True)
adata = adata[adata.obs['pct_counts_mt'] < 20].copy()
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)
adata = adata[:, adata.var['highly_variable']].copy()
sc.pp.scale(adata, max_value=10)
sc.tl.pca(adata, svd_solver='arpack')
sc.pp.neighbors(adata, n_neighbors=15, use_rep='X_pca')
sc.tl.leiden(adata, resolution=1.0, flavor='igraph', n_iterations=2, directed=False)
sc.tl.paga(adata, groups='leiden')
conn = adata.uns['paga']['connectivities'].toarray()
vals = conn[np.triu_indices_from(conn, k=1)]
vals = vals[vals > 0]
print('n edges > 0:', len(vals))
for thr in [0.03, 0.05, 0.1, 0.2, 0.3, 0.5]:
    n_isolated = sum(1 for i in range(conn.shape[0]) if (conn[i] > thr).sum() == 0)
    print(f'threshold={thr}: isolated clusters = {n_isolated}/{conn.shape[0]}, edges surviving = {(vals>thr).sum()}/{len(vals)}')
print('connectivity value distribution (nonzero): min', vals.min(), 'median', np.median(vals), 'max', vals.max())
