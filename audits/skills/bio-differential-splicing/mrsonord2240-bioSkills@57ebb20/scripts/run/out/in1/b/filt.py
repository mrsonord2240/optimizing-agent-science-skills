import pandas as pd
import numpy as np

se = pd.read_csv('rmats_output/SE.MATS.JC.txt', sep='\t')

def has_coverage_in_each_rep(inc, skip, minimum=10):
    """Require inclusion + skipping reads in every replicate, not two unrelated minima."""
    inc_values = [int(v) for v in inc.split(',')]
    skip_values = [int(v) for v in skip.split(',')]
    return len(inc_values) == len(skip_values) and all(
        (i + s) >= minimum for i, s in zip(inc_values, skip_values)
    )

se['coverage_ok'] = se.apply(
    lambda row: has_coverage_in_each_rep(row['IJC_SAMPLE_1'], row['SJC_SAMPLE_1']) and
                has_coverage_in_each_rep(row['IJC_SAMPLE_2'], row['SJC_SAMPLE_2']),
    axis=1,
)

significant = se[
    (se['FDR'] < 0.05) &
    (se['IncLevelDifference'].abs() > 0.10) &
    se['coverage_ok']
].copy()
print('significant rows:', len(significant)); print(significant[['GeneID','IncLevelDifference','FDR','coverage_ok']].to_string())
