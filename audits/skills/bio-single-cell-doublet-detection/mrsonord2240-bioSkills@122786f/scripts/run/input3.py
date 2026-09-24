"""Input 3 (Edge) - bio-single-cell-doublet-detection
A near-homogeneous sort: the case the Skill's Common Errors row 2 names -
"Auto-threshold splits the histogram badly / Scrublet histogram is unimodal /
 Inspect the histogram and set threshold manually".

Derived SYNTHETIC data: ../data/sorted_cd4.h5ad - 900 cells drawn from the CD4 T-cell compartment
of the synthetic 8-sample PBMC set (one cell type only, so heterotypic doublets are rare and the
simulated-doublet score distribution should be unimodal), with the true doublets that happen to be
CD4-CD4 kept as labels.
"""
import scanpy as sc
import numpy as np
import pandas as pd

D = r'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
DATA = r'F:/OpenScience/audits/bio-single-cell-doublet-detection/data'
rng = np.random.default_rng(20260916)

a = sc.read_h5ad(D + '/all_samples_filtered.h5ad')
tc = pd.read_csv(D + '/truth_cells.csv').set_index('cell_id').loc[a.obs_names]
a.obs['true_doublet'] = tc['true_doublet'].values.astype(bool)
a.obs['true_cell_type'] = tc['true_cell_type'].values
sub = a[a.obs['true_cell_type'] == 'CD4 T cells'].copy()
sub = sub[rng.choice(sub.n_obs, 900, replace=False)].copy()
sub.write_h5ad(DATA + '/sorted_cd4.h5ad')
print(f'Sorted CD4 set: {sub.n_obs} cells, true doublets in it: {int(sub.obs["true_doublet"].sum())}')

expected_rate = 0.008 * sub.n_obs / 1000
print(f'Skill rate rule -> expected_doublet_rate = {expected_rate:.4f}')
sc.pp.scrublet(sub, expected_doublet_rate=expected_rate, random_state=0)
u = sub.uns['scrublet']
print('scrublet uns keys:', sorted(u.keys()))
thr = u.get('threshold')
print(f'auto threshold = {thr}; called {int(sub.obs["predicted_doublet"].sum())} doublets')

sim = np.asarray(u['doublet_scores_sim'])
obs = sub.obs['doublet_score'].values
print(f'simulated-doublet scores: n={len(sim)} min={sim.min():.4f} med={np.median(sim):.4f} max={sim.max():.4f}')
print(f'observed scores:          n={len(obs)} min={obs.min():.4f} med={np.median(obs):.4f} max={obs.max():.4f}')


def modality(x, bins=40):
    """crude bimodality check: count interior local maxima of a smoothed histogram"""
    h, _ = np.histogram(x, bins=bins)
    h = np.convolve(h, np.ones(3) / 3, mode='same')
    return int(sum(1 for i in range(1, len(h) - 1) if h[i] > h[i - 1] and h[i] > h[i + 1] and h[i] > 0.05 * h.max()))


print(f'simulated-score histogram local maxima = {modality(sim)}  '
      f'(1 => unimodal => the Skill\'s documented auto-threshold failure case)')

# the Skill's prescribed fix: inspect and set the threshold manually.
# The only principled manual anchor the Skill offers is the expected rate, so use it.
k = max(1, int(round(expected_rate * sub.n_obs)))
manual_thr = np.sort(obs)[-k]
manual_pred = obs >= manual_thr
truth = sub.obs['true_doublet'].values
for nm, p in [('auto threshold', sub.obs['predicted_doublet'].values.astype(bool)),
              ('manual threshold from the rate rule', manual_pred)]:
    tp = int((p & truth).sum()); fp = int((p & ~truth).sum()); fn = int((~p & truth).sum())
    print(f'  {nm}: called {int(p.sum())} TP={tp} FP={fp} FN={fn} '
          f'recall={tp/max(tp+fn,1):.3f} precision={tp/max(tp+fp,1):.3f}')

print('\nhomotypic check (Governing Principle / Common Errors "Reported 0% doublets"):')
print(f'  of the {int(truth.sum())} true doublets in this sorted population, '
      f'{int((sub.obs["doublet_score"].values[truth] > np.median(obs)).sum())} score above the median '
      f'observed score - i.e. most CD4-CD4 homotypic doublets are not separable, as the Skill states.')
print('DONE')
