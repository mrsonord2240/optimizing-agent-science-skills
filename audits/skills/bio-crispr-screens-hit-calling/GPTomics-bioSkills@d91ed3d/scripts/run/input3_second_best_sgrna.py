'''
Input 3 (Variant B) -- "Apply the second-best-sgRNA rule: a gene is a hit only if the
2nd-most-extreme sgRNA also passes the threshold. Filter my MAGeCK hit list by this
rule and flag single-guide-driven hits for orthogonal validation."

Runs the Skill's own `second_best_lfc()` function (SKILL.md, "Second-Best sgRNA
Conservative Rule") verbatim against the real HAP1 TKOv3 MAGeCK sgrna_summary.txt,
for the Tier-1 consensus gene list computed in Input 1.
'''
import pandas as pd

def second_best_lfc(sgrna_lfc_df, genes_series, direction='neg'):
    '''Verbatim from SKILL.md.'''
    results = []
    for gene in genes_series.unique():
        gene_lfc = sgrna_lfc_df[genes_series == gene].sort_values()
        if direction == 'neg':
            second = gene_lfc.iloc[1] if len(gene_lfc) >= 2 else gene_lfc.iloc[0]
        else:
            second = gene_lfc.iloc[-2] if len(gene_lfc) >= 2 else gene_lfc.iloc[-1]
        results.append({'gene': gene, 'second_best_lfc': second})
    return pd.DataFrame(results)

sgrna = pd.read_csv('mageck_hap1.sgrna_summary.txt', sep='\t')
tier1 = pd.read_csv('input1_consensus_output.csv')
tier1_genes = tier1[tier1['n_methods'] == 2]['gene']

sub = sgrna[sgrna['Gene'].isin(tier1_genes)]
result = second_best_lfc(sub['LFC'], sub['Gene'], direction='neg')

# Also compute how many sgRNAs each gene actually had (needed to interpret "second-best"
# meaningfully -- the SKILL's own function silently falls back to the single guide's own
# LFC when a gene has only 1 sgRNA, which _looks_ like it passed the second-best rule
# even though there is no second guide at all. Flag this.)
n_guides = sub.groupby('Gene').size().rename('n_sgrnas')
result = result.merge(n_guides, left_on='gene', right_index=True)

THRESHOLD = -1.0  # abs(LFC) > 1, SKILL.md Quantitative Thresholds table (2-fold)
result['passes_second_best_rule'] = result['second_best_lfc'] < THRESHOLD
result['single_guide_gene'] = result['n_sgrnas'] < 2

print(f'Tier-1 genes checked: {len(result)}')
print(f'Pass second-best rule (second-best LFC < {THRESHOLD}): {int(result["passes_second_best_rule"].sum())}')
print(f'Genes with only 1 sgRNA in this library (silently exempt from the rule): {int(result["single_guide_gene"].sum())}')
print()
print('Genes that FAIL the second-best rule (single-outlier-guide risk), sorted by second_best_lfc:')
failing = result[~result['passes_second_best_rule']].sort_values('second_best_lfc')
print(failing.to_string(index=False) if len(failing) else '(none)')
print()
print('Sample of passing genes (top 5 most negative second-best LFC):')
print(result[result['passes_second_best_rule']].sort_values('second_best_lfc').head(5).to_string(index=False))
