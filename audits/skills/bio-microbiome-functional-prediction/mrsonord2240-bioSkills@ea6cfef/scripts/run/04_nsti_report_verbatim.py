#!/usr/bin/env python3
# Re-audit: SKILL.md's corrected "Report NSTI (mandatory)" Python snippet, copied verbatim
# (only path substituted to point at picrust2_out_reaudit -- MY OWN freshly-generated output,
# not the original audit's or fixer's cached picrust2_out_real), run against a truly
# independent PICRUSt2 execution.
import pandas as pd

nsti = pd.read_csv('picrust2_out_reaudit/combined_marker_predicted_and_nsti.tsv.gz', sep='\t')   # cols: sequence, metadata_NSTI
asv_counts = pd.read_csv('asv_table_fixed.tsv', sep='\t', index_col=0)                # ASVs x samples
nsti = nsti.set_index('sequence')
reads_per_asv = asv_counts.sum(axis=1)

max_nsti = 2.0   # PICRUSt2 default; ASVs above this are dropped before metagenome inference
dropped = nsti.index[nsti['metadata_NSTI'] > max_nsti]
reads_dropped_frac = reads_per_asv.reindex(dropped).sum() / reads_per_asv.sum()
print(f'mean NSTI {nsti.metadata_NSTI.mean():.3f}  median {nsti.metadata_NSTI.median():.3f}')
print(f'ASVs dropped at NSTI>{max_nsti}: {len(dropped)}/{len(nsti)}  reads dropped: {reads_dropped_frac:.1%}')
