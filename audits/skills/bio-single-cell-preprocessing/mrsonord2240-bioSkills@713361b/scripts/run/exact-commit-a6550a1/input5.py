"""Input 5 (Stress) - bio-single-cell-preprocessing
Multi-part: a depth-imbalanced 8-sample design (batch B sequenced ~3x shallower), where the
Skill's three headline multi-sample claims are all testable at once -
  (a) global MAD over-cuts the shallow batch and under-cuts the deep one   (SKILL.md:79)
  (b) HVG batch_key avoids batch-specific technical genes                   (SKILL.md:176)
  (c) reflexive regress_out of total_counts / pct_counts_mt erases biology  (SKILL.md:189)

Derived SYNTHETIC data: ../data/depth_imbalanced.h5ad - the synthetic 8-sample PBMC matrix with
samples S3,S4,S7,S8 (batch B) binomially downsampled to 35% of their counts (seed 20260916).
"""
import scanpy as sc
import numpy as np
import pandas as pd
from scipy.stats import median_abs_deviation
from scipy import sparse
from sklearn.metrics import silhouette_score

D = r'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
DATA = r'F:/OpenScience/audits/bio-single-cell-preprocessing/data'
rng = np.random.default_rng(20260916)

a = sc.read_h5ad(D + '/all_samples_filtered.h5ad')
truth = pd.read_csv(D + '/truth_cells.csv').set_index('cell_id').loc[a.obs_names]
a.obs['true_cell_type'] = truth['true_cell_type'].values
a.obs['true_low_quality'] = truth['true_low_quality'].values

shallow = a.obs['sample'].isin(['S3', 'S4', 'S7', 'S8']).values
X = a.X.tocsr().astype(np.int64)
rows = []
for i in range(a.n_obs):
    r = X[i]
    d = r.data
    rows.append(sparse.csr_matrix((rng.binomial(d, 0.35) if shallow[i] else d, r.indices, r.indptr),
                                  shape=r.shape))
a.X = sparse.vstack(rows).astype(np.float32)
a.write_h5ad(DATA + '/depth_imbalanced.h5ad')

a.var['mt'] = a.var_names.str.startswith('MT-')
a.var['ribo'] = a.var_names.str.startswith(('RPS', 'RPL'))
a.var['hb'] = a.var_names.str.contains(r'^HB[ABDEGMQZ]\d*(?!\w)')
sc.pp.calculate_qc_metrics(a, qc_vars=['mt', 'ribo', 'hb'], percent_top=[20], log1p=True, inplace=True)
print('median total_counts per sample:')
print(a.obs.groupby('sample', observed=True)['total_counts'].median().round(0).to_string())


def is_outlier(ad, metric, nmads):
    M = ad.obs[metric]
    return (M < np.median(M) - nmads * median_abs_deviation(M)) | (np.median(M) + nmads * median_abs_deviation(M) < M)


flags = ['log1p_total_counts', 'log1p_n_genes_by_counts', 'pct_counts_in_top_20_genes']

# (a) global vs per-sample MAD
g = (is_outlier(a, flags[0], 5) | is_outlier(a, flags[1], 5) | is_outlier(a, flags[2], 5)
     | is_outlier(a, 'pct_counts_mt', 3) | (a.obs['pct_counts_mt'] > 8))
ps = pd.Series(False, index=a.obs_names)
for s, idx in a.obs.groupby('sample', observed=True).groups.items():
    sub = a[idx]
    ps.loc[idx] = (is_outlier(sub, flags[0], 5) | is_outlier(sub, flags[1], 5) | is_outlier(sub, flags[2], 5)
                   | is_outlier(sub, 'pct_counts_mt', 3) | (sub.obs['pct_counts_mt'] > 8)).values

tab = pd.DataFrame({'sample': a.obs['sample'].values, 'global': g.values, 'per_sample': ps.values,
                    'lowq': a.obs['true_low_quality'].values})
