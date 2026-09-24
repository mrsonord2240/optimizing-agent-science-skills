"""Input 5 (Stress) - bio-single-cell-doublet-detection
Multi-part, and the part that matters is the claim the researcher wants to make.
  (a) multiplexed pool: 8 HTO-hashed donors in ONE 10x lane -> which cell count sets the rate?
      (SKILL.md:46 "the physical doublet rate is set by TOTAL lane loading")
  (b) the small CD3D+LYZ+ cluster the researcher wants to call a novel transitional state
      (Governing Principle + Common Errors row 4)
Data: SYNTHETIC 8-sample PBMC set treated as one pooled lane.
"""
import scanpy as sc
import numpy as np
import pandas as pd

D = r'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
a = sc.read_h5ad(D + '/all_samples_filtered.h5ad')
tc = pd.read_csv(D + '/truth_cells.csv').set_index('cell_id').loc[a.obs_names]
a.obs['true_doublet'] = tc['true_doublet'].values.astype(bool)
a.obs['true_cell_type'] = tc['true_cell_type'].values

# --- (a) the rate rule applied the two ways the Skill contrasts ---
per_sample_n = a.obs['sample'].value_counts().mean()
print('(a) expected-rate rule:')
print(f'  per demultiplexed sample (~{per_sample_n:.0f} cells): '
      f'{100*0.008*per_sample_n/1000:.2f}%  <- the Skill says this UNDERESTIMATES')
print(f'  from total lane loading ({a.n_obs} cells):        '
      f'{100*0.008*a.n_obs/1000:.2f}%  <- the Skill says use this')
print(f'  physical doublets actually injected:            '
      f'{100*a.obs["true_doublet"].mean():.2f}%')
print('  note: this synthetic set injects ~3% per 800-cell lane by design, above what the '
      '0.8%/1000 rule predicts, so absolute recall is not the Skill\'s fault - the comparison '
      'that matters is per-sample vs total-lane.')

# --- (b) cluster and look for the fake transitional population ---
a.layers['counts'] = a.X.copy()
sc.pp.normalize_total(a); sc.pp.log1p(a)
sc.pp.highly_variable_genes(a, n_top_genes=2000, flavor='seurat_v3', layer='counts')
sc.pp.pca(a, mask_var='highly_variable', random_state=0)
sc.pp.neighbors(a, random_state=0)
sc.tl.leiden(a, resolution=1.2, flavor='igraph', n_iterations=2, directed=False, random_state=0)
print(f'\n(b) {a.obs["leiden"].nunique()} Leiden clusters')

ln = a[:, ['CD3D', 'CD3E', 'LYZ', 'CD14', 'NKG7', 'MS4A1']].to_df()
tab = pd.DataFrame({
    'n': a.obs.groupby('leiden', observed=True).size(),
    'pct_true_doublet': 100 * a.obs.groupby('leiden', observed=True)['true_doublet'].mean(),
})
for g in ['CD3D', 'LYZ', 'MS4A1']:
    tab[f'{g}+'] = 100 * (ln[g] > 0).groupby(a.obs['leiden'], observed=True).mean()
tab['CD3D+LYZ+'] = 100 * ((ln['CD3D'] > 0) & (ln['LYZ'] > 0)).groupby(a.obs['leiden'], observed=True).mean()
tab = tab.sort_values('pct_true_doublet', ascending=False)
print(tab.round(1).head(8).to_string())

sus = tab.index[0]
print(f'\n  cluster {sus}: n={int(tab.loc[sus,"n"])}, {tab.loc[sus,"pct_true_doublet"]:.1f}% of it is a '
      f'true injected doublet, {tab.loc[sus,"CD3D+LYZ+"]:.1f}% co-express CD3D and LYZ.')
print('  true cell-type composition of that cluster (doublet parents are labelled by their first parent):')
print('   ', a.obs.loc[a.obs['leiden'] == sus, 'true_cell_type'].value_counts().head(4).to_dict())
print(f'  dataset-wide baseline: {100*a.obs["true_doublet"].mean():.1f}% doublets, '
      f'{100*((ln["CD3D"]>0)&(ln["LYZ"]>0)).mean():.1f}% CD3D+LYZ+ cells')
print('DONE')
