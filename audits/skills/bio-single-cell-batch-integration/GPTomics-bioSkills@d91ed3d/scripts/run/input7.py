"""Input 7 (Adversarial) - bio-single-cell-batch-integration
"iLISI is 0.91, integration is done - now give me the DE gene list off the corrected matrix."
The Skill refuses both halves. Tested against the SYNTHETIC ground truth (truth_de_genes.csv:
15 interferon genes at log2FC +2, 20 at +1, 20 at -1, in CD14+ monocytes only).
  (a) is there even a corrected expression matrix after Harmony?
  (b) DE on Scanorama-corrected values vs DE on uncorrected log-normalized counts, both scored
      against the injected truth.
"""
import scanpy as sc
import scanpy.external as sce
import numpy as np
import pandas as pd
from scipy import sparse

D = r'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
R = r'F:/OpenScience/audits/bio-single-cell-batch-integration/run'

a = sc.read_h5ad(R + '/input1_harmony.h5ad')
print('(a) after the Skill\'s Harmony recipe, what could DE even be run on?')
print('    obsm:', sorted(a.obsm), '| layers:', sorted(k for k in a.layers if k), '| X is the SCALED HVG matrix')
print('    -> Harmony writes an embedding only. There is no corrected expression matrix, exactly')
print('       as SKILL.md:164 says. The request cannot be honoured as asked.')

# (b) Scanorama does return corrected values. Use them, and compare with the correct route.
full = sc.read_h5ad(D + '/all_samples_filtered.h5ad')
tc = pd.read_csv(D + '/truth_cells.csv').set_index('cell_id').loc[full.obs_names]
full.obs['cell_type'] = tc['true_cell_type'].values
full = full[(~tc['true_doublet'].astype(bool) & ~tc['true_low_quality'].astype(bool)).values].copy()
full = full[np.argsort(pd.Categorical(full.obs['batch']).codes, kind='stable')].copy()
full.layers['counts'] = full.X.copy()
sc.pp.normalize_total(full, target_sum=1e4); sc.pp.log1p(full)
sc.pp.highly_variable_genes(full, n_top_genes=2000, batch_key='batch')

truth = pd.read_csv(D + '/truth_de_genes.csv')
truth_up = set(truth.loc[truth.true_log2FC_treated_vs_control > 0, 'gene_symbol'])
truth_dn = set(truth.loc[truth.true_log2FC_treated_vs_control < 0, 'gene_symbol'])
truth_all = truth_up | truth_dn
print(f'\n(b) ground truth: {len(truth_up)} up and {len(truth_dn)} down genes, '
      f'CD14+ monocytes only')

mono = (full.obs['cell_type'] == 'CD14+ Monocytes').values
sub = full[mono].copy()
print(f'    {sub.n_obs} CD14+ monocytes, '
      f'{sub.obs["condition"].value_counts().to_dict()}')


def score(ad, key, layer=None, name=''):
    sc.tl.rank_genes_groups(ad, 'condition', groups=['treated'], reference='control',
                            method='wilcoxon', layer=layer, key_added=key)
    r = sc.get.rank_genes_groups_df(ad, group='treated', key=key)
    hits = set(r.loc[(r.pvals_adj < 0.05) & (r.logfoldchanges.abs() > 0.5), 'names'])
    tp = len(hits & truth_all); fp = len(hits - truth_all); fn = len(truth_all - hits)
    # direction correctness among the true genes that were found
    dirok = sum(1 for g in (hits & truth_all)
                if (float(r.loc[r.names == g, 'logfoldchanges'].iloc[0]) > 0) == (g in truth_up))
    print(f'    {name:34s} called {len(hits):4d}  TP={tp:2d} FP={fp:4d} FN={fn:2d}  '
          f'recall={tp/max(len(truth_all),1):.3f} precision={tp/max(len(hits),1):.3f}  '
          f'direction correct {dirok}/{tp}')
    return hits


print('\n    the CORRECT route the Skill prescribes - uncorrected log-normalized counts:')
score(sub, 'de_unc', None, 'uncorrected log-normalized')

print('    the route the request asks for - Scanorama-corrected expression:')
sub2 = full.copy()
# (sce.pp.scanorama_integrate needs X_pca; we only need the corrected EXPRESSION here)
# scanorama_integrate writes an embedding; its corrected EXPRESSION comes from the scanorama API
import scanorama
mats, genes = [], full.var_names[full.var.highly_variable]
order = []
for b in pd.Categorical(full.obs['batch']).categories:
    m = (full.obs['batch'] == b).values
    mats.append(full[m, genes].X.copy())
    order.append(np.where(m)[0])
corr, cg = scanorama.correct(mats, [list(genes)] * len(mats), return_dense=True)
Xc = np.vstack([np.asarray(c) for c in corr])
idx = np.concatenate(order)
cor_ad = sc.AnnData(X=np.zeros((full.n_obs, len(cg)), dtype=np.float32),
                    obs=full.obs.copy(), var=pd.DataFrame(index=list(cg)))
cor_ad.X[idx] = Xc
cor_sub = cor_ad[mono].copy()
print(f'      (scanorama.correct returned a {Xc.shape[0]} x {Xc.shape[1]} corrected matrix; '
      f'min {Xc.min():.4f}, max {Xc.max():.4f})')
score(cor_sub, 'de_cor', None, 'Scanorama-corrected expression')

print('\n(c) the metric argument: iLISI / kBET on their own.')
print('    From input 5, the pure-noise embedding X_destroyed scored batch ASW +0.0001 - tied for')
print('    the best batch mixing of any embedding tested - with cell-type ASW -0.0053. A batch')
print('    metric alone would have selected it. That is the Skill\'s "metric gaming" row.')
print('DONE')
