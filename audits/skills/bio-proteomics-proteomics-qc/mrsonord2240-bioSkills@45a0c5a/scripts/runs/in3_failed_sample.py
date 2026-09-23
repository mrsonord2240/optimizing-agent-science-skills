"""Input 3 (Edge): failed-loading sample hidden by MaxLFQ. Mode A, SKILL.md inspect-before-normalize procedure.
Data: SYNTHETIC proteinGroups_failed.txt (T4 loaded ~3x low; LFQ column re-normalised) vs proteinGroups.txt.
Audit 2026-09-11."""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from skill_funcs import *

D = os.path.join(os.path.dirname(__file__), '..', 'data')
info = pd.read_csv(os.path.join(D, 'sample_annotation.csv')).set_index('sample')
samples = info.index.tolist()
grp = info['condition']


def inspect(path, prefix):
    pg = strip_contaminant_rows(pd.read_csv(path, sep='\t', low_memory=False))
    m = pg[[f'{prefix} {s}' for s in samples]].replace(0, np.nan)   # MaxQuant 0 = missing
    m.columns = samples
    q = raw_sample_qc(m)
    q['log2_median'] = np.log2(q['median_intensity'])
    q['fold_total_vs_group'] = q['total_signal'] / q.assign(g=grp).groupby('g')['total_signal'].transform('median')
    q['fold_median_vs_group'] = q['median_intensity'] / q.assign(g=grp).groupby('g')['median_intensity'].transform('median')
    q['ids_vs_group'] = q['n_quantified'] / q.assign(g=grp).groupby('g')['n_quantified'].transform('median')
    # SKILL.md l.103: "a sample shifted >=2-3x below its group median is a loading/injection failure to exclude"
    q['flag_2x'] = (q['fold_total_vs_group'] <= 0.5) | (q['fold_median_vs_group'] <= 0.5)
    return q


for fname in ['proteinGroups.txt', 'proteinGroups_failed.txt']:
    for prefix in ['LFQ intensity', 'Intensity']:
        q = inspect(os.path.join(D, fname), prefix)
        print(f'\n=== {fname} | column "{prefix} <sample>" ===')
        print(q[['n_quantified', 'missing_pct', 'log2_median', 'fold_total_vs_group', 'fold_median_vs_group', 'ids_vs_group', 'flag_2x']].round(3).to_string())
        print('flagged by >=2x rule:', q.index[q['flag_2x']].tolist())

# Downstream consequence (why it matters): median-normalize the RAW Intensity matrix and look again
pg = strip_contaminant_rows(pd.read_csv(os.path.join(D, 'proteinGroups_failed.txt'), sep='\t', low_memory=False))
m = np.log2(pg[[f'Intensity {s}' for s in samples]].replace(0, np.nan)); m.columns = samples
norm = m - m.median()
print('\nlog2 medians RAW:', m.median().round(2).to_dict())
print('log2 medians after median-normalisation:', norm.median().round(2).to_dict(), '-> evidence erased, as SKILL.md says')
rc = replicate_correlation(norm, grp)
print('\nWithin-Treatment r after normalisation (failed file):')
print(rc[rc.group == 'Treatment'].round(3).to_string())
