'''
Input 6 (Scope Boundary) -- "My BAGEL2 Bayes Factors keep changing between reruns on the
exact same input data -- 33 genes flip across the BF>6 essential/non-essential threshold.
Which run do I trust for hit calling, and how should I report this?"

This sits squarely inside the Skill's own stated scope ("...or interpreting unstable hit
lists across reruns" -- SKILL.md frontmatter description) and is a REAL, already-verified
defect: the bagel-essentiality audit ran `BAGEL.py bf` twice on identical input with no
-s/--seed flag (matching every example in that Skill) and found BF differences up to 26.7
and 33 threshold-flips (bagel-essentiality audit, P0 "BAGEL2 results are non-deterministic
and the Skill never says so"). Both real runs are reused here unmodified.

Tests whether bio-crispr-screens-hit-calling -- whose whole job is cross-method
reconciliation and whose description explicitly claims to cover this exact scenario --
gives an agent any actual guidance for it, or is silent.
'''
import pandas as pd

run1 = pd.read_csv('bayes_factor.txt', sep='\t').rename(columns={'BF': 'BF_run1'})
run2 = pd.read_csv('bayes_factor_rep2.txt', sep='\t').rename(columns={'BF': 'BF_run2'})
merged = run1.merge(run2, on='GENE')
merged['diff'] = (merged['BF_run1'] - merged['BF_run2']).abs()
merged['flips_bf6'] = (merged['BF_run1'] > 6) != (merged['BF_run2'] > 6)

print(f'Genes compared: {len(merged)}')
print(f'Max |BF_run1 - BF_run2|: {merged["diff"].max():.2f}')
print(f'Mean |diff|: {merged["diff"].mean():.3f}')
n_flips = int(merged['flips_bf6'].sum())
print(f'Genes flipping across BF>6 threshold between identical reruns: {n_flips}')
print()
print('Sample of flipping genes:')
print(merged[merged['flips_bf6']][['GENE', 'BF_run1', 'BF_run2']].head(10).to_string(index=False))
print()
print('--- What bio-crispr-screens-hit-calling SKILL.md actually says about this scenario ---')
print('SKILL.md frontmatter description explicitly claims coverage of')
print('  "...interpreting unstable hit lists across reruns."')
print('Grep of SKILL.md + usage-guide.md for BAGEL2 seed/determinism guidance: NO MATCH.')
print('The Reconciliation table (SKILL.md "Reconciliation: When Two Methods Disagree") only')
print('covers disagreement BETWEEN methods (MAGeCK vs BAGEL2, Chronos vs MAGeCK, etc.) --')
print('there is no row for disagreement between two runs of the SAME method on the SAME data.')
print('The Failure Modes section likewise has no entry for BAGEL2 run-to-run instability.')
print('An agent following only this Skill would have no way to know a fixed -s seed exists,')
print('or that BAGEL2\'s default is non-deterministic at all -- despite the Skill\'s own')
print('description explicitly promising to help interpret exactly this situation.')
