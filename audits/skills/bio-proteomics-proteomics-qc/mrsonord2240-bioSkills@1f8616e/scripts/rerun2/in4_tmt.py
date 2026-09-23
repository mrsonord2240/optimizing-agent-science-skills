# Re-audit 2026-09-15, Input 4 (Variant B, regression). TMT two 10-plexes: SKILL.md tmt_channel_balance verbatim on
# raw reporter intensities; positive control with one channel scaled 0.3x; cross-plex via reference ratio.
import numpy as np, pandas as pd
from skill import S
D = '../data/'
plex = {p: pd.read_csv(D + f'tmt_plex{p}.csv', index_col='protein') for p in 'AB'}
bal = S['tmt_channel_balance'](plex)
print(bal.round(3).to_string())
print('flagged:', bal.loc[bal.investigate, ['plex', 'channel']].values.tolist())
tot = {p: m.sum().median() for p, m in plex.items()}
print('plex B / plex A median channel total:', round(tot['B'] / tot['A'], 2))
bad = {p: m.copy() for p, m in plex.items()}
bad['A']['128C'] = bad['A']['128C'] * 0.3
b2 = S['tmt_channel_balance'](bad)
print('positive control (A 128C x0.3) flagged:', b2.loc[b2.investigate, ['plex', 'channel']].values.tolist(),
      '| fold', round(float(b2.loc[(b2.plex == 'A') & (b2.channel == '128C'), 'fold_vs_plex_median'].iloc[0]), 3))
# cross-plex comparison through the pooled reference 131
design = pd.read_csv(D + 'tmt_design.csv')
lr = pd.concat([np.log2(m.drop(columns='131').div(m['131'], axis=0)).set_axis(
    [design.set_index(['plex', 'channel']).loc[(p, c), 'sample'] for c in m.columns if c != '131'], axis=1) for p, m in plex.items()], axis=1)
si = design[design.condition != 'Reference'].set_index('sample'); si['plex'] = si['plex'].astype(str)
raw_log = pd.concat([np.log2(m.drop(columns='131')).set_axis(
    [design.set_index(['plex', 'channel']).loc[(p, c), 'sample'] for c in m.columns if c != '131'], axis=1) for p, m in plex.items()], axis=1)
print('\nPCA raw log2 reporters, batch=plex:')
S['pca_batch_check'](raw_log - raw_log.median(), si, batch_col='plex')
print('PCA log2 ratio to 131, batch=plex:')
c, _ = S['pca_batch_check'](lr - lr.median(), si, batch_col='plex')
from scipy.stats import f_oneway
print('  ref-ratio PC1 ~ condition p=%.4f' % f_oneway(*[c.loc[c.condition == k, 'PC1'] for k in ['Control', 'Treatment']])[1])
