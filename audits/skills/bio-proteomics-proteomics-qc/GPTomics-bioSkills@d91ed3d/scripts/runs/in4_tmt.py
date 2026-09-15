"""Input 4 (Variant B): TMT channel-loading balance on RAW reporter intensities, two 10-plexes with pooled
reference in 131. Mode A (SKILL.md: Decision Tree 'TMT data, channel looks off'; Thresholds 'investigate > ~2x,
flag > ~3-4x'; no Python code given for TMT). Data: SYNTHETIC tmt_plexA/B.csv. Audit 2026-09-11."""
import os, sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from skill_funcs import *

D = os.path.join(os.path.dirname(__file__), '..', 'data')
design = pd.read_csv(os.path.join(D, 'tmt_design.csv'))
plex = {p: pd.read_csv(os.path.join(D, f'tmt_plex{p}.csv'), index_col='protein') for p in 'AB'}
rows = []
for p, m in plex.items():
    tot = m.sum(); med = m.median()
    for ch in m.columns:
        rows.append({'plex': p, 'channel': ch, 'total': tot[ch], 'median': med[ch],
                     'fold_total_within_plex': tot[ch] / tot.median(), 'n_zero_or_na': int((m[ch].fillna(0) == 0).sum())})
bal = pd.DataFrame(rows)
bal['fold_total_across_plexes'] = bal['total'] / bal['total'].median()
bal['flag_within'] = np.where(abs(np.log2(bal['fold_total_within_plex'])) > 1, 'INVESTIGATE(>2x)', '')
bal['flag_across'] = np.where(abs(np.log2(bal['fold_total_across_plexes'])) > 1, 'INVESTIGATE(>2x)', '')
print(bal.round(3).to_string())
print('\nWithin-plex flags :', bal.loc[bal.flag_within != '', ['plex', 'channel']].values.tolist())
print('Across-plex flags :', bal.loc[bal.flag_across != '', ['plex', 'channel']].values.tolist())
print('Plex B / plex A median total ratio:', round(bal[bal.plex == 'B']['total'].median() / bal[bal.plex == 'A']['total'].median(), 2))

# Reference-channel ratio: log2(channel / 131) per protein removes the plex (elution-sampling) effect
lr = []
for p, m in plex.items():
    r = np.log2(m.drop(columns='131').div(m['131'], axis=0))
    r.columns = [design.set_index(['plex', 'channel']).loc[(p, c), 'sample'] for c in r.columns]
    lr.append(r)
lr = pd.concat(lr, axis=1)
raw_log = pd.concat([np.log2(plex['A'].drop(columns='131')).set_axis(lr.columns[:9], axis=1),
                     np.log2(plex['B'].drop(columns='131')).set_axis(lr.columns[9:], axis=1)], axis=1)
si = design[design.condition != 'Reference'].set_index('sample')
si['plex'] = si['plex'].astype(str)
print('\nPCA on raw log2 reporter intensities (both plexes):')
c1, e1 = pca_batch_check(raw_log - raw_log.median(), si, batch_col='plex')
print('  explained', np.round(e1, 3))
print('PCA on log2 ratio to pooled reference 131:')
c2, e2 = pca_batch_check(lr - lr.median(), si, batch_col='plex')
print('  explained', np.round(e2, 3))
from scipy.stats import f_oneway
for name, c in (('raw', c1), ('ref-ratio', c2)):
    _, p = f_oneway(*[c.loc[c['condition'] == k, 'PC1'] for k in ['Control', 'Treatment']])
    print(f'  {name}: PC1 ~ condition p={p:.4f}')

# Ratio compression check the SKILL describes: observed treatment effect on known-up proteins
truth = pd.read_csv(os.path.join(D, 'truth_proteins.csv')).set_index('protein')
tp = truth.reindex(lr.index)
t = [c for c in lr.columns if '_T' in c]; cc = [c for c in lr.columns if '_C' in c]
obs = lr[t].mean(axis=1) - lr[cc].mean(axis=1)
sel = tp['class'].isin(['up', 'down'])
slope = np.polyfit(tp.loc[sel, 'true_log2fc'], obs[sel], 1)[0]
print(f'\nObserved vs true log2FC slope on {int(sel.sum())} true DA proteins: {slope:.2f} (ratio compression; SKILL.md: "10:1 reads ~5:1")')
