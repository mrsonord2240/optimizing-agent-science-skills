'''Input 9 (NEW -- auditor-added, specificity half of the comparability-check test).
Input 5 already showed _check_comparable() correctly fires (a true positive) on a
genuinely mismatched essentiality-vs-drug-response pair. A check that always fires
would be useless -- this input tests the complementary false-positive risk: does it
stay silent on two genuinely MATCHED comparisons?

Uses BAGEL2 rep1 vs rep2 (bayes_factor.txt vs bayes_factor_rep2.txt) -- two identical
reruns of the SAME comparison (same screen, same design, just an unseeded rerun).
These are about as "comparable" as two files can be; the hit-set overlap should be
massively enriched and the check must NOT warn.
'''
import os, sys, io, contextlib
import pandas as pd

RUN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RUN)
os.chdir(RUN)
from lib_consensus_inline import _check_comparable

rep1 = pd.read_csv('bayes_factor.txt', sep='\t').rename(columns={'BF': 'BF_rep1'})
rep2 = pd.read_csv('bayes_factor_rep2.txt', sep='\t').rename(columns={'BF': 'BF_rep2'})
merged = rep1.merge(rep2, on='GENE', how='inner')
merged['hit_rep1'] = merged['BF_rep1'] > 6
merged['hit_rep2'] = merged['BF_rep2'] > 6

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    warnings = _check_comparable(merged, ['hit_rep1', 'hit_rep2'])
stdout = buf.getvalue()
print(stdout if stdout else '(no warning printed)')

n1, n2 = int(merged['hit_rep1'].sum()), int(merged['hit_rep2'].sum())
n_overlap = int((merged['hit_rep1'] & merged['hit_rep2']).sum())
print(f'rep1 hits: {n1}, rep2 hits: {n2}, overlap: {n_overlap}')

assert len(warnings) == 0, (
    f'FALSE POSITIVE: _check_comparable() fired on two genuinely matched BAGEL2 '
    f'reruns of the SAME comparison -- {warnings}')
print('\nPASS: no false-positive warning on a genuinely matched (same-comparison) pair.')

# Second matched case, independent of BAGEL2 rep1/rep2: real MAGeCK vs real BAGEL2 on
# the SAME HAP1 TKOv3 comparison (used end-to-end in Input 1) -- confirm directly here
# too rather than only inferring it from Input 1's absence of a WARNING line.
mageck = pd.read_csv('mageck_hap1.gene_summary.txt', sep='\t')[['id', 'neg|fdr']].rename(columns={'id': 'gene'})
bagel = pd.read_csv('bayes_factor.txt', sep='\t').rename(columns={'GENE': 'gene', 'BF': 'BF'})
merged2 = mageck.merge(bagel, on='gene', how='outer')
merged2['mageck_hit'] = merged2['neg|fdr'] < 0.05
merged2['bagel_hit'] = merged2['BF'] > 6

buf2 = io.StringIO()
with contextlib.redirect_stdout(buf2):
    warnings2 = _check_comparable(merged2, ['mageck_hit', 'bagel_hit'])
print(buf2.getvalue() if buf2.getvalue() else '(no warning printed)')
assert len(warnings2) == 0, (
    f'FALSE POSITIVE: _check_comparable() fired on real matched MAGeCK+BAGEL2 pair -- {warnings2}')
print('PASS: no false-positive warning on the real matched MAGeCK+BAGEL2 pair either.')
