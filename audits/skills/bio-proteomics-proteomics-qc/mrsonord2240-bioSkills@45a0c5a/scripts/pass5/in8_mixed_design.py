# Pass-5 confirmation audit, Input 8 (NEW this pass).
# Researcher request: "We have four runs: two controls, one treated, one treated+drug. Run your full QC
# and tell me what you can and cannot conclude."
#
# This is the PARTIALLY degenerate design the fix log did not test: the fixer verified the all-singleton
# case (one run per condition). Here one group has 2 samples and two groups have 1 each, so every guard
# has to choose between raising, warning and computing.
import io, contextlib
import numpy as np, pandas as pd
from skill import S

D = '../data/'
pg = pd.read_csv(D + 'proteinGroups.txt', sep='\t', low_memory=False)
clean = S['strip_contaminant_rows'](pg)

# 4 of the 8 synthetic samples, relabelled into a 2 / 1 / 1 design (SYNTHETIC data, data/proteinGroups.txt)
cols = ['C1', 'C2', 'T1', 'T2']
groups = pd.Series(['Control', 'Control', 'Treated', 'Treated_drug'], index=cols)
raw = clean[[f'Intensity {s}' for s in cols]].replace(0, np.nan)
raw.columns = cols
lfq = clean[[f'LFQ intensity {s}' for s in cols]].replace(0, np.nan)
lfq.columns = cols
log2 = np.log2(lfq)
print('design:', groups.value_counts().to_dict())

print('\n--- raw_sample_qc (should warn about the two singleton groups and fall back) ---')
qc = S['raw_sample_qc'](raw, groups)
print(qc[['n_quantified', 'baseline', 'fold_total_vs_group', 'ids_vs_group', 'flag']].round(3).to_string())

print('\n--- replicate_correlation (one group HAS 2 samples, so it must NOT raise) ---')
try:
    rc = S['replicate_correlation'](log2, groups)
    print(rc.to_string(index=False))
except Exception as e:
    print(f'  {type(e).__name__}: {e}')

print('\n--- median_cv_linear (same: must compute Control, and say the singletons are NaN) ---')
try:
    cv = S['median_cv_linear'](lfq, groups)
    print(cv.to_string(index=False))
except Exception as e:
    print(f'  {type(e).__name__}: {e}')

print('\n--- pca_batch_check with batch_col=condition, level sizes 2/1/1 ---')
info = pd.DataFrame({'condition': groups.values, 'batch': groups.values}, index=cols)
filt = log2.dropna(how='any')
try:
    coords, var = S['pca_batch_check'](filt, info, batch_col='batch')
    print('  explained:', np.round(var, 3))
except Exception as e:
    print(f'  {type(e).__name__}: {e}')

print('\n--- what a reader is left with ---')
print('  Control CV/r are real; Treated and Treated_drug have NO within-group evidence at all.')
