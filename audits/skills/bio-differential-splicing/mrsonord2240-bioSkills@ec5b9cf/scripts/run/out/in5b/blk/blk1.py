import pandas as pd
import numpy as np

se = pd.read_csv('rmats_output/SE.MATS.JC.txt', sep='\t')

def min_per_rep(s):
    return s.str.split(',').apply(lambda x: min(int(v) for v in x))

se['min_inc'] = min_per_rep(se['IJC_SAMPLE_1']).combine(min_per_rep(se['IJC_SAMPLE_2']), min)
se['min_skip'] = min_per_rep(se['SJC_SAMPLE_1']).combine(min_per_rep(se['SJC_SAMPLE_2']), min)

significant = se[
    (se['FDR'] < 0.05) &
    (se['IncLevelDifference'].abs() > 0.10) &
    ((se['min_inc'] + se['min_skip']) >= 10)
].copy()
