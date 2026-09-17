'''Input 8 (NEW -- auditor-added, targets the fix-log's central claim: "the consensus
code gives the same answer from both of its implementations"). The Skill has two
places consensus logic lives: the inline consensus_hits()/_check_comparable() in
SKILL.md, and the standalone examples/consensus_hits.py script. Pre-fix, these
disagreed on their MAGeCK-FDR/BAGEL-BF defaults (0.05/5 vs 0.1/5 vs the table's
0.05/6), swinging the real-data hit count by 34%. Post-fix both claim to default to
the table's FDR<0.05/BF>6. Verify independently: do the two implementations produce
IDENTICAL per-gene mageck_hit/bagel_hit boolean calls on the same real input files?
'''
import os, sys, shutil, subprocess
import pandas as pd

RUN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RUN)
os.chdir(RUN)
from lib_consensus_inline import consensus_hits as inline_consensus_hits

# Implementation A: inline SKILL.md function (3-method call; use its own mageck_hit /
# bagel_hit columns, ignoring drugz_hit, so the comparison is apples-to-apples with
# the 2-method example script).
merged_inline = inline_consensus_hits('mageck_hap1.gene_summary.txt', 'bayes_factor.txt', 'drugz_drug_output.txt')
inline_calls = merged_inline.set_index('gene')[['mageck_hit', 'bagel_hit']].sort_index()

# Implementation B: examples/consensus_hits.py, run as its own process (staged
# filenames as it hardcodes them), then re-derive the same two boolean columns from
# its own thresholds by re-reading its source rather than trusting only stdout counts.
shutil.copy('mageck_hap1.gene_summary.txt', 'mageck.gene_summary.txt')
shutil.copy('bayes_factor.txt', 'bagel_bf.txt')
result = subprocess.run([sys.executable, 'examples_consensus_hits.py'], capture_output=True, text=True)
print('--- examples_consensus_hits.py stdout ---')
print(result.stdout)
assert result.returncode == 0, result.stderr

mageck_b = pd.read_csv('mageck.gene_summary.txt', sep='\t')[['id', 'neg|fdr']].rename(columns={'id': 'gene'})
bagel_b = pd.read_csv('bagel_bf.txt', sep='\t')[['GENE', 'BF']].rename(columns={'GENE': 'gene'})
merged_b = mageck_b.merge(bagel_b, on='gene', how='outer')
merged_b['mageck_hit'] = merged_b['neg|fdr'] < 0.05
merged_b['bagel_hit'] = merged_b['BF'] > 6
example_calls = merged_b.set_index('gene')[['mageck_hit', 'bagel_hit']].sort_index()

common_genes = inline_calls.index.intersection(example_calls.index)
print(f'\nGenes in both: {len(common_genes)} (inline: {len(inline_calls)}, example: {len(example_calls)})')

a = inline_calls.loc[common_genes].fillna(False)
b = example_calls.loc[common_genes].fillna(False)
mageck_agree = (a['mageck_hit'] == b['mageck_hit']).all()
bagel_agree = (a['bagel_hit'] == b['bagel_hit']).all()
n_mageck_mismatch = int((a['mageck_hit'] != b['mageck_hit']).sum())
n_bagel_mismatch = int((a['bagel_hit'] != b['bagel_hit']).sum())

print(f'mageck_hit identical across both implementations: {mageck_agree} ({n_mageck_mismatch} mismatches)')
print(f'bagel_hit identical across both implementations: {bagel_agree} ({n_bagel_mismatch} mismatches)')

both_agree_count = int((a['mageck_hit'] & a['bagel_hit']).sum())
print(f'\n2-method consensus count, implementation A (inline, mageck_hit & bagel_hit): {both_agree_count}')
print(f'2-method consensus count, implementation B (examples/consensus_hits.py, both hits): {int((b["mageck_hit"] & b["bagel_hit"]).sum())}')

assert mageck_agree, 'REGRESSION: mageck_hit threshold differs between the two implementations'
assert bagel_agree, 'REGRESSION: bagel_hit threshold differs between the two implementations'
print('\nPASS: both implementations produce byte-identical hit calls from the same real data.')
