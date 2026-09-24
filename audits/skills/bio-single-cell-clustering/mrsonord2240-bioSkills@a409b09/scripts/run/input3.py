"""Input 3 (Edge) - bio-single-cell-clustering
"One giant blob" / "is this one population or several?" - the Skill's Common Errors row 1 and
the Validating section. A sorted, near-homogeneous CD4 T-cell capture where the honest answer is
"one population", and the Skill's own diagnostics have to say so.

Derived SYNTHETIC data: ../data/sorted_cd4_clean.h5ad - 1,400 CD4 T cells (no doublets, no
low-quality) drawn from the synthetic 8-sample PBMC set, seed 20260916.
"""
import scanpy as sc
import numpy as np
import pandas as pd
from sklearn.metrics import adjusted_rand_score

D = r'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
DATA = r'F:/OpenScience/audits/bio-single-cell-clustering/data'
rng = np.random.default_rng(20260916)

a = sc.read_h5ad(D + '/all_samples_filtered.h5ad')
tc = pd.read_csv(D + '/truth_cells.csv').set_index('cell_id').loc[a.obs_names]
keep = ((tc['true_cell_type'] == 'CD4 T cells') & ~tc['true_doublet'].astype(bool)
        & ~tc['true_low_quality'].astype(bool)).values
a = a[keep].copy()
a = a[rng.choice(a.n_obs, 1400, replace=False)].copy()
a.write_h5ad(DATA + '/sorted_cd4_clean.h5ad')
print(f'Sorted CD4 capture: {a.n_obs} cells, ONE true cell type, {a.obs["sample"].nunique()} donors')

a.layers['counts'] = a.X.copy()
sc.pp.normalize_total(a); sc.pp.log1p(a)
sc.pp.highly_variable_genes(a, n_top_genes=2000, flavor='seurat_v3', layer='counts')
sc.tl.pca(a, n_comps=50, svd_solver='arpack', mask_var='highly_variable', random_state=0)
sc.pp.neighbors(a, n_neighbors=15, n_pcs=30, random_state=0)

# --- the sweep the Skill prescribes, and the diagnostic it names ---
print('\nresolution sweep on a single true population:')
for res in [0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0]:
    key = f'r{res}'
    sc.tl.leiden(a, resolution=res, key_added=key, flavor='igraph', n_iterations=2,
                 directed=False, random_state=0)
    k = a.obs[key].nunique()
    line = f'  resolution {res}: {k} clusters'
    if k > 1:
        sc.tl.rank_genes_groups(a, key, method='wilcoxon')
        top = {g: list(pd.DataFrame(a.uns['rank_genes_groups']['names'])[g][:10])
               for g in a.obs[key].cat.categories}
        gs = list(top)
        ov = np.mean([len(set(top[gs[i]]) & set(top[gs[j]])) / 10
                      for i in range(len(gs)) for j in range(i + 1, len(gs))])
        pmin = float(np.min(pd.DataFrame(a.uns['rank_genes_groups']['pvals_adj']).min()))
        line += (f'; mean top-10 marker overlap between clusters = {ov:.2f}; '
                 f'smallest adjusted p across all splits = {pmin:.2e}')
    print(line)

print('\nSKILL Common Errors row 1: "if markers stay uniform across a resolution sweep, the blob may')
print('be a single real population, not a parameter bug" - the overlap column above is that check.')

# --- stability, the Skill's "necessary, not sufficient" test, at resolution 0.6 ---
sc.tl.leiden(a, resolution=0.6, key_added='base', flavor='igraph', n_iterations=2,
             directed=False, random_state=0)
base = a.obs['base'].values
jac = []
for b in range(10):
    idx = rng.choice(a.n_obs, int(0.8 * a.n_obs), replace=False)
    sub = a[idx].copy()
    sc.pp.neighbors(sub, n_neighbors=15, n_pcs=30, random_state=0)
    sc.tl.leiden(sub, resolution=0.6, key_added='bb', flavor='igraph', n_iterations=2,
                 directed=False, random_state=0)
    for g in np.unique(base[idx]):
        m = base[idx] == g
        best = max((np.sum(m & (sub.obs['bb'].values == h)) /
                    np.sum(m | (sub.obs['bb'].values == h)))
                   for h in sub.obs['bb'].cat.categories)
        jac.append((g, best))
jd = pd.DataFrame(jac, columns=['cluster', 'jaccard']).groupby('cluster').jaccard.mean()
print('\nbootstrap stability (10 x 80% resample, Jaccard per cluster; Skill says >= 0.6-0.7 = stable):')
print(jd.round(3).to_string())
print(f'  -> {int((jd >= 0.6).sum())}/{len(jd)} clusters pass the Skill\'s stability bar '
      f'even though every cell here is the same true type.')
print('  This is exactly the Skill\'s point: "Stable does not mean real."')
print('DONE')

# --- what IS the split, then? the Skill's "A cluster maps to one sample/lane only" row ---
ct = pd.crosstab(a.obs['base'], a.obs['batch'])
print('\ncluster x batch (the split at resolution 0.6):')
print(ct.to_string())
print('cluster x sample:')
print(pd.crosstab(a.obs['base'], a.obs['sample']).to_string())
print(f'ARI(cluster, batch) = {adjusted_rand_score(a.obs["base"], a.obs["batch"]):.3f}; '
      f'ARI(cluster, sample) = {adjusted_rand_score(a.obs["base"], a.obs["sample"]):.3f}; '
      f'ARI(cluster, condition) = {adjusted_rand_score(a.obs["base"], a.obs["condition"]):.3f}')
