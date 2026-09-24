# NEW input (auditor-designed): Step 6b's mageck mle example
#   `mageck mle --count-table experiment.count.txt --design-matrix design.txt \
#      --output-prefix timecourse_mle --norm-method median`
# does not set --permutation-round, so it silently uses MAGeCK's default (2). The sibling
# Skill mageck-analysis (fixed and re-audited this round) found that raising
# --permutation-round from 2 to 5 flipped 19/48 (40%) of a real screen's FDR<0.05 hits, and
# now documents ">=10 for any FDR call near 0.05". This pipeline's own Step 6b example
# carries no such caveat and no cross-reference to it.
#
# This script reproduces that defect at reduced scale (1500 genes / 5,926 sgRNAs subsampled
# from the same real HAP1 TKOv3 count table used elsewhere in this audit, using a synthetic
# 3-timepoint design: T0=baseline, T18_A=day7, T18_B/T18_C=day14 replicates) to confirm it
# is a live, reproducible property of this Skill's own literal command, not just an
# inherited generic warning.
#
# CLI invocations (run via PowerShell, native Windows PATH for RRA.exe):
#   mageck mle --count-table mle_subsample.count.txt --design-matrix mle_design.txt \
#     --output-prefix mle_default --norm-method median                   # default round=2
#   mageck mle --count-table mle_subsample.count.txt --design-matrix mle_design.txt \
#     --permutation-round 10 --output-prefix mle_round10 --norm-method median
import pandas as pd

d = pd.read_csv('mle_default.gene_summary.txt', sep='\t')[['Gene', 'day14|fdr']].rename(
    columns={'day14|fdr': 'fdr_r2'})
r10 = pd.read_csv('mle_round10.gene_summary.txt', sep='\t')[['Gene', 'day14|fdr']].rename(
    columns={'day14|fdr': 'fdr_r10'})
m = d.merge(r10, on='Gene')
h2 = m['fdr_r2'] < 0.05
h10 = m['fdr_r10'] < 0.05
print('genes total:', len(m))
print('round2 (documented default) hits, day14 FDR<0.05:', h2.sum())
print('round10 hits, day14 FDR<0.05:', h10.sum())
print('flips:', (h2 != h10).sum())
print(m[h2 != h10][['Gene', 'fdr_r2', 'fdr_r10']].to_string())
