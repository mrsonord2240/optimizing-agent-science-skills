"""
Input 1 (Canonical) -- PAGA continuum test + diffusion pseudotime rooted on a
known marker, following bio-single-cell-trajectory-inference SKILL.md
"Decide Topology First With PAGA" and "Diffusion Pseudotime From an Anchored
Root" code blocks, on real data: Paul et al. 2015 myeloid/erythroid
progenitor differentiation (scanpy's own sc.datasets.paul15(), 2730 cells x
3451 genes), the canonical published PAGA/DPT dataset (Wolf 2019 uses it).

Ground truth: Paul15 clusters are labelled by cell type, e.g. '7MEP'
(megakaryocyte-erythroid progenitor) and '9GMP'/'10GMP'
(granulocyte-monocyte progenitor) are the two early progenitor pools;
'1Ery'..'6Ery' are the erythroid maturation series (increasing maturity with
number); '15Mo','14Mo' / '16Neu','17Neu' are terminal myeloid/neutrophil
fates. A biologically correct pseudotime should increase monotonically
along the Ery numbering and should be low in MEP/GMP, high in mature
Ery/Mo/Neu.
"""
import numpy as np
import pandas as pd
import scanpy as sc

sc.settings.verbosity = 1

adata = sc.read_h5ad('../data/paul15_raw.h5ad')
adata.X = adata.X.astype('float64')

# Standard published preprocessing for this dataset (scanpy PAGA/DPT tutorial
# recipe: this is the documented real-world workflow the Skill assumes has
# already happened upstream in single-cell/preprocessing).
sc.pp.recipe_zheng17(adata)
sc.tl.pca(adata, svd_solver='arpack')

# --- SKILL.md "Decide Topology First With PAGA" block, run verbatim ---
sc.pp.neighbors(adata, n_neighbors=15, use_rep='X_pca')
sc.tl.leiden(adata, resolution=1.0, flavor='igraph', n_iterations=2, directed=False)
sc.tl.paga(adata, groups='leiden')
sc.pl.paga(adata, threshold=0.03, show=False)  # required: populates adata.uns['paga']['pos'] for init_pos='paga' below
sc.tl.umap(adata, init_pos='paga')

conn = adata.uns['paga']['connectivities'].toarray()
n_clusters = conn.shape[0]
above_thresh = (conn > 0.03).sum() - n_clusters  # exclude diagonal-ish zero
print(f'PAGA: {n_clusters} leiden clusters, connectivity matrix nnz above 0.03 threshold: {int((conn>0.03).sum())}')
print('Max connectivity value:', conn.max())
isolated = [i for i in range(n_clusters) if (conn[i] > 0.03).sum() == 0]
print(f'Clusters with NO edge surviving threshold=0.03 (would be discrete, per Skill rule 2): {isolated}')

# --- SKILL.md "Diffusion Pseudotime From an Anchored Root" block ---
sc.tl.diffmap(adata, n_comps=15)
# Anchor root on a known marker/cell-type label (MEP = earliest common
# progenitor in this dataset), not "by eye" -- exactly what the Skill
# prescribes and what its Common Errors table warns against violating.
root_candidates = np.flatnonzero(adata.obs['paul15_clusters'] == '7MEP')
print('Number of MEP (progenitor) cells found for rooting:', len(root_candidates))
adata.uns['iroot'] = int(root_candidates[0])
sc.tl.dpt(adata, n_dcs=10, n_branchings=0)

df = adata.obs[['paul15_clusters', 'dpt_pseudotime']].copy()
means = df.groupby('paul15_clusters', observed=True)['dpt_pseudotime'].mean().sort_values()
print('\nMean DPT pseudotime per published cell-type cluster (should be low for MEP/GMP progenitors, high for mature Ery/Mo/Neu):')
print(means.to_string())

# Assertion: is the erythroid maturation series (1Ery smallest number ->
# most immature, 6Ery -> most mature per Paul et al. numbering) monotone
# in mean pseudotime?
ery_order = ['1Ery', '2Ery', '3Ery', '4Ery', '5Ery', '6Ery']
ery_means = [means[c] for c in ery_order if c in means.index]
is_monotone = all(ery_means[i] <= ery_means[i+1] for i in range(len(ery_means)-1))
print(f'\nErythroid series present: {[c for c in ery_order if c in means.index]}')
print(f'Mean pseudotime values along series: {[round(v,4) for v in ery_means]}')
print(f'ASSERTION monotone_erythroid_pseudotime: {is_monotone}')

progenitor_mean = means.get('7MEP', np.nan)
mature_labels = [c for c in means.index if c.startswith('6Ery') or c in ('15Mo','17Neu','19Lymph')]
mature_mean = means[mature_labels].mean() if mature_labels else np.nan
print(f'\nMEP (progenitor) mean pseudotime: {progenitor_mean:.4f}')
print(f'Mature-fate labels mean pseudotime: {mature_mean:.4f}')
print(f'ASSERTION progenitor_lower_than_mature: {progenitor_mean < mature_mean}')

adata.write('../data/paul15_paga_dpt.h5ad')
print('\nDone.')
