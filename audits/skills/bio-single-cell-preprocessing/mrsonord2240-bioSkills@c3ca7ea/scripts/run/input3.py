"""Input 3 (Edge) - bio-single-cell-preprocessing
A tiny, low-complexity snRNA-seq-like capture: does the Skill's MAD recipe survive, and is
its Common Errors row ("MAD ~ 0 ... assert n_obs > 0 ... fall back to fixed cutoffs")
actually actionable?

Derived SYNTHETIC data: 120 nuclei-like barcodes built from sample S1 of the synthetic
8-sample PBMC set by (a) subsetting to 120 cells, (b) zeroing the 13 MT- genes to imitate a
nuclei prep, (c) downsampling counts to a near-constant depth so the MAD of the QC metrics
collapses. Written to ../data/tiny_nuclei.h5ad.
"""
import scanpy as sc
import numpy as np
import pandas as pd
from scipy.stats import median_abs_deviation

D = r'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
DATA = r'F:/OpenScience/audits/bio-single-cell-preprocessing/data'

rng = np.random.default_rng(20260916)
a = sc.read_h5ad(D + '/all_samples_filtered.h5ad')
a = a[a.obs['sample'] == 'S1'].copy()
a = a[rng.choice(a.n_obs, 120, replace=False)].copy()

# nuclei prep: no mitochondrial transcripts
mt = a.var_names.str.startswith('MT-')
X = a.X.toarray()
X[:, np.asarray(mt)] = 0
# low-complexity capture: 70% of nuclei land on an identical 800-UMI plateau (the
# ">50% share a value" case the Skill's Common Errors table names), 30% keep a tail
plateau = rng.permutation(X.shape[0])[:84]
newX = np.zeros_like(X)
for i in range(X.shape[0]):
    row = X[i]
    target = 800 if i in set(plateau.tolist()) else int(rng.integers(400, 2200))
    idx = np.repeat(np.arange(len(row)), row.astype(int))
    if len(idx) > target:
        idx = rng.choice(idx, target, replace=False)
    newX[i] = np.bincount(idx, minlength=len(row))
a.X = newX
a.write_h5ad(DATA + '/tiny_nuclei.h5ad')
print(f'Derived tiny nuclei-like set: {a.n_obs} cells, {a.n_vars} genes, '
      f'total_counts range {newX.sum(1).min():.0f}-{newX.sum(1).max():.0f}')

# --- SKILL.md Quality Control block, verbatim ---
a.var['mt'] = a.var_names.str.startswith('MT-')
a.var['ribo'] = a.var_names.str.startswith(('RPS', 'RPL'))
a.var['hb'] = a.var_names.str.contains(r'^HB[ABDEGMQZ]\d*(?!\w)')
sc.pp.calculate_qc_metrics(a, qc_vars=['mt', 'ribo', 'hb'], percent_top=[20], log1p=True, inplace=True)

for m in ['log1p_total_counts', 'log1p_n_genes_by_counts', 'pct_counts_in_top_20_genes', 'pct_counts_mt']:
    print(f'  {m}: median={np.median(a.obs[m]):.4f}  MAD={median_abs_deviation(a.obs[m]):.6f}')


def is_outlier(adata, metric, nmads):
    M = adata.obs[metric]
    return (M < np.median(M) - nmads * median_abs_deviation(M)) | (np.median(M) + nmads * median_abs_deviation(M) < M)


outlier = (is_outlier(a, 'log1p_total_counts', 5) | is_outlier(a, 'log1p_n_genes_by_counts', 5)
           | is_outlier(a, 'pct_counts_in_top_20_genes', 5))
mt_outlier = is_outlier(a, 'pct_counts_mt', 3) | (a.obs['pct_counts_mt'] > 8)
print(f'SKILL verbatim MAD rule: outlier={int(outlier.sum())}, mt_outlier={int(mt_outlier.sum())}, '
      f'survivors={int((~(outlier | mt_outlier)).sum())}/{a.n_obs}')

# --- the guard the Skill's Common Errors row prescribes ---
survivors = int((~(outlier | mt_outlier)).sum())
frac = survivors / a.n_obs
print(f'GUARD: survival fraction = {frac:.3f}')
if frac < 0.5:
    print('  -> Skill fallback triggered: MAD-adaptive collapsed, switching to fixed cutoffs')
    keep = (a.obs['n_genes_by_counts'] > 200) & (a.obs['total_counts'] > 500)
    print(f'  fixed-cutoff survivors: {int(keep.sum())}/{a.n_obs}')
else:
    print('  -> no fallback needed')

# does the Skill's mito rule do anything on nuclei?
print(f'pct_counts_mt: all zero? {bool((a.obs["pct_counts_mt"] == 0).all())} '
      f'-> mt_outlier flags {int(mt_outlier.sum())} cells (mito rule is inert on nuclei, as the Skill says)')
