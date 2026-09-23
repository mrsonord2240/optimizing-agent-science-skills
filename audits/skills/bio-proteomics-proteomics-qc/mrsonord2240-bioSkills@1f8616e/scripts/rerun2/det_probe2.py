import numpy as np, pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.stats import f_oneway
from skill import S
D = '../data/'
plex = {p: pd.read_csv(D + f'tmt_plex{p}.csv', index_col='protein') for p in 'AB'}
design = pd.read_csv(D + 'tmt_design.csv')
idx = design.set_index(['plex', 'channel'])
raw_log = pd.concat([np.log2(m).set_axis([idx.loc[(p, c), 'sample'] for c in m.columns], axis=1)
                     for p, m in plex.items()], axis=1)
si = design.set_index('sample'); si['plex'] = si['plex'].astype(str)
M = (raw_log - raw_log.median()).dropna(how='any')
X = StandardScaler().fit_transform(M.T)
print('TMT matrix for PCA:', X.shape, '(samples x proteins)')
n_pc = min(5, X.shape[0] - 1)
for kw in ({'svd_solver': 'auto'}, {'svd_solver': 'full'}, {'random_state': 0}):
    ps = []
    for _ in range(6):
        pcs = PCA(n_components=n_pc, **kw).fit(X)
        co = pd.DataFrame(pcs.transform(X), columns=[f'PC{i+1}' for i in range(n_pc)],
                          index=M.columns).join(si)
        g = [co[co['plex'] == b]['PC3'] for b in co['plex'].unique()]
        ps.append(round(float(f_oneway(*g)[1]), 5))
    print(f'  {str(kw):28s} PC3~plex p over 6 fits: {ps} unique={len(set(ps))}')
print('\nexplained_variance_ratio over 3 auto fits:')
for _ in range(3):
    print('  ', np.round(PCA(n_components=n_pc).fit(X).explained_variance_ratio_, 5))
