"""Input 5 (Stress): batch-dominated PCA + T4 exclusion decision with sensitivity check (proteinGroups_failed.txt).
Mode A following SKILL.md: raw inspection -> contaminant strip -> log2 LFQ -> completeness -> pca_batch_check,
with and without T4; batch-removed view for PCA only. Writes the matrix used by in5_limma_sensitivity.R.
Data: SYNTHETIC. Audit 2026-09-11."""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from skill_funcs import *

D = os.path.join(os.path.dirname(__file__), '..', 'data')
OUT = os.path.join(os.path.dirname(__file__), 'out_in5'); os.makedirs(OUT, exist_ok=True)
info = pd.read_csv(os.path.join(D, 'sample_annotation.csv')).set_index('sample')
S = info.index.tolist(); grp = info['condition']
pg = strip_contaminant_rows(pd.read_csv(os.path.join(D, 'proteinGroups_failed.txt'), sep='\t', low_memory=False))
lfq = pg[[f'LFQ intensity {s}' for s in S]].replace(0, np.nan); lfq.columns = S
lfq.index = pg['Protein IDs'].str.split(';').str[0]
log2 = np.log2(lfq)
filt = completeness_filter(log2, grp, 0.7)
print('matrix after completeness_filter:', filt.shape)
filt.to_csv(os.path.join(OUT, 'log2_lfq_failed_filtered.csv'))

print('\n[all 8] pca_batch_check:')
c8, e8 = pca_batch_check(filt, info)
print('  explained', np.round(e8, 3))
print(c8[['PC1', 'PC2', 'PC3', 'condition', 'batch']].round(2).to_string())

keep = [s for s in S if s != 'T4']
f7 = completeness_filter(log2[keep], grp[keep], 0.7)
print('\n[T4 excluded] pca_batch_check:')
c7, e7 = pca_batch_check(f7, info.loc[keep])
print('  explained', np.round(e7, 3))

# T4 distance from its group centroid in PC space (all-8 fit) vs the other samples
for s in S:
    same = [x for x in S if grp[x] == grp[s] and x != s]
    d = np.linalg.norm(c8.loc[s, ['PC1', 'PC2', 'PC3']] - c8.loc[same, ['PC1', 'PC2', 'PC3']].mean())
    print(f'  {s}: distance to own-group centroid (PC1-3) = {d:.1f}')

# Batch-removed view for PCA only (balanced design: per-protein batch-mean centring, like limma::removeBatchEffect)
bc = filt.copy()
for b in info['batch'].unique():
    cols = info.index[info['batch'] == b]
    bc[cols] = bc[cols].sub(bc[cols].mean(axis=1), axis=0)
print('\n[batch-centred view, for plotting only] pca_batch_check:')
cb, eb = pca_batch_check(bc, info)
print('  explained', np.round(eb, 3))
from scipy.stats import f_oneway
_, p = f_oneway(*[cb.loc[cb['condition'] == k, 'PC1'] for k in ['Control', 'Treatment']])
print(f'  PC1 ~ condition p={p:.4f}')

# n_components=5 guard: what happens with the Skill's function at small n (e.g. 2 vs 2 pilot)?
try:
    pca_batch_check(filt[['C1', 'C3', 'T1', 'T3']], info.loc[['C1', 'C3', 'T1', 'T3']])
except Exception as e:
    print('\n[4-sample pilot] pca_batch_check ERROR:', type(e).__name__, str(e).splitlines()[0])
