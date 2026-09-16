'''
Input 1 (Canonical) -- "Run MAGeCK RRA and BAGEL2 on my HAP1 TKOv3 essentiality screen
(T0 vs T18). Build a consensus hit list using MAGeCK neg|fdr<0.05 and BAGEL2 BF>6.
Output Tier 1 (both methods) and Tier 2 (one method) separately, and validate the
resulting hit list against CEGv2/NEGv1."

This adapts the Skill's own `consensus_hits()` function (SKILL.md, "Run All Five on the
Same Data") to two methods, using the exact thresholds the Skill's own Quantitative
Thresholds table recommends (MAGeCK FDR<0.05; BAGEL2 BF>6 "standard"), NOT the
`consensus_hits()` code's own inline defaults (mageck_fdr_thresh=0.05 matches, but
bagel_bf_thresh=5 default in the code contradicts the Skill's own text-table default of
6 -- flagged below as a P2).

Data: real HAP1 TKOv3 T0-vs-T18 MAGeCK gene_summary.txt and BAGEL2 bayes_factor.txt,
copied unmodified from the already-audited mageck-analysis / bagel-essentiality runs
(same screen, same underlying counts -- a legitimate same-data consensus).
'''
import pandas as pd

MAGECK_FDR_THRESH = 0.05   # SKILL.md Quantitative Thresholds table
BAGEL_BF_THRESH = 6        # SKILL.md Quantitative Thresholds table ("standard")

mageck = pd.read_csv('mageck_hap1.gene_summary.txt', sep='\t')[['id', 'neg|score', 'neg|fdr']] \
    .rename(columns={'id': 'gene', 'neg|score': 'mageck_neg_score', 'neg|fdr': 'mageck_neg_fdr'})
bagel = pd.read_csv('bayes_factor.txt', sep='\t')[['GENE', 'BF']] \
    .rename(columns={'GENE': 'gene', 'BF': 'bagel_bf'})

merged = mageck.merge(bagel, on='gene', how='outer')
merged['mageck_hit'] = merged['mageck_neg_fdr'] < MAGECK_FDR_THRESH
merged['bagel_hit'] = merged['bagel_bf'] > BAGEL_BF_THRESH
merged['n_methods'] = merged[['mageck_hit', 'bagel_hit']].fillna(False).astype(int).sum(axis=1)

tier1 = merged[merged['n_methods'] == 2].sort_values('mageck_neg_score')
tier2_mageck_only = merged[(merged['mageck_hit']) & (~merged['bagel_hit'].fillna(False))]
tier2_bagel_only = merged[(merged['bagel_hit']) & (~merged['mageck_hit'].fillna(False))]

print(f'Total genes merged: {len(merged)}')
print(f'MAGeCK hits (neg|fdr<{MAGECK_FDR_THRESH}): {int(merged["mageck_hit"].sum())}')
print(f'BAGEL2 hits (BF>{BAGEL_BF_THRESH}): {int(merged["bagel_hit"].sum())}')
print(f'Tier 1 (both methods): {len(tier1)}')
print(f'Tier 2 -- MAGeCK-only: {len(tier2_mageck_only)}')
print(f'Tier 2 -- BAGEL2-only: {len(tier2_bagel_only)}')
print()
print('Top 10 Tier 1 consensus hits:')
print(tier1[['gene', 'mageck_neg_score', 'mageck_neg_fdr', 'bagel_bf']].head(10).to_string(index=False))

# --- Ground-truth validation against CEGv2 (core essential) / NEGv1 (non-essential) ---
ceg = set(pd.read_csv('CEGv2.txt', sep='\t')['GENE'])
negv1 = set(pd.read_csv('NEGv1.txt', sep='\t')['GENE'])

def precision_recall(hit_genes, ref_essential, ref_nonessential):
    hit_genes = set(hit_genes)
    tested = ref_essential | ref_nonessential
    tested_hits = hit_genes & tested
    tp = len(tested_hits & ref_essential)
    fp = len(tested_hits & ref_nonessential)
    fn = len(ref_essential - hit_genes)
    precision = tp / (tp + fp) if (tp + fp) else float('nan')
    recall = tp / (tp + fn) if (tp + fn) else float('nan')
    return tp, fp, fn, precision, recall

for label, genes in [('Tier 1 consensus', tier1['gene']),
                      ('MAGeCK-only (Tier 2)', tier2_mageck_only['gene']),
                      ('BAGEL2-only (Tier 2)', tier2_bagel_only['gene'])]:
    tp, fp, fn, prec, rec = precision_recall(genes, ceg, negv1)
    print(f'{label}: n={len(genes)}  CEGv2_hits={tp}  NEGv1_hits={fp}  precision={prec:.3f}  recall(of CEGv2)={rec:.3f}')

merged.to_csv('input1_consensus_output.csv', index=False)
