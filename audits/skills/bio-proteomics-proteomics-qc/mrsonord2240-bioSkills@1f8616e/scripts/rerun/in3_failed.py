# Re-audit 2026-09-15, Input 3 (Edge, regression). proteinGroups_failed.txt: T4 loaded ~3x low, LFQ re-normalised.
# User looked at LFQ boxplots. Skill names Intensity as the raw column; raw_sample_qc flags on total / IDs.
import numpy as np, pandas as pd
from skill import S
D = '../data/'
info = pd.read_csv(D + 'sample_annotation.csv').set_index('sample'); grp = info['condition']; samples = info.index.tolist()
for fname in ['proteinGroups.txt', 'proteinGroups_failed.txt']:
    pg = S['strip_contaminant_rows'](pd.read_csv(D + fname, sep='\t', low_memory=False))
    for prefix in ['LFQ intensity', 'Intensity']:
        m = pg[[f'{prefix} {s}' for s in samples]]; m.columns = samples
        q = S['raw_sample_qc'](m, grp)
        print(f'--- {fname} | {prefix}: flagged {q.index[q.flag].tolist()}')
        if fname.endswith('failed.txt'):
            print(q.loc[['T1', 'T2', 'T3', 'T4'], ['n_quantified', 'missing_pct', 'fold_total_vs_group', 'ids_vs_group', 'flag']].round(3).to_string())
pg = S['strip_contaminant_rows'](pd.read_csv(D + 'proteinGroups_failed.txt', sep='\t', low_memory=False))
m = np.log2(pg[[f'Intensity {s}' for s in samples]].replace(0, np.nan)); m.columns = samples
med = m.median()
print('\nT4 raw log2 median fold vs group:', round(2 ** (med['T4'] - med[['T1', 'T2', 'T3', 'T4']].median()), 3))
print('after median normalisation all medians:', (m - med).median().round(2).unique().tolist())
