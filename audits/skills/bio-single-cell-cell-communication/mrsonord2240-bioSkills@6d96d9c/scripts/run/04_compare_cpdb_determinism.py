"""Re-auditor determinism check: compare the full pvalues and significant_means matrices from
the two independent, freshly-run debug_seed=1337 CellPhoneDB calls above -- not a spot check,
the entire result set.
"""
import pandas as pd
import numpy as np

p1 = pd.read_csv('run/reaudit_cpdb_pvalues_run1.csv')
p2 = pd.read_csv('run/reaudit_cpdb_pvalues_run2.csv')

print('pvalues shapes', p1.shape, p2.shape)
print('pvalues columns identical:', list(p1.columns) == list(p2.columns))

meta_cols = [c for c in p1.columns if c in ('id_cp_interaction','interacting_pair','partner_a','partner_b',
             'gene_a','gene_b','secreted','receptor_a','receptor_b','annotation_strategy','is_integrin',
             'directionality','classification')]
num_cols = [c for c in p1.columns if c not in meta_cols]

print('n numeric (cell-pair) columns:', len(num_cols))

# Row order / identity
rows_match = p1[meta_cols].equals(p2[meta_cols]) if meta_cols else True
print('row metadata identical order:', rows_match)

arr1 = p1[num_cols].to_numpy(dtype=float)
arr2 = p2[num_cols].to_numpy(dtype=float)

exact_equal = np.array_equal(arr1, arr2)
print('FULL_PVALUE_MATRIX_BIT_IDENTICAL:', exact_equal)

if not exact_equal:
    diff_mask = arr1 != arr2
    n_diff = diff_mask.sum()
    print('n_differing_cells', n_diff, 'of', arr1.size)
    max_diff = np.nanmax(np.abs(arr1 - arr2))
    print('max_abs_diff', max_diff)

# significance flags at p<0.05, across the FULL matrix (not just marginal calls)
sig1 = (arr1 < 0.05)
sig2 = (arr2 < 0.05)
flips = (sig1 != sig2).sum()
print('SIGNIFICANCE_FLAGS_TOTAL:', sig1.size)
print('SIGNIFICANCE_FLAGS_FLIPPED:', flips)

# significant_means file too
sm1 = pd.read_csv('run/reaudit_cpdb_sigmeans_run1.csv')
sm2 = pd.read_csv('run/reaudit_cpdb_sigmeans_run2.csv')
sm_num_cols = [c for c in sm1.columns if c not in meta_cols]
a1 = sm1[sm_num_cols].to_numpy(dtype=float)
a2 = sm2[sm_num_cols].to_numpy(dtype=float)
print('sigmeans shapes', sm1.shape, sm2.shape)
print('SIGMEANS_BIT_IDENTICAL (NaN-aware):', (np.array_equal(a1, a2) or (np.isnan(a1) == np.isnan(a2)).all() and np.allclose(np.nan_to_num(a1), np.nan_to_num(a2))))
