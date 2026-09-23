'''Input 5 (Stress, regression of pre-fix Input 5): "Run MAGeCK + BAGEL2 + drugZ on
what the requester believes is 'the same screen' and build a 3-method consensus" --
but the drugZ table is actually from an unrelated drug-response comparison on the
same library. Pre-fix, this silently produced an empty Tier-1 list with no warning
(a documented P1). Post-fix, the SKILL.md inline consensus_hits() calls the new
_check_comparable() helper. Verify the warning actually fires on this real
mismatched pair -- this is the sensitivity half of the comparability-check test
(input9_comparability_specificity.py is the specificity half).
'''
import os, sys
import pandas as pd

RUN = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RUN)
os.chdir(RUN)
from lib_consensus_inline import consensus_hits

import io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    merged = consensus_hits('mageck_hap1.gene_summary.txt', 'bayes_factor.txt', 'drugz_drug_output.txt')
stdout = buf.getvalue()
print(stdout)

print(f'Merged genes: {len(merged)}')
print(f'MAGeCK hits (FDR<0.05): {int(merged["mageck_hit"].sum())}')
print(f'BAGEL2 hits (BF>6): {int(merged["bagel_hit"].sum())}')
print(f'drugZ hits (FDR<0.05): {int(merged["drugz_hit"].sum())}')
n_tier1 = int((merged['consensus_count'] == 3).sum())
n_tier2 = int((merged['consensus_count'] == 2).sum())
print(f'Tier 1 (3/3): {n_tier1}')
print(f'Tier 2 (2/3): {n_tier2}')

# Cross-check against the real drugZ planted ground truth -- these mageck/bagel hits
# should NOT overlap the drug-response planted hits, confirming this is a genuine
# mismatched-comparison scenario, not coincidental biology.
gt_lines = [l.strip().split('\t') for l in open('drugz_ground_truth.txt') if l.strip()]
gt_genes = set()
for row in gt_lines:
    if len(row) > 1:
        gt_genes.update(g.strip() for g in row[1].split(','))
mageck_bagel_agree = set(merged[(merged['mageck_hit']) & (merged['bagel_hit'])]['gene'])
overlap_with_planted_drug_hits = mageck_bagel_agree & gt_genes
print(f'\nMAGeCK+BAGEL2 essentiality-agreement genes: {len(mageck_bagel_agree)}')
print(f'Planted drugZ ground-truth genes: {sorted(gt_genes)}')
print(f'Overlap between the two (expected near-zero -- different questions): {sorted(overlap_with_planted_drug_hits)}')

assert 'WARNING' in stdout, (
    'REGRESSION: _check_comparable() did not fire on a genuinely mismatched '
    'essentiality-vs-drug-response pair -- the P1 fix is not working')
assert 'drugz_hit' in stdout or 'mageck_hit vs drugz_hit' in stdout or 'bagel_hit vs drugz_hit' in stdout, (
    'expected the warning to name the drugz column specifically')
print('\nPASS: comparability check correctly flags the mismatched drugZ pairing.')
