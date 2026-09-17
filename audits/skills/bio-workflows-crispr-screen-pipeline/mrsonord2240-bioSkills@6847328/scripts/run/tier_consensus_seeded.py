# Regression test: Step 7's tier-consensus code (unmodified) against the FIXED pipeline's
# real MAGeCK RRA (essentiality_rra.gene_summary.txt, reused from the pre-fix run, unaffected
# by the fix) + the newly-seeded BAGEL2 output (bayes_factor_seeded_run1.txt) + drugZ
# (drugz_output.txt, reused, Step 6c text unchanged by the fix).
import pandas as pd

mageck = pd.read_csv('essentiality_rra.gene_summary.txt', sep='\t')[['id', 'neg|fdr']].rename(
    columns={'id': 'gene', 'neg|fdr': 'mageck_neg_fdr'})
bagel = pd.read_csv('bayes_factor_seeded_run1.txt', sep='\t')[['GENE', 'BF']].rename(
    columns={'GENE': 'gene', 'BF': 'bagel_bf'})
drugz_df = pd.read_csv('drugz_output.txt', sep='\t')[['GENE', 'fdr_synth']].rename(
    columns={'GENE': 'gene', 'fdr_synth': 'drugz_synth_fdr'})

merged = mageck.merge(bagel, on='gene', how='outer').merge(drugz_df, on='gene', how='outer')
merged['mageck_hit'] = merged['mageck_neg_fdr'] < 0.05
merged['bagel_hit'] = merged['bagel_bf'] > 6
merged['drugz_hit'] = merged['drugz_synth_fdr'] < 0.05
merged['tier'] = merged[['mageck_hit', 'bagel_hit', 'drugz_hit']].astype(int).sum(axis=1)
merged.to_csv('tier_consensus_seeded.csv', index=False)
print('Total merged:', len(merged))
print('Tier1 (3/3):', (merged['tier'] >= 3).sum())
print('Tier2 (2/3):', (merged['tier'] == 2).sum())
