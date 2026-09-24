"""Input 3 (Edge) - bio-single-cell-markers-annotation
The Common Errors row: "NaN / degenerate logFC and p-values from marker ranking / Only one
cluster present, so the 'vs rest' reference is empty / Marker ranking needs >=2 groups".
Tested on a genuinely homogeneous sorted population.
"""
import scanpy as sc, numpy as np, pandas as pd, warnings
D = r'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
a = sc.read_h5ad(D + '/all_samples_filtered.h5ad')
tc = pd.read_csv(D + '/truth_cells.csv').set_index('cell_id').loc[a.obs_names]
keep = ((tc['true_cell_type'] == 'CD4 T cells') & ~tc['true_doublet'].astype(bool)
        & ~tc['true_low_quality'].astype(bool)).values
a = a[keep].copy()
a.layers['counts'] = a.X.copy()
sc.pp.normalize_total(a, target_sum=1e4); sc.pp.log1p(a)
sc.pp.highly_variable_genes(a, n_top_genes=2000, flavor='seurat_v3', layer='counts')
sc.tl.pca(a, n_comps=50, mask_var='highly_variable', random_state=0)
sc.pp.neighbors(a, random_state=0)
a.obs['one'] = pd.Categorical(['all'] * a.n_obs)
print(f'{a.n_obs} CD4 T cells, one group only')

print('\n(a) rank_genes_groups with a single group (the documented degenerate case):')
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always')
    try:
        sc.tl.rank_genes_groups(a, groupby='one', method='wilcoxon', pts=True)
        df = sc.get.rank_genes_groups_df(a, group=None)
        print(f'  ran without error. rows {len(df)}; NaN logfoldchanges '
              f'{int(df.logfoldchanges.isna().sum())}; NaN pvals {int(df.pvals.isna().sum())}; '
              f'smallest padj {df.pvals_adj.min()}')
    except Exception as e:
        print(f'  ERROR RAISED: {type(e).__name__}: {str(e)[:200]}')
    print('  warnings:', [f'{x.category.__name__}: {str(x.message)[:110]}' for x in w][:3] or 'none')

print('\n(b) the Skill\'s prescribed fix: subcluster, then rank')
sc.tl.leiden(a, resolution=0.5, flavor='igraph', n_iterations=2, directed=False, random_state=0)
print(f'  subclustering gives {a.obs["leiden"].nunique()} groups')
sc.tl.rank_genes_groups(a, groupby='leiden', method='wilcoxon', pts=True)
df2 = sc.get.rank_genes_groups_df(a, group=None)
spec = df2[(df2.logfoldchanges > 1) & (df2.pct_nz_group > 0.5) & (df2.pct_nz_reference < 0.25)]
print(f'  markers {len(df2)} -> "specific" {len(spec)}; smallest padj {df2.pvals_adj.min():.2e}')
print(f'  clusters x batch: ')
print(pd.crosstab(a.obs["leiden"], a.obs["batch"]).to_string())
print('  -> the Skill\'s OTHER option for this row is "report it as a single homogeneous type".')
print('     Every cell here IS one true type, so that is the correct branch; the subcluster')
print('     branch produces markers that only track the sequencing batch.')
print('DONE')
