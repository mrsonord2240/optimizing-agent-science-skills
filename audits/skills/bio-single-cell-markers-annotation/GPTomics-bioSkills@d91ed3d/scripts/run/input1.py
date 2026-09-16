"""Input 1 (Canonical) - bio-single-cell-markers-annotation
Scanpy marker detection exactly as SKILL.md:61-71, the specificity filter it prescribes, and
manual labelling with the canonical PBMC marker table at SKILL.md:164-172. Scored against the
SYNTHETIC ground-truth cell types. Also tests the "Defaults that bite" row about method=None.
"""
import scanpy as sc, numpy as np, pandas as pd
from sklearn.metrics import adjusted_rand_score

D = r'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
OUT = r'F:/OpenScience/audits/bio-single-cell-markers-annotation/run'
a = sc.read_h5ad(D + '/all_samples_filtered.h5ad')
tc = pd.read_csv(D + '/truth_cells.csv').set_index('cell_id').loc[a.obs_names]
a.obs['true_cell_type'] = tc['true_cell_type'].values
a = a[(~tc['true_doublet'].astype(bool) & ~tc['true_low_quality'].astype(bool)).values].copy()
a.layers['counts'] = a.X.copy()
sc.pp.normalize_total(a, target_sum=1e4); sc.pp.log1p(a)
sc.pp.highly_variable_genes(a, n_top_genes=2000, flavor='seurat_v3', layer='counts')
sc.tl.pca(a, n_comps=50, mask_var='highly_variable', random_state=0)
sc.pp.neighbors(a, random_state=0)
sc.tl.leiden(a, resolution=0.3, flavor='igraph', n_iterations=2, directed=False, random_state=0)
print(f'{a.n_obs} cells, {a.obs["leiden"].nunique()} clusters, '
      f'{a.obs["true_cell_type"].nunique()} true types')

# --- "Defaults that bite" row 1: scanpy method=None resolves to t-test ---
import inspect
sig = inspect.signature(sc.tl.rank_genes_groups)
print(f'\nrank_genes_groups default method = {sig.parameters["method"].default!r}')
sc.tl.rank_genes_groups(a, groupby='leiden', key_added='def')
print(f'  params recorded after a default call: {a.uns["def"]["params"]}')
sc.tl.rank_genes_groups(a, groupby='leiden', method='wilcoxon', pts=True,
                        corr_method='benjamini-hochberg', key_added='wil')
dflt = pd.DataFrame(a.uns['def']['names'])
wilc = pd.DataFrame(a.uns['wil']['names'])
ov = np.mean([len(set(dflt[g][:20]) & set(wilc[g][:20])) / 20 for g in dflt.columns])
print(f'  top-20 marker overlap between the default call and explicit wilcoxon: {ov:.2f}')

# --- SKILL.md:66-70, verbatim ---
a.uns['rank_genes_groups'] = a.uns['wil']
markers = sc.get.rank_genes_groups_df(a, group=None)
print('\ncolumns returned by rank_genes_groups_df:', list(markers.columns))
specific = markers[(markers['logfoldchanges'] > 1) & (markers['pct_nz_group'] > 0.5)
                   & (markers['pct_nz_reference'] < 0.25)]
print(f'markers total {len(markers)} -> specific {len(specific)} '
      f'({specific["group"].nunique()}/{a.obs["leiden"].nunique()} clusters keep any)')
print(specific.groupby('group').head(5)[['group', 'names', 'logfoldchanges',
                                         'pct_nz_group', 'pct_nz_reference']].to_string(index=False))

# --- the Skill's point that p-value ranking is useless here ---
byp = markers.sort_values('pvals_adj').groupby('group').head(5)
print(f'\nsmallest adjusted p across all clusters: {markers.pvals_adj.min():.2e}; '
      f'genes at padj<0.05: {(markers.pvals_adj < 0.05).sum()} of {len(markers)}')
print('  top-5-by-p vs top-5-by-specificity overlap per cluster:',
      round(np.mean([len(set(byp[byp.group == g].names) &
                        set(specific[specific.group == g].names[:5])) / 5
                     for g in dflt.columns]), 2))

# --- manual labelling from the Skill's canonical PBMC table ---
PANEL = {'CD4 T': ['CD3D', 'CD4', 'IL7R'], 'CD8 T': ['CD3D', 'CD8A', 'CD8B'],
         'B': ['MS4A1', 'CD79A', 'CD19'], 'DC': ['FCER1A', 'CST3'],
         'NK': ['NKG7', 'GNLY', 'NCAM1'], 'CD14 Mono': ['CD14', 'LYZ', 'S100A8'],
         'FCGR3A Mono': ['FCGR3A', 'MS4A7'], 'Platelet': ['PPBP', 'PF4']}
sc_scores = {}
for lab, genes in PANEL.items():
    g = [x for x in genes if x in a.var_names]
    sc.tl.score_genes(a, gene_list=g, ctrl_size=50, n_bins=25, score_name=f's_{lab}')
    sc_scores[lab] = a.obs.groupby('leiden', observed=True)[f's_{lab}'].mean()
S = pd.DataFrame(sc_scores)
print('\nmodule score per cluster (rows = leiden, cols = canonical panel):')
print(S.round(2).to_string())
cluster_labels = S.idxmax(axis=1).to_dict()
a.obs['cell_type'] = a.obs['leiden'].map(cluster_labels).fillna('Unassigned')
print('assigned:', {k: v for k, v in sorted(cluster_labels.items(), key=lambda x: int(x[0]))})
XW = {'CD4 T': 'CD4 T cells', 'CD8 T': 'CD8 T cells', 'B': 'B cells', 'DC': 'Dendritic cells',
      'NK': 'NK cells', 'CD14 Mono': 'CD14+ Monocytes', 'FCGR3A Mono': 'FCGR3A+ Monocytes',
      'Platelet': 'Megakaryocytes'}
pred = a.obs['cell_type'].map(XW).values
print(f'\naccuracy of the manual labelling vs truth: {(pred == a.obs["true_cell_type"].values).mean():.3f}')
print(pd.crosstab(a.obs['true_cell_type'].values, pred).to_string())
a.write_h5ad(OUT + '/input1_markers.h5ad')
print('DONE')