print('\n(a) removal rate per sample (batch B = S3,S4,S7,S8 is the shallow batch):')
summ = tab.groupby('sample').agg(n=('global', 'size'), global_rm=('global', 'mean'),
                                 per_sample_rm=('per_sample', 'mean'), true_lowq=('lowq', 'mean'))
print((summ * [1, 100, 100, 100]).round(1).to_string())
for nm, col in [('global', 'global'), ('per-sample', 'per_sample')]:
    tp = int((tab[col] & tab.lowq).sum()); fp = int((tab[col] & ~tab.lowq).sum())
    fn = int((~tab[col] & tab.lowq).sum())
    print(f'  {nm}: removed {int(tab[col].sum())} TP={tp} FP={fp} FN={fn} '
          f'recall={tp/max(tp+fn,1):.3f} precision={tp/max(tp+fp,1):.3f}')

a = a[~ps.values].copy()
sc.pp.filter_genes(a, min_cells=3)
a.layers['counts'] = a.X.copy()
sc.pp.normalize_total(a)
sc.pp.log1p(a)

# (b) HVG with and without batch_key
sc.pp.highly_variable_genes(a, n_top_genes=2000, flavor='seurat_v3', layer='counts')
nb = set(a.var_names[a.var.highly_variable])
try:
    sc.pp.highly_variable_genes(a, n_top_genes=2000, flavor='seurat_v3', layer='counts', batch_key='sample')
    wb = set(a.var_names[a.var.highly_variable])
    print(f'\n(b) HVGs: no batch_key vs batch_key -> {len(nb & wb)}/2000 shared, '
          f'{len(nb - wb)} unique to the no-batch_key list')
except Exception as e:
    print(f'\n(b) SKILL.md:176 batch_key advice FAILED on the shallow batch: '
          f'{type(e).__name__}: {str(e)[:160]}')
    print('    (seurat_v3 loess per batch is singular when a batch has too little depth; '
          'SKILL.md Common Errors has no row for this)')
    # workaround a careful agent would reach for, and whether it works
    a2 = a.copy()
    sc.pp.filter_genes(a2, min_cells=30)
    try:
        sc.pp.highly_variable_genes(a2, n_top_genes=2000, flavor='seurat_v3', layer='counts',
                                    batch_key='sample')
        wb = set(a2.var_names[a2.var.highly_variable])
        print(f'    workaround (filter_genes min_cells=30 first): OK, '
              f'{len(nb & wb)}/2000 shared with the no-batch_key list')
    except Exception as e2:
        print(f'    workaround also failed: {type(e2).__name__}: {str(e2)[:120]}')
    sc.pp.highly_variable_genes(a, n_top_genes=2000, flavor='seurat_v3', layer='counts')

sc.pp.pca(a, mask_var='highly_variable', random_state=0)
lab = a.obs['true_cell_type'].values
bat = a.obs['batch'].values
sil_t = silhouette_score(a.obsm['X_pca'][:, :30], lab, random_state=0)
sil_b = silhouette_score(a.obsm['X_pca'][:, :30], bat, random_state=0)
print(f'    PCA(no regression): silhouette by TRUE CELL TYPE={sil_t:.4f}, by BATCH={sil_b:.4f}')

# (c) reflexive regress_out, the thing the Skill tells you not to do
b = a[:, a.var.highly_variable].copy()
sc.pp.regress_out(b, ['total_counts', 'pct_counts_mt'])
sc.pp.pca(b, random_state=0)
sil_t2 = silhouette_score(b.obsm['X_pca'][:, :30], lab, random_state=0)
sil_b2 = silhouette_score(b.obsm['X_pca'][:, :30], bat, random_state=0)
print(f'(c) PCA after regress_out(total_counts, pct_counts_mt): '
      f'silhouette by TRUE CELL TYPE={sil_t2:.4f} (delta {sil_t2-sil_t:+.4f}), by BATCH={sil_b2:.4f}')
print('DONE')
