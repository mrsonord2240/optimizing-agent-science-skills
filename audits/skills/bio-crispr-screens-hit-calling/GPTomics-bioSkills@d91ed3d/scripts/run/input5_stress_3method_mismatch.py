'''
Input 5 (Stress) -- "Run MAGeCK + BAGEL2 + drugZ on my screen. Output the tier-1
consensus (3-method agreement) at FDR <0.05 / BF >6 across all. These hits go to
arrayed validation." (usage-guide.md, Multi-Method Consensus, verbatim prompt.)

Stress test: this lab has three real result files on hand -- MAGeCK and BAGEL2 from the
HAP1 TKOv3 T0-vs-T18 ESSENTIALITY dropout screen, and a drugZ table from a SEPARATE
drug-vs-vehicle CHEMOGENOMIC screen on the same library. The SKILL's own instruction is
to "Run MAGeCK + BAGEL2 + (drugZ or JACKS) on the SAME count matrix" (SKILL.md, "Run All
Five on the Same Data") -- but nothing in SKILL.md, usage-guide.md, or consensus_hits()
itself checks that the three input files actually came from the same screen/arm before
merging on gene symbol. This reproduces exactly that mistake: extending the Skill's own
`consensus_hits()` pattern to three methods whose files are on-hand but not experimentally
comparable, to see whether the code (or the Skill's guidance) catches it.
'''
import pandas as pd

def consensus_hits(mageck_path, bagel_path, drugz_path,
                    mageck_fdr_thresh=0.05, bagel_bf_thresh=6, drugz_fdr_thresh=0.05):
    '''Adapted directly from SKILL.md's consensus_hits(), 3-method form.'''
    mageck = pd.read_csv(mageck_path, sep='\t')[['id', 'neg|fdr']].rename(columns={'id': 'gene', 'neg|fdr': 'mageck_neg_fdr'})
    bagel = pd.read_csv(bagel_path, sep='\t')[['GENE', 'BF']].rename(columns={'GENE': 'gene', 'BF': 'bagel_bf'})
    drugz = pd.read_csv(drugz_path, sep='\t')[['GENE', 'fdr_synth']].rename(columns={'GENE': 'gene', 'fdr_synth': 'drugz_synth_fdr'})
    merged = mageck.merge(bagel, on='gene', how='outer').merge(drugz, on='gene', how='outer')
    merged['mageck_hit'] = merged['mageck_neg_fdr'] < mageck_fdr_thresh
    merged['bagel_hit'] = merged['bagel_bf'] > bagel_bf_thresh
    merged['drugz_hit'] = merged['drugz_synth_fdr'] < drugz_fdr_thresh
    merged['consensus_count'] = (merged[['mageck_hit', 'bagel_hit', 'drugz_hit']].astype(int)).sum(axis=1)
    return merged.sort_values('consensus_count', ascending=False)

result = consensus_hits('mageck_hap1.gene_summary.txt', 'bayes_factor.txt', 'drugz_drug_output.txt')

tier1 = result[result['consensus_count'] == 3]
print(f'Total genes merged: {len(result)}')
print(f'Tier 1 (3/3 "consensus") genes: {len(tier1)}')
print(tier1[['gene', 'mageck_neg_fdr', 'bagel_bf', 'drugz_synth_fdr']].to_string(index=False) if len(tier1) else '(none)')
print()

# Sanity check: are the drugZ "hits" here actually the planted drug-response genes, or
# essentiality genes that happen to pass drugZ's synthetic-lethal FDR threshold on an
# unrelated comparison?
ground_truth = open('drugz_ground_truth.txt').read()
print('drugZ ground truth for THIS table (drug-response study, not essentiality):')
print(ground_truth)
planted = set()
for line in ground_truth.strip().split('\n'):
    planted.update(line.split('\t')[1].split(','))
overlap = set(tier1['gene']) & planted
print(f'Of the {len(tier1)} nominal "3-method consensus" genes, {len(overlap)} are actually')
print(f'planted drug-response genes from the drugZ study: {sorted(overlap) if overlap else "(none)"}')
print('The rest are essentiality genes from a DIFFERENT screen whose drugZ FDR is an artifact')
print('of running drugZ math on a comparison it was never designed to answer for this table.')
