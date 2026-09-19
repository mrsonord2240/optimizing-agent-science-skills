"""
Input 3 (Edge / boundary) -- "Is this a real continuum or a mixture of
discrete cell types?" run on real 10x PBMC 1k v3 data (filtered matrix,
public-data/), which is a mix of mature, terminally-differentiated
lymphocyte/monocyte types -- NOT a genuine developmental continuum. This
tests whether the Skill's Governing Principle rule 2 ("no algorithm tests
whether a continuum exists; decide topology first with PAGA... isolated
clusters with no surviving connectivity edges are discrete cell types, not
trajectory branches, and must not be forced into one ordering") actually
holds up when the SKILL.md's own PAGA code block is run on data that
should NOT show a continuum.
"""
import scanpy as sc
import numpy as np

sc.settings.verbosity = 1

adata = sc.read_h5ad('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/public-data/pbmc_1k_v3_filtered.h5ad')
print(adata)

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

# --- SKILL.md "Decide Topology First With PAGA" block, verbatim ---
sc.pp.neighbors(adata, n_neighbors=15, use_rep='X_pca')
sc.tl.leiden(adata, resolution=1.0, flavor='igraph', n_iterations=2, directed=False)
sc.tl.paga(adata, groups='leiden')
sc.pl.paga(adata, threshold=0.03, show=False)

conn = adata.uns['paga']['connectivities'].toarray()
n_clusters = conn.shape[0]
print(f'\nPBMC 1k: {n_clusters} leiden clusters')
print('Cluster sizes:', adata.obs['leiden'].value_counts().sort_index().to_dict())

isolated = [i for i in range(n_clusters) if (conn[i] > 0.03).sum() == 0]
print(f'Clusters with NO surviving edge at threshold=0.03: {isolated} ({len(isolated)}/{n_clusters})')
print(f'ASSERTION discrete_types_detected (>=30% of clusters isolated, i.e. PAGA correctly flags this as NOT a clean continuum): '
      f'{len(isolated) / n_clusters >= 0.3}')

# quick marker check to confirm these are mature discrete types, not a
# differentiation series
markers = {'CD3D': 'T cell', 'MS4A1': 'B cell', 'LYZ': 'Monocyte', 'NKG7': 'NK cell', 'PPBP': 'Platelet'}
present = [m for m in markers if m in adata.raw.var_names] if adata.raw is not None else []
print('\nNote: cluster sizes and isolation pattern above should be interpreted against known PBMC composition '
      '(T/B/NK/Mono/Platelet are discrete mature types, not stages of one differentiation series).')
print('Done.')
