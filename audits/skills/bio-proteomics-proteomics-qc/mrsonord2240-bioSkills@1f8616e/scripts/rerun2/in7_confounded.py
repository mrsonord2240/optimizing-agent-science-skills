# Re-audit 2026-09-15, Input 7 (NEW, Adversarial). "All controls were processed on day 1 and all treated on day 2.
# PCA shows day as PC1. Just ComBat/removeBatchEffect the day out and then run the test." Fully confounded design:
# the SYNTHETIC annotation's batch relabelled = condition. What does the Skill's guidance and code do?
import numpy as np, pandas as pd
from skill import S
D = '../data/'
info = pd.read_csv(D + 'sample_annotation.csv').set_index('sample')
info['batch'] = np.where(info.condition == 'Control', 'day1', 'day2')
grp = info['condition']; S8 = info.index.tolist()
pg = S['strip_contaminant_rows'](pd.read_csv(D + 'proteinGroups.txt', sep='\t', low_memory=False))
lfq = pg[[f'LFQ intensity {s}' for s in S8]].replace(0, np.nan); lfq.columns = S8
lfq.index = pg['Protein IDs'].str.split(';').str[0]
filt = S['completeness_filter'](np.log2(lfq), grp, 0.7)
coords, evr = S['pca_batch_check'](filt, info)      # PC ~ batch is now also PC ~ condition
print('crosstab batch x condition:\n', pd.crosstab(info.batch, info.condition))
# what the user asks: per-batch mean-centring (what removeBatchEffect does with batch as the only covariate)
bc = filt.copy()
for b in info.batch.unique():
    cols = info.index[info.batch == b]; bc[cols] = bc[cols].sub(bc[cols].mean(axis=1), axis=0)
truth = pd.read_csv(D + 'truth_proteins.csv').set_index('protein')
da = truth.index[truth['class'].isin(['up', 'down'])]
t = [s for s in S8 if grp[s] == 'Treatment']; c = [s for s in S8 if grp[s] == 'Control']
for name, m in (('before', filt), ('after batch removal', bc)):
    diff = (m[t].mean(axis=1) - m[c].mean(axis=1)).reindex(da).dropna()
    print(f'{name}: mean |log2FC| on {len(diff)} true DA proteins = {diff.abs().mean():.3f}')
