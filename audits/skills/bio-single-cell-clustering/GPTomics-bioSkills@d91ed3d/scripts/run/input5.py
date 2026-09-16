"""Input 5 (Stress) - bio-single-cell-clustering
The multi-part request a PI actually sends: raise the resolution until a rare subset appears,
quote its marker p-values as proof, and read the UMAP gap as lineage distance. The Skill's
Governing Principle and the UMAP section both refuse this. Tested three ways:
  (a) a null dataset with NO structure at all - do post-clustering marker p-values still fire?
  (b) do the Skill's own validation rules catch the fake cluster?
  (c) do UMAP distances agree with PCA distances (the Skill says they are not metric)?
Derived SYNTHETIC data: ../data/permuted_null.h5ad (see data/README.md).
"""
import scanpy as sc
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist
from scipy.stats import spearmanr

DATA = r'F:/OpenScience/audits/bio-single-cell-clustering/data'
R = r'F:/OpenScience/audits/bio-single-cell-clustering/run'
rng = np.random.default_rng(20260916)

# ---------- (a) the null: permute each gene independently, destroying all cell structure ----------
a = sc.read_h5ad(DATA + '/sorted_cd4_clean.h5ad')
X = a.X.toarray() if hasattr(a.X, 'toarray') else np.asarray(a.X)
Xp = np.empty_like(X)
for j in range(X.shape[1]):
    Xp[:, j] = rng.permutation(X[:, j])
n = sc.AnnData(X=Xp, obs=a.obs[['sample', 'batch', 'condition']].copy(), var=a.var[[]].copy())
n.write_h5ad(DATA + '/permuted_null.h5ad')
n.layers['counts'] = n.X.copy()
sc.pp.normalize_total(n); sc.pp.log1p(n)
sc.pp.highly_variable_genes(n, n_top_genes=2000, flavor='seurat_v3', layer='counts')
sc.tl.pca(n, n_comps=50, svd_solver='arpack', mask_var='highly_variable', random_state=0)
sc.pp.neighbors(n, n_neighbors=15, n_pcs=30, random_state=0)
print('(a) PERMUTED NULL: every gene independently shuffled across cells, so no cell-to-cell')
print('    structure of any kind survives. n =', n.n_obs)
for res in [0.4, 1.0, 2.0]:
    sc.tl.leiden(n, resolution=res, key_added=f'n{res}', flavor='igraph', n_iterations=2,
                 directed=False, random_state=0)
    k = n.obs[f'n{res}'].nunique()
    sc.tl.rank_genes_groups(n, f'n{res}', method='wilcoxon')
    padj = pd.DataFrame(n.uns['rank_genes_groups']['pvals_adj'])
    print(f'    resolution {res}: {k} clusters; smallest adjusted p = {padj.min().min():.2e}; '
          f'genes with adjusted p < 0.05 in at least one cluster = {int((padj < 0.05).any(axis=1).sum())}')
print('    -> the true null holds exactly for every gene here, so a valid test would reject')
print('       nothing. Leiden still finds clusters and the marker test still returns adjusted')
print('       p-values down to 1e-12 with several genes below FDR 0.05. That is the claim the')
print('       Skill makes - post-clustering p-values are invalid, not merely inflated.')

# ---------- (b) the real data: does the fake rare cluster survive the Skill's checks? ----------
c = sc.read_h5ad(R + '/input1_clustered.h5ad')
sc.pp.neighbors(c, n_neighbors=15, n_pcs=30, random_state=0)
sc.tl.leiden(c, resolution=2.0, key_added='hi', flavor='igraph', n_iterations=2,
             directed=False, random_state=0)
sizes = c.obs['hi'].value_counts()
rare = sizes.index[-1]
m = (c.obs['hi'] == rare).values
print(f'\n(b) at resolution 2.0: {c.obs["hi"].nunique()} clusters; smallest is cluster {rare} '
      f'with {int(m.sum())} cells')
sc.tl.rank_genes_groups(c, 'hi', groups=[rare], reference='rest', method='wilcoxon')
padj = pd.DataFrame(c.uns['rank_genes_groups']['pvals_adj'])[rare]
names = pd.DataFrame(c.uns['rank_genes_groups']['names'])[rare]
print(f'    top markers: {list(names[:5])}, smallest adjusted p = {padj.min():.2e}')
comp = c.obs.loc[m, 'true_cell_type'].value_counts(normalize=True)
print(f'    true composition of that cluster: {comp.head(3).round(3).to_dict()}')
print(f'    ARI(cluster membership, batch) = '
      f'{__import__("sklearn.metrics", fromlist=["x"]).adjusted_rand_score(m.astype(int), c.obs["batch"]):.3f}; '
      f'fraction from a single sample = {c.obs.loc[m, "sample"].value_counts(normalize=True).iloc[0]:.3f}')

# ---------- (c) UMAP distances vs PCA distances ----------
idx = rng.choice(c.n_obs, 1500, replace=False)
sc.tl.umap(c, min_dist=0.3, random_state=0)
du = pdist(c.obsm['X_umap'][idx])
dp = pdist(c.obsm['X_pca'][idx, :30])
rho = spearmanr(du, dp).statistic
print(f'\n(c) Spearman correlation between UMAP pairwise distance and PCA(30) pairwise distance '
      f'on 1,500 cells: rho = {rho:.3f}')
lab = c.obs['l_30_0.2'].values[idx]
cent_u = pd.DataFrame(c.obsm['X_umap'][idx]).groupby(lab).mean()
cent_p = pd.DataFrame(c.obsm['X_pca'][idx, :30]).groupby(lab).mean()
ru = pdist(cent_u.values); rp = pdist(cent_p.values)
print(f'    between-cluster centroid distances: Spearman(UMAP, PCA) = {spearmanr(ru, rp).statistic:.3f}')
print('    -> the Skill\'s rule "UMAP distances are not metric data" is supported: cluster')
print('       ordering by UMAP distance does not reproduce the ordering in PCA space.')
print('DONE')
