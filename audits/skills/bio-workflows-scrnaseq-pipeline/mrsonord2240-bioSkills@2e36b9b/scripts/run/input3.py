"""Input 3 (Variant B) - bio-workflows-scrnaseq-pipeline
The "Alternative Path: Scanpy" block, SKILL.md:252-300, run VERBATIM (only the input path
repointed) on one SYNTHETIC sample. Then scored against ground truth, and the block's two
specific self-corrections (adata.raw before scaling; pinned leiden backend) checked.
"""
import scanpy as sc, numpy as np, pandas as pd
from sklearn.metrics import adjusted_rand_score
D = r'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'

# --- SKILL.md Scanpy path, verbatim ---
adata = sc.read_10x_mtx(D + '/S2/outs/filtered_feature_bc_matrix')
adata.var_names_make_unique()
print('loaded', adata.shape)

adata.var['mt'] = adata.var_names.str.startswith('MT-')
sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], percent_top=None, log1p=False, inplace=True)

sc.pp.filter_cells(adata, min_genes=200)
sc.pp.filter_genes(adata, min_cells=3)
adata = adata[adata.obs.n_genes_by_counts < 5000, :]
adata = adata[adata.obs.pct_counts_mt < 20, :]
print('after flat QC', adata.shape)

expected_rate = 0.008 * adata.n_obs / 1000
sc.pp.scrublet(adata, expected_doublet_rate=expected_rate)
adata = adata[~adata.obs['predicted_doublet'], :]
print(f'after scrublet (expected_rate {expected_rate:.4f})', adata.shape)

sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)

adata.raw = adata
adata = adata[:, adata.var.highly_variable]
sc.pp.scale(adata, max_value=10)
sc.tl.pca(adata, n_comps=50)
sc.pp.neighbors(adata, n_neighbors=15, n_pcs=30)
sc.tl.umap(adata)
sc.tl.leiden(adata, resolution=0.5, flavor='igraph', n_iterations=2, directed=False)
sc.tl.rank_genes_groups(adata, 'leiden', method='wilcoxon')
print('clusters:', adata.obs['leiden'].nunique())
adata.write('F:/OpenScience/audits/bio-workflows-scrnaseq-pipeline/run/input3_scanpy.h5ad')
print('block ran to completion, object written')

# --- AUDIT ---
print('\n=== AUDIT ===')
tc = pd.read_csv(D + '/truth_cells.csv')
tc = tc[tc['sample'] == 'S2'].set_index('barcode')
kept = [b for b in adata.obs_names]
sub = tc.loc[kept]
print(f'true doublets: {int(tc.true_doublet.sum())} injected, {int(sub.true_doublet.sum())} left '
      f'({100*(1-sub.true_doublet.sum()/tc.true_doublet.sum()):.0f}% removed)')
print(f'true low-quality: {int(tc.true_low_quality.sum())} injected, '
      f'{int(sub.true_low_quality.sum())} left '
      f'({100*(1-sub.true_low_quality.sum()/tc.true_low_quality.sum()):.0f}% removed)')
print(f'clustering ARI vs true cell type: '
      f'{adjusted_rand_score(sub.true_cell_type, adata.obs["leiden"]):.3f}')

# the block's own inline warning: .raw before scaling, so LFCs are not computed from z-scores
df = sc.get.rank_genes_groups_df(adata, group=None)
print(f'\nrank_genes_groups logfoldchanges: {int(df.logfoldchanges.isna().sum())} NaN of {len(df)}; '
      f'range {df.logfoldchanges.min():.2f} to {df.logfoldchanges.max():.2f}')
print('  (the block sets adata.raw BEFORE scale, which is what keeps these finite)')
# what happens if you do not
b = sc.read_10x_mtx(D + '/S2/outs/filtered_feature_bc_matrix'); b.var_names_make_unique()
sc.pp.filter_cells(b, min_genes=200); sc.pp.filter_genes(b, min_cells=3)
sc.pp.normalize_total(b, target_sum=1e4); sc.pp.log1p(b)
sc.pp.highly_variable_genes(b, n_top_genes=2000)
b = b[:, b.var.highly_variable].copy()
sc.pp.scale(b, max_value=10)
sc.tl.pca(b, n_comps=50); sc.pp.neighbors(b, n_neighbors=15, n_pcs=30)
sc.tl.leiden(b, resolution=0.5, flavor='igraph', n_iterations=2, directed=False)
sc.tl.rank_genes_groups(b, 'leiden', method='wilcoxon')
d2 = sc.get.rank_genes_groups_df(b, group=None)
print(f'  WITHOUT adata.raw: {int(d2.logfoldchanges.isna().sum())} NaN of {len(d2)}; '
      f'range {np.nanmin(d2.logfoldchanges):.2f} to {np.nanmax(d2.logfoldchanges):.2f}')

# the leiden pinning claim
import warnings
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always')
    sc.tl.leiden(adata, resolution=0.5, key_added='unpinned')
    fw = [str(x.message)[:100] for x in w if issubclass(x.category, FutureWarning)]
print(f'\nunpinned sc.tl.leiden FutureWarning: {fw[:1] if fw else "none"}')
print(f'  ARI(pinned, unpinned) = {adjusted_rand_score(adata.obs["leiden"], adata.obs["unpinned"]):.4f}')
print('DONE')
