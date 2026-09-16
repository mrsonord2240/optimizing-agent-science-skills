import pandas as pd

mageck = pd.read_csv('essentiality_rra.gene_summary.txt', sep='\t')[['id', 'neg|fdr']].rename(
    columns={'id': 'gene', 'neg|fdr': 'mageck_neg_fdr'})
bagel = pd.read_csv('bayes_factor.txt', sep='\t')[['GENE', 'BF']].rename(
    columns={'GENE': 'gene', 'BF': 'bagel_bf'})
drugz_df = pd.read_csv('drugz_output.txt', sep='\t')[['GENE', 'fdr_synth']].rename(
    columns={'GENE': 'gene', 'fdr_synth': 'drugz_synth_fdr'})

merged = mageck.merge(bagel, on='gene', how='outer').merge(drugz_df, on='gene', how='outer')
merged['mageck_hit'] = merged['mageck_neg_fdr'] < 0.05
merged['bagel_hit'] = merged['bagel_bf'] > 6
merged['drugz_hit'] = merged['drugz_synth_fdr'] < 0.05
merged['tier'] = merged[['mageck_hit', 'bagel_hit', 'drugz_hit']].astype(int).sum(axis=1)
tier1 = merged[merged['tier'] >= 3]
tier2 = merged[merged['tier'] == 2]
merged.to_csv('tier_consensus.csv', index=False)
print("Total genes merged:", len(merged))
print("Tier1 (3/3):", len(tier1), tier1['gene'].head(10).tolist())
print("Tier2 (2/3):", len(tier2))
print("NaN mageck_hit count (outer-join gaps):", merged['mageck_neg_fdr'].isna().sum())
print("NaN bagel_hit count:", merged['bagel_bf'].isna().sum())
print("NaN drugz_hit count:", merged['drugz_synth_fdr'].isna().sum())
