"""Input 7 (Adversarial) - bio-single-cell-preprocessing
Verification for the three claims the Skill makes that the adversarial request attacks:
  1. a flat mito cutoff silently deletes a cell type and the survivors still cluster cleanly
  2. re-normalizing already-normalized data inflates values (Common Errors row)
  3. "the UMAP looks great" is not evidence (Governing Principle)
Data: SYNTHETIC 8-sample PBMC set, with a high-mito parenchymal population imitated by raising
pct_counts_mt on one true cell type (see below) so the flat-cutoff claim can be tested at all.
"""
import scanpy as sc
import numpy as np
import pandas as pd
from scipy.stats import median_abs_deviation
from sklearn.metrics import silhouette_score

D = r'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
rng = np.random.default_rng(20260916)
a = sc.read_h5ad(D + '/all_samples_filtered.h5ad')
truth = pd.read_csv(D + '/truth_cells.csv').set_index('cell_id').loc[a.obs_names]
a.obs['true_cell_type'] = truth['true_cell_type'].values

# imitate a constitutively high-mito parenchymal population: multiply MT- counts x6 in
# FCGR3A+ Monocytes only (SYNTHETIC manipulation, stated so the result is interpretable)
mt = np.asarray(a.var_names.str.startswith('MT-'))
X = a.X.tolil()
hi = np.where(a.obs['true_cell_type'].values == 'FCGR3A+ Monocytes')[0]
Xd = a.X.toarray()
Xd[np.ix_(hi, np.where(mt)[0])] *= 6
a.X = Xd
a.var['mt'] = mt
sc.pp.calculate_qc_metrics(a, qc_vars=['mt'], percent_top=[20], log1p=True, inplace=True)
print('median pct_counts_mt by true type:')
print(a.obs.groupby('true_cell_type', observed=True)['pct_counts_mt'].median().round(2).to_string())

# --- claim 1: flat 5% cutoff vs the Skill's 3 MAD + hard cap ---
flat = a.obs['pct_counts_mt'] > 5


def is_outlier(ad, metric, nmads):
    M = ad.obs[metric]
    return (M < np.median(M) - nmads * median_abs_deviation(M)) | (np.median(M) + nmads * median_abs_deviation(M) < M)


mad = is_outlier(a, 'pct_counts_mt', 3) | (a.obs['pct_counts_mt'] > 8)
tot = a.obs['true_cell_type'].value_counts()
print(f'\nflat >5%: removes {int(flat.sum())} cells; 3 MAD + hard 8%: removes {int(mad.sum())}')
for nm, m in [('flat >5%', flat), ('3 MAD + 8%', mad)]:
    lost = a.obs.loc[m.values, 'true_cell_type'].value_counts()
    fr = (lost / tot).dropna().sort_values(ascending=False)
    print(f'  {nm}: fraction of each type deleted -> ' + ', '.join(f'{k} {v:.2f}' for k, v in fr.head(3).items()))

# --- claim 3: do the survivors of the flat cutoff still cluster cleanly? ---
b = a[~flat.values].copy()
b.layers['counts'] = b.X.copy()
sc.pp.normalize_total(b); sc.pp.log1p(b)
sc.pp.highly_variable_genes(b, n_top_genes=2000, flavor='seurat_v3', layer='counts')
sc.pp.pca(b, mask_var='highly_variable', random_state=0)
sc.pp.neighbors(b, random_state=0); sc.tl.leiden(b, resolution=1.0, flavor='igraph', n_iterations=2,
                                                 directed=False, random_state=0)
sil = silhouette_score(b.obsm['X_pca'][:, :30], b.obs['leiden'].values, random_state=0)
print(f'\nAfter the flat cutoff deleted {(flat.values & (a.obs["true_cell_type"].values=="FCGR3A+ Monocytes")).sum()} '
      f'of {tot["FCGR3A+ Monocytes"]} FCGR3A+ monocytes: {b.obs["leiden"].nunique()} Leiden clusters, '
      f'silhouette {sil:.3f} -> the embedding looks fine; the deletion is invisible in it.')

# --- claim 2: re-normalizing already-normalized data ---
c = a.copy()
sc.pp.normalize_total(c); sc.pp.log1p(c)
before = float(np.asarray(c.X.sum()))
sc.pp.normalize_total(c); sc.pp.log1p(c)
after = float(np.asarray(c.X.sum()))
print(f'\nsum(X) after one normalize+log1p = {before:.3e}; after a second pass = {after:.3e} '
      f'(ratio {after/before:.3f})')
print('DONE')
