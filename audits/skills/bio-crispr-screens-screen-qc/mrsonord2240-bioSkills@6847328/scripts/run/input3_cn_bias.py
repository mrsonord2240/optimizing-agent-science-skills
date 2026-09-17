"""Input 3 -- Variant B (regression + extended). Two-rule CN-bias diagnostic on the audit's
own synthetic 40-gene focal amplicon (same data as the pre-fix audit's Input 3): confirms the
new amplified-vs-diploid gap rule catches what the genome-wide Spearman rho rule alone missed,
AND (independent negative control, not copied from the fixer's own verify_qc.py -- re-derived
here with a different seed) that shuffling the copy-number labels makes the artifact disappear."""
import sys
import pandas as pd, numpy as np
sys.path.insert(0, '.')
import qc_functions as qc

D = r'F:\OpenScience\audits\bio-crispr-screens-screen-qc\data'
lfc = pd.read_csv(D + r'\synthetic_gene_lfc_for_cn.txt', sep='\t')
cn = pd.read_csv(D + r'\synthetic_copy_number.txt', sep='\t')

print('=== Positive case: real (synthetic, labeled) 40-gene focal amplicon ===')
r = qc.cn_bias_diagnostic(lfc, cn)
for k, v in r.items():
    if k == 'per_bin':
        continue
    print(f'  {k}: {round(v, 4) if isinstance(v, float) else v}')
print('  Rule 1 (genome-wide rho < -0.10 and p<0.01) alone:',
      bool(r['cn_vs_lfc_rho'] < -0.1 and r['cn_vs_lfc_p'] < 0.01))
print('  Rule 2 (gap < -0.5 and p_gap<0.01) alone:',
      bool(r['amplified_vs_diploid_gap'] < -0.5 and r['p_amplified_more_depleted'] < 0.01))
print('  cn_bias_present (either rule):', r['cn_bias_present'])
assert r['cn_bias_present'], 'FIX REGRESSION: two-rule diagnostic no longer catches the focal amplicon'
assert not (r['cn_vs_lfc_rho'] < -0.1 and r['cn_vs_lfc_p'] < 0.01), 'rho rule unexpectedly also fires -- amplicon is no longer a good rho-blind-spot test case'

print('\n=== Negative control: copy-number labels shuffled (own seed, independent of fixer) ===')
rng = np.random.default_rng(2026)
cn_shuffled = cn.copy()
cn_shuffled['copy_number'] = rng.permutation(cn_shuffled['copy_number'].values)
r2 = qc.cn_bias_diagnostic(lfc, cn_shuffled)
for k, v in r2.items():
    if k == 'per_bin':
        continue
    print(f'  {k}: {round(v, 4) if isinstance(v, float) else v}')
print('  cn_bias_present (should be False):', r2['cn_bias_present'])
assert not r2['cn_bias_present'], 'FALSE POSITIVE: shuffled CN labels still flagged as bias'

print('\nCN two-rule diagnostic: positive case caught, negative control silent. PASS')
