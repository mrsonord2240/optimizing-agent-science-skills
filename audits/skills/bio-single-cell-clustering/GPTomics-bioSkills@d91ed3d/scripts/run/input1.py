"""Input 1 (Canonical) - bio-single-cell-clustering
The Scanpy path exactly as SKILL.md:59-73 and the Sweep section prescribe: PCA -> elbow ->
neighbors -> Leiden with the pinned backend -> resolution sweep -> UMAP.
Scored against the SYNTHETIC ground-truth cell types (ARI / NMI), and the Skill's own
reproducibility claim (pin flavor/n_iterations/random_state) tested directly.
"""
import scanpy as sc
import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score

D = r'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
OUT = r'F:/OpenScience/audits/bio-single-cell-clustering/run'

a = sc.read_h5ad(D + '/all_samples_filtered.h5ad')
tc = pd.read_csv(D + '/truth_cells.csv').set_index('cell_id').loc[a.obs_names]
a.obs['true_cell_type'] = tc['true_cell_type'].values
a = a[~tc['true_doublet'].values.astype(bool) & ~tc['true_low_quality'].values.astype(bool)].copy()
a.layers['counts'] = a.X.copy()
sc.pp.normalize_total(a); sc.pp.log1p(a)
sc.pp.highly_variable_genes(a, n_top_genes=2000, flavor='seurat_v3', layer='counts')
print(f'{a.n_obs} clean cells, {int(a.var.highly_variable.sum())} HVGs, '
      f'{a.obs["true_cell_type"].nunique()} true cell types')

# --- SKILL.md:64-65 : PCA then the elbow ---
sc.tl.pca(a, n_comps=50, svd_solver='arpack', mask_var='highly_variable', random_state=0)
vr = a.uns['pca']['variance_ratio']
print('variance ratio, PCs 1-15:', np.round(vr[:15], 4))
# the Skill says to read the elbow off the plot; quantify it so the choice is defensible
drops = vr[:-1] - vr[1:]
elbow = int(np.argmax(drops < 0.1 * drops[0]) + 1)
print(f'first PC where the drop falls below 10% of the first drop: {elbow}  '
      f'(the Skill recommends n_pcs 30-50 regardless)')

truth = a.obs['true_cell_type'].values
rows = []
for n_pcs in [10, 30, 50]:
    sc.pp.neighbors(a, n_neighbors=15, n_pcs=n_pcs, random_state=0)
    for res in [0.2, 0.4, 0.6, 0.8, 1.0, 2.0]:
        key = f'l_{n_pcs}_{res}'
        sc.tl.leiden(a, resolution=res, key_added=key, flavor='igraph',
                     n_iterations=2, directed=False, random_state=0)
        k = a.obs[key].nunique()
        rows.append(dict(n_pcs=n_pcs, resolution=res, k=k,
                         ARI=adjusted_rand_score(truth, a.obs[key]),
                         NMI=normalized_mutual_info_score(truth, a.obs[key])))
res_tab = pd.DataFrame(rows)
print('\nresolution / n_pcs sweep against the 8 true cell types:')
print(res_tab.round(3).to_string(index=False))
best = res_tab.loc[res_tab.ARI.idxmax()]
print(f'best ARI {best.ARI:.3f} at n_pcs={int(best.n_pcs)}, resolution={best.resolution} '
      f'({int(best.k)} clusters vs 8 true types)')
print('SKILL claim "n_pcs dominates the result far more than n_neighbors" - n_pcs effect on ARI:')
print(res_tab.groupby('n_pcs').ARI.agg(['min', 'max']).round(3).to_string())

# --- n_neighbors, the Skill's "secondary lever" ---
rows2 = []
for nn in [5, 15, 30, 50]:
    sc.pp.neighbors(a, n_neighbors=nn, n_pcs=30, random_state=0)
    sc.tl.leiden(a, resolution=0.6, key_added='tmp', flavor='igraph', n_iterations=2,
                 directed=False, random_state=0)
    rows2.append(dict(n_neighbors=nn, k=a.obs['tmp'].nunique(),
                      ARI=adjusted_rand_score(truth, a.obs['tmp'])))
print('n_neighbors sweep at n_pcs=30, resolution=0.6:')
print(pd.DataFrame(rows2).round(3).to_string(index=False))

# --- the Skill's reproducibility claim: pinned vs unpinned backend ---
sc.pp.neighbors(a, n_neighbors=15, n_pcs=30, random_state=0)
sc.tl.leiden(a, resolution=0.6, key_added='p1', flavor='igraph', n_iterations=2,
             directed=False, random_state=0)
sc.tl.leiden(a, resolution=0.6, key_added='p2', flavor='igraph', n_iterations=2,
             directed=False, random_state=0)
print(f'\npinned backend, two runs: ARI(p1,p2) = {adjusted_rand_score(a.obs.p1, a.obs.p2):.4f}, '
      f'identical labels = {bool((a.obs.p1.values == a.obs.p2.values).all())}')
import warnings
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always')
    sc.tl.leiden(a, resolution=0.6, key_added='u1')
    msgs = [str(x.message)[:120] for x in w if issubclass(x.category, FutureWarning)]
print('unpinned sc.tl.leiden FutureWarning:', msgs[:1] if msgs else 'none raised')
print(f'unpinned vs pinned: ARI = {adjusted_rand_score(a.obs.u1, a.obs.p1):.4f}, '
      f'{a.obs.u1.nunique()} vs {a.obs.p1.nunique()} clusters')

sc.tl.umap(a, min_dist=0.3, random_state=0)
a.write_h5ad(OUT + '/input1_clustered.h5ad')
print('DONE')
