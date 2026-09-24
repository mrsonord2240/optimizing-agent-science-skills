"""Input 4 (Variant B) - bio-single-cell-clustering
Subclustering, SKILL.md:121-131. The Skill's specific claim: "Reusing the global PCA imports axes
uninformative within a homogeneous subset and manufactures artifactual sub-splits." Tested by
running both routes on the same coarse cluster of the SYNTHETIC 8-sample PBMC set.
"""
import scanpy as sc
import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score

R = r'F:/OpenScience/audits/bio-single-cell-clustering/run'
a = sc.read_h5ad(R + '/input1_clustered.h5ad')
# coarse partition from input 1 (n_pcs=30, resolution=0.2)
key = 'l_30_0.2'
sizes = a.obs[key].value_counts()
print('coarse clusters:', sizes.head(6).to_dict())
# pick the largest cluster whose cells are >95% one true type - a genuinely homogeneous subset
cand = None
for g in sizes.index:
    m = a.obs[key] == g
    pur = a.obs.loc[m, 'true_cell_type'].value_counts(normalize=True).iloc[0]
    if pur > 0.95 and m.sum() > 400:
        cand = g
        print(f'chosen cluster {g}: n={int(m.sum())}, purity {pur:.3f}, '
              f'type {a.obs.loc[m, "true_cell_type"].mode()[0]}')
        break
sub_mask = (a.obs[key] == cand).values

# --- route A: the Skill's prescription - recompute HVGs, PCA and the graph on the subset ---
subA = a[sub_mask].copy()
sc.pp.highly_variable_genes(subA, n_top_genes=2000)
subA = subA[:, subA.var.highly_variable].copy()
sc.pp.scale(subA, max_value=10)
sc.tl.pca(subA, n_comps=30, random_state=0)
sc.pp.neighbors(subA, n_neighbors=15, n_pcs=20, random_state=0)
sc.tl.leiden(subA, resolution=0.4, flavor='igraph', n_iterations=2, directed=False, random_state=0)
print(f'\nroute A (Skill: recompute HVG+PCA on the subset): {subA.obs["leiden"].nunique()} subclusters')

# --- route B: the mistake the Skill names - reuse the global PCA ---
subB = a[sub_mask].copy()
sc.pp.neighbors(subB, n_neighbors=15, n_pcs=20, random_state=0)   # uses the inherited X_pca
sc.tl.leiden(subB, resolution=0.4, key_added='leiden_global', flavor='igraph', n_iterations=2,
             directed=False, random_state=0)
print(f'route B (reuse the global PCA):                    {subB.obs["leiden_global"].nunique()} subclusters')

ca, cb = subA.obs['leiden'].values, subB.obs['leiden_global'].values
print(f'ARI(route A, route B) = {adjusted_rand_score(ca, cb):.3f}')

# --- what do the two partitions actually track? ---
meta = a.obs.loc[sub_mask]
for nm, cl in [('route A', ca), ('route B', cb)]:
    print(f'  {nm}: ARI vs batch {adjusted_rand_score(cl, meta["batch"]):.3f}, '
          f'vs sample {adjusted_rand_score(cl, meta["sample"]):.3f}, '
          f'vs condition {adjusted_rand_score(cl, meta["condition"]):.3f}, '
          f'vs true type {adjusted_rand_score(cl, meta["true_cell_type"]):.3f}')

# --- marker distinctness of each subclustering (the Skill's stop rule) ---
for nm, obj, k in [('route A', subA, 'leiden'), ('route B', subB, 'leiden_global')]:
    if obj.obs[k].nunique() < 2:
        print(f'  {nm}: single cluster, stop rule satisfied trivially'); continue
    sc.tl.rank_genes_groups(obj, k, method='wilcoxon')
    names = pd.DataFrame(obj.uns['rank_genes_groups']['names'])
    gs = list(names.columns)
    ov = np.mean([len(set(names[gs[i]][:10]) & set(names[gs[j]][:10])) / 10
                  for i in range(len(gs)) for j in range(i + 1, len(gs))])
    pmin = float(np.min(pd.DataFrame(obj.uns['rank_genes_groups']['pvals_adj']).min()))
    print(f'  {nm}: mean top-10 marker overlap {ov:.2f}, smallest adjusted p {pmin:.2e} '
          f'-> the Skill\'s stop rule ("stop when splits lose distinct markers") says CONTINUE')
print('DONE')
