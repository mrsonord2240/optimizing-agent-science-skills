#!/usr/bin/env python3
"""Corrected version of the SKILL.md NSTI snippet -- using the REAL filename PICRUSt2 2.6.3
produces (combined_marker_predicted_and_nsti.tsv.gz), to get the actual NSTI distribution
for the real 770-ASV / 34-sample moving-pictures gut dataset (PICRUSt2's best-case
environment per the skill's own claims)."""
import pandas as pd

nsti = pd.read_csv('picrust2_out_real/combined_marker_predicted_and_nsti.tsv.gz', sep='\t')
asv_counts = pd.read_csv('asv_table_fixed.tsv', sep='\t', index_col=0)
nsti = nsti.set_index('sequence')
reads_per_asv = asv_counts.sum(axis=1)

max_nsti = 2.0
dropped = nsti.index[nsti['metadata_NSTI'] > max_nsti]
reads_dropped_frac = reads_per_asv.reindex(dropped).sum() / reads_per_asv.sum()
print(f'mean NSTI {nsti.metadata_NSTI.mean():.3f}  median {nsti.metadata_NSTI.median():.3f}')
print(f'ASVs dropped at NSTI>{max_nsti}: {len(dropped)}/{len(nsti)}  reads dropped: {reads_dropped_frac:.1%}')
print(f'total ASVs in nsti file: {len(nsti)}  total ASVs in table: {len(asv_counts)}')

# Sanity-check the pathway table too
paths = pd.read_csv('picrust2_out_real/pathways_out/path_abun_unstrat.tsv.gz', sep='\t', index_col=0)
print(f'MetaCyc pathways predicted: {paths.shape[0]}, samples: {paths.shape[1]}')
print('Top 5 pathways by total abundance:')
print(paths.sum(axis=1).sort_values(ascending=False).head(5))

ko = pd.read_csv('picrust2_out_real/KO_metagenome_out/pred_metagenome_unstrat.tsv.gz', sep='\t', index_col=0)
print(f'KOs predicted: {ko.shape[0]}, samples: {ko.shape[1]}')
