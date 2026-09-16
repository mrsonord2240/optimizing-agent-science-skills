"""Input 5 (Stress) - bio-single-cell-cell-annotation
"One cluster comes back with low confidence and no reference label fits - is it a novel type?"
The Skill's four-way triage (SKILL.md:129-147) run verbatim on a dataset where the answer is
known, because the doublets and low-quality cells are labelled.

Data: SYNTHETIC 8-sample PBMC set, but WITHOUT removing the injected doublets and low-quality
cells, so the artifacts the triage is meant to catch are actually present.
"""
import os
os.environ.setdefault('CELLTYPIST_FOLDER',
                      r'F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/cache/celltypist')
import scanpy as sc
import celltypist
import numpy as np
import pandas as pd

D = r'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
a = sc.read_h5ad(D + '/all_samples_filtered.h5ad')
tc = pd.read_csv(D + '/truth_cells.csv').set_index('cell_id').loc[a.obs_names]
a.obs['true_cell_type'] = tc['true_cell_type'].values
a.obs['true_doublet'] = tc['true_doublet'].values.astype(bool)
a.obs['true_low_quality'] = tc['true_low_quality'].values.astype(bool)
a.layers['counts'] = a.X.copy()
a.var['mt'] = a.var_names.str.startswith('MT-')
sc.pp.calculate_qc_metrics(a, qc_vars=['mt'], percent_top=[20], log1p=True, inplace=True)
print(f'{a.n_obs} cells INCLUDING {int(a.obs.true_doublet.sum())} injected doublets and '
      f'{int(a.obs.true_low_quality.sum())} low-quality cells')

sc.pp.normalize_total(a, target_sum=1e4); sc.pp.log1p(a)
sc.pp.highly_variable_genes(a, n_top_genes=2000, flavor='seurat_v3', layer='counts')
sc.tl.pca(a, n_comps=50, mask_var='highly_variable', random_state=0)
sc.pp.neighbors(a, random_state=0)
sc.tl.leiden(a, resolution=1.5, flavor='igraph', n_iterations=2, directed=False, random_state=0)

# doublet score so the triage has the column it expects
sc.pp.scrublet(a, batch_key='sample', expected_doublet_rate=0.03, random_state=0)

b = a.copy()
b.X = b.layers['counts'].copy()
sc.pp.normalize_total(b, target_sum=1e4); sc.pp.log1p(b)
pred = celltypist.annotate(b, model='Immune_All_Low.pkl', majority_voting=True,
                           over_clustering='leiden')
b = pred.to_adata()
for c in ['leiden', 'pct_counts_mt', 'n_genes_by_counts', 'predicted_doublet', 'sample',
          'true_doublet', 'true_low_quality', 'true_cell_type']:
    b.obs[c] = a.obs[c].values
print(f'{b.obs["leiden"].nunique()} clusters annotated')

# --- SKILL.md:135-144, run verbatim ---
cluster_conf = b.obs.groupby('leiden', observed=True)['conf_score'].median()
suspect = cluster_conf[cluster_conf < 0.5].index.tolist()
qc = b.obs.groupby('leiden', observed=True)[
    ['pct_counts_mt', 'n_genes_by_counts', 'predicted_doublet']].mean()
batch_purity = b.obs.groupby('leiden', observed=True)['sample'].agg(
    lambda s: s.value_counts(normalize=True).max())
print(f'\nSKILL triage block ran. clusters with median conf_score < 0.5: {suspect}')
tab = qc.join(batch_purity.rename('batch_purity'))
tab['median_conf'] = cluster_conf
tab['n'] = b.obs.groupby('leiden', observed=True).size()
tab['TRUE_doublet_frac'] = b.obs.groupby('leiden', observed=True)['true_doublet'].mean()
tab['TRUE_lowq_frac'] = b.obs.groupby('leiden', observed=True)['true_low_quality'].mean()
print(tab.round(3).sort_values('median_conf').to_string())

print('\nSCORING THE TRIAGE against the injected truth:')
print(f'  dataset baseline: {100*b.obs.true_doublet.mean():.1f}% doublets, '
      f'{100*b.obs.true_low_quality.mean():.1f}% low-quality')
if suspect:
    for s in suspect:
        r = tab.loc[s]
        verdict = []
        if r.pct_counts_mt > 2 * tab.pct_counts_mt.median(): verdict.append('low-quality')
        if r.predicted_doublet > 2 * tab.predicted_doublet.median(): verdict.append('doublet')
        if r.batch_purity > 0.9: verdict.append('batch/technical')
        print(f'  cluster {s}: n={int(r.n)}, triage flags {verdict or ["none -> novel candidate"]}; '
              f'TRUTH doublet {100*r.TRUE_doublet_frac:.1f}%, low-quality {100*r.TRUE_lowq_frac:.1f}%')
else:
    print('  the Skill\'s conf_score < 0.5 screen selected NO cluster.')
    worst = tab.sort_values('median_conf').index[0]
    r = tab.loc[worst]
    print(f'  lowest-confidence cluster is {worst}: median conf {r.median_conf:.3f}, n={int(r.n)}, '
          f'TRUTH doublet {100*r.TRUE_doublet_frac:.1f}%, low-quality {100*r.TRUE_lowq_frac:.1f}%')
    hi = tab.sort_values('TRUE_doublet_frac', ascending=False).index[0]
    r2 = tab.loc[hi]
    print(f'  the MOST doublet-enriched cluster is {hi}: TRUTH doublet '
          f'{100*r2.TRUE_doublet_frac:.1f}%, median conf {r2.median_conf:.3f}, '
          f'scrublet rate {r2.predicted_doublet:.3f}, mito {r2.pct_counts_mt:.2f}%')
    hq = tab.sort_values('TRUE_lowq_frac', ascending=False).index[0]
    r3 = tab.loc[hq]
    print(f'  the MOST low-quality cluster is {hq}: TRUTH low-quality '
          f'{100*r3.TRUE_lowq_frac:.1f}%, median conf {r3.median_conf:.3f}, '
          f'mito {r3.pct_counts_mt:.2f}% vs dataset median {tab.pct_counts_mt.median():.2f}%')
print('DONE')
