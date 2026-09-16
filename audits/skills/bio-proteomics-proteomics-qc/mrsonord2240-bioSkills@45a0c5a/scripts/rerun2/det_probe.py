# Determinism probe for SKILL.md pca_batch_check: sklearn PCA is constructed with no random_state.
import numpy as np, pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.stats import f_oneway
from skill import S

D = '../data/'
plex = {p: pd.read_csv(D + f'tmt_plex{p}.csv', index_col='protein') for p in 'AB'}
design = pd.read_csv(D + 'tmt_design.csv')
raw_log = pd.concat([np.log2(m).set_axis(
    [design.set_index(['plex','channel']).loc[(p,c),'sample'] for c in m.columns if c != '131'] +
    ([design.set_index(['plex','channel']).loc[(p,'131'),'sample']] if '131' in m.columns else []), axis=1)
    for p, m in plex.items()], axis=1) if False else None

# simpler: reuse the canonical LFQ matrix
pg = pd.read_csv(D + 'proteinGroups.txt', sep='\t', low_memory=False)
info = pd.read_csv(D + 'sample_annotation.csv').set_index('sample')
clean = S['strip_contaminant_rows'](pg)
lfq = clean[[f'LFQ intensity {s}' for s in info.index]].replace(0, np.nan)
lfq.columns = info.index
log2 = np.log2(lfq)
filt = S['completeness_filter'](log2, info['condition'], 0.7).dropna(how='any')
print('complete proteins:', len(filt), 'samples:', filt.shape[1])

X = StandardScaler().fit_transform(filt.T)
print('sklearn PCA svd_solver chosen for this shape: n_components=5,',
      'X shape', X.shape)
for solver in ('auto', 'full'):
    ps = []
    for _ in range(5):
        pcs = PCA(n_components=5, svd_solver=solver).fit(X)
        co = pd.DataFrame(pcs.transform(X), columns=[f'PC{i+1}' for i in range(5)],
                          index=filt.columns).join(info)
        g = [co[co['batch'] == b]['PC3'] for b in co['batch'].unique()]
        ps.append(round(float(f_oneway(*g)[1]), 6))
    print(f'  svd_solver={solver:5s} PC3~batch p over 5 fits: {ps}  unique={len(set(ps))}')
# and with a fixed random_state
ps = []
for _ in range(5):
    pcs = PCA(n_components=5, random_state=0).fit(X)
    co = pd.DataFrame(pcs.transform(X), columns=[f'PC{i+1}' for i in range(5)],
                      index=filt.columns).join(info)
    g = [co[co['batch'] == b]['PC3'] for b in co['batch'].unique()]
    ps.append(round(float(f_oneway(*g)[1]), 6))
print(f'  random_state=0    PC3~batch p over 5 fits: {ps}  unique={len(set(ps))}')
