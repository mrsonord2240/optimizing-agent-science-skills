"""
T3 Result Determinism check: SKILL.md's PAGA/leiden/UMAP/DPT code blocks
never set an explicit seed anywhere in the shown code (no random_state=,
no np.random.seed()). Verify empirically whether re-running the exact
documented code twice, from the same input, on the same machine, gives
the same pseudotime result -- or whether the Skill is silently relying on
library defaults that an agent could not know are seeded without
independently checking.
"""
import numpy as np
import scanpy as sc

def run_once():
    adata = sc.read_h5ad('../data/paul15_raw.h5ad')
    adata.X = adata.X.astype('float64')
    sc.pp.recipe_zheng17(adata)
    sc.tl.pca(adata, svd_solver='arpack')
    sc.pp.neighbors(adata, n_neighbors=15, use_rep='X_pca')
    sc.tl.leiden(adata, resolution=1.0, flavor='igraph', n_iterations=2, directed=False)
    sc.tl.paga(adata, groups='leiden')
    sc.pl.paga(adata, threshold=0.03, show=False)
    sc.tl.umap(adata, init_pos='paga')
    sc.tl.diffmap(adata, n_comps=15)
    root = np.flatnonzero(adata.obs['paul15_clusters'] == '7MEP')[0]
    adata.uns['iroot'] = int(root)
    sc.tl.dpt(adata, n_dcs=10, n_branchings=0)
    return adata.obs['leiden'].astype(str).values, adata.obs['dpt_pseudotime'].values

leiden1, pt1 = run_once()
leiden2, pt2 = run_once()

n_leiden_clusters_1 = len(set(leiden1))
n_leiden_clusters_2 = len(set(leiden2))
print('Run 1: n_leiden_clusters =', n_leiden_clusters_1)
print('Run 2: n_leiden_clusters =', n_leiden_clusters_2)
print('Leiden cluster count matches:', n_leiden_clusters_1 == n_leiden_clusters_2)

corr = np.corrcoef(pt1, pt2)[0, 1]
max_abs_diff = np.max(np.abs(pt1 - pt2))
print(f'DPT pseudotime correlation between two runs (no seed set anywhere in SKILL.md code): {corr:.6f}')
print(f'Max abs diff: {max_abs_diff:.8f}')
print(f'ASSERTION deterministic_pseudotime (corr > 0.999): {corr > 0.999}')
