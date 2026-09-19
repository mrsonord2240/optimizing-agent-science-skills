#!/usr/bin/env python3
"""Run the SKILL.md 'Report NSTI (mandatory)' code snippet VERBATIM (only the picrust2_out
path prefix substituted for our real output dir name) against the real 770-ASV
moving-pictures PICRUSt2 output, to check whether the skill's own documented, mandatory
QC step actually works as written on the real tool output."""
import pandas as pd

nsti = pd.read_csv('picrust2_out_real/marker_predicted_and_nsti.tsv.gz', sep='\t')   # cols: sequence, metadata_NSTI
asv_counts = pd.read_csv('asv_table_fixed.tsv', sep='\t', index_col=0)                # ASVs x samples
nsti = nsti.set_index('sequence')
reads_per_asv = asv_counts.sum(axis=1)

max_nsti = 2.0
dropped = nsti.index[nsti['metadata_NSTI'] > max_nsti]
reads_dropped_frac = reads_per_asv.reindex(dropped).sum() / reads_per_asv.sum()
print(f'mean NSTI {nsti.metadata_NSTI.mean():.3f}  median {nsti.metadata_NSTI.median():.3f}')
print(f'ASVs dropped at NSTI>{max_nsti}: {len(dropped)}/{len(nsti)}  reads dropped: {reads_dropped_frac:.1%}')
