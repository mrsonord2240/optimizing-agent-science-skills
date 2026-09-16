"""Input 2 (Variant A) - bio-single-cell-doublet-detection
The scanpy route exactly as SKILL.md:95-105 prescribes: sc.pp.scrublet on raw counts, per sample,
expected_doublet_rate set from recovered cells with the Skill's 0.008 x n/1000 rule (NOT the 0.05
placeholder). Scored against the SYNTHETIC ground-truth doublet labels.
"""
import scanpy as sc
import numpy as np
import pandas as pd

D = r'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
a = sc.read_h5ad(D + '/all_samples_filtered.h5ad')
tc = pd.read_csv(D + '/truth_cells.csv').set_index('cell_id').loc[a.obs_names]
truth = tc['true_doublet'].values.astype(bool)
print('scanpy', sc.__version__, '| cells', a.n_obs, '| true doublets', int(truth.sum()))


def prf(pred, truth, name):
    tp = int((pred & truth).sum()); fp = int((pred & ~truth).sum()); fn = int((~pred & truth).sum())
    print(f'  {name}: called {int(pred.sum())} ({100*pred.mean():.2f}%) TP={tp} FP={fp} FN={fn} '
          f'recall={tp/max(tp+fn,1):.3f} precision={tp/max(tp+fp,1):.3f}')


def auc(score, truth):
    r = pd.Series(score).rank().values
    n1, n0 = truth.sum(), (~truth).sum()
    return (r[truth].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)


# --- route A: the Skill's per-sample loop, rate from that lane's recovered cells ---
score = np.zeros(a.n_obs); pred = np.zeros(a.n_obs, dtype=bool)
for s in sorted(a.obs['sample'].unique()):
    m = (a.obs['sample'] == s).values
    sub = a[m].copy()
    expected_rate = 0.008 * sub.n_obs / 1000
    sc.pp.scrublet(sub, expected_doublet_rate=expected_rate, random_state=0)
    score[m] = sub.obs['doublet_score'].values
    pred[m] = sub.obs['predicted_doublet'].values.astype(bool)
    thr = sub.uns['scrublet']['threshold'] if 'threshold' in sub.uns['scrublet'] else None
    print(f'  {s}: n={sub.n_obs} expected_rate={expected_rate:.4f} threshold={thr} '
          f'called={int(sub.obs["predicted_doublet"].sum())} true={int(truth[m].sum())}')
print('PER-SAMPLE loop, rate from recovered cells (the Skill\'s rule):')
prf(pred, truth, 'scrublet per-sample')
print(f'  AUC = {auc(score, truth):.4f}')

# --- route B: the same loop but with Scrublet's 0.05 placeholder the Skill warns against ---
pred05 = np.zeros(a.n_obs, dtype=bool)
for s in sorted(a.obs['sample'].unique()):
    m = (a.obs['sample'] == s).values
    sub = a[m].copy()
    sc.pp.scrublet(sub, expected_doublet_rate=0.05, random_state=0)
    pred05[m] = sub.obs['predicted_doublet'].values.astype(bool)
print('PER-SAMPLE loop with the 0.05 placeholder the Skill warns against:')
prf(pred05, truth, 'scrublet 0.05')

# --- route C: batch_key, the alternative the Skill offers in the same sentence ---
b = a.copy()
try:
    sc.pp.scrublet(b, batch_key='sample', expected_doublet_rate=0.008 * (a.n_obs / 8) / 1000,
                   random_state=0)
    predb = b.obs['predicted_doublet'].values.astype(bool)
    print('batch_key route (SKILL.md:105 "or pass batch_key"):')
    prf(predb, truth, 'scrublet batch_key')
    print(f'  agrees with the explicit loop on {int((predb == pred).sum())}/{a.n_obs} cells')
except Exception as e:
    print('batch_key route FAILED:', type(e).__name__, str(e)[:200])

# --- route D: the documented mistake - one call on the merged object ---
c = a.copy()
sc.pp.scrublet(c, expected_doublet_rate=0.008 * a.n_obs / 1000, random_state=0)
print('MERGED object, single call (the Skill\'s Common Errors row 1):')
prf(c.obs['predicted_doublet'].values.astype(bool), truth, 'scrublet merged')

# --- determinism of the prescribed call ---
d1 = a[a.obs['sample'] == 'S1'].copy(); sc.pp.scrublet(d1, expected_doublet_rate=0.006)
d2 = a[a.obs['sample'] == 'S1'].copy(); sc.pp.scrublet(d2, expected_doublet_rate=0.006)
print('no random_state, two runs on S1 agree on '
      f'{int((d1.obs["predicted_doublet"].values == d2.obs["predicted_doublet"].values).sum())}/{d1.n_obs} cells')
print('DONE')
