# Re-audit 2026-09-15, Input 5 (Stress, regression). Batch-dominated PCA + T4 exclusion decision + sensitivity.
# SKILL.md functions verbatim on proteinGroups_failed.txt; writes matrices for in5_limma.R.
import os
import numpy as np, pandas as pd
from skill import S
D = '../data/'; os.makedirs('out_in5', exist_ok=True)
info = pd.read_csv(D + 'sample_annotation.csv').set_index('sample'); grp = info['condition']; S8 = info.index.tolist()
pg = S['strip_contaminant_rows'](pd.read_csv(D + 'proteinGroups_failed.txt', sep='\t', low_memory=False))
raw = pg[[f'Intensity {s}' for s in S8]]; raw.columns = S8
q = S['raw_sample_qc'](raw, grp)
print('raw_sample_qc flags:', q.index[q.flag].tolist(), '| T4 total', round(q.loc['T4', 'fold_total_vs_group'], 3), 'IDs', round(q.loc['T4', 'ids_vs_group'], 3), 'missing', round(q.loc['T4', 'missing_pct'], 1))
lfq = pg[[f'LFQ intensity {s}' for s in S8]].replace(0, np.nan); lfq.columns = S8
lfq.index = pg['Protein IDs'].str.split(';').str[0]
log2 = np.log2(lfq)
filt = S['completeness_filter'](log2, grp, 0.7); filt.to_csv('out_in5/log2_lfq_failed_filtered.csv')
print('\n[all 8]'); c8, e8 = S['pca_batch_check'](filt, info); print('  explained', np.round(e8, 3))
for s in S8:
    same = [x for x in S8 if grp[x] == grp[s] and x != s]
    print(f'  {s}: distance to own-group centroid (PC1-3) {np.linalg.norm(c8.loc[s, ["PC1","PC2","PC3"]] - c8.loc[same, ["PC1","PC2","PC3"]].mean()):.1f}')
keep = [s for s in S8 if s != 'T4']
print('\n[T4 excluded]'); c7, e7 = S['pca_batch_check'](S['completeness_filter'](log2[keep], grp[keep], 0.7), info.loc[keep]); print('  explained', np.round(e7, 3))
bc = filt.copy()
for b in info.batch.unique():
    cols = info.index[info.batch == b]; bc[cols] = bc[cols].sub(bc[cols].mean(axis=1), axis=0)
print('\n[batch-centred, plots only]'); cb, _ = S['pca_batch_check'](bc, info)
from scipy.stats import f_oneway
print('  PC1 ~ condition p=%.4f' % f_oneway(*[cb.loc[cb.condition == k, 'PC1'] for k in ['Control', 'Treatment']])[1])
pil = ['C1', 'C3', 'T1', 'T3']
print('\n[2 vs 2 pilot]')
try:
    cp, ep = S['pca_batch_check'](filt[pil], info.loc[pil]); print('  ran, n_components', len(ep))
except Exception as e:
    print('  ', type(e).__name__, e)
