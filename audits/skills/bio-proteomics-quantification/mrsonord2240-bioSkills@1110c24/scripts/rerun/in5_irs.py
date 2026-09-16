'''Quant Input 5 (regression, stress): two TMT10 plexes, 131 pooled reference, plex B ~2x; SL + IRS; some proteins lack a
plex-B reference. Block b05 executed verbatim. SYNTHETIC data.'''
import numpy as np, pandas as pd, warnings
QQ = 'F:/OpenScience/audits/bio-proteomics-quantification'
ns = {}
with open(f'{QQ}/rerun/blocks/b05_Bridge_multiple_TMT_plexes_with_IRS.py', encoding='utf-8') as fh:
    exec(fh.read(), ns)
A = pd.read_csv(f'{QQ}/data/tmt_plexA.csv', index_col=0); B = pd.read_csv(f'{QQ}/data/tmt_plexB.csv', index_col=0)
des = pd.read_csv(f'{QQ}/data/tmt_design.csv', dtype=str)
common = A.index.intersection(B.index); A, B = A.loc[common].copy(), B.loc[common].copy()
B.iloc[0:3, B.columns.get_loc('131')] = 0; B.iloc[3:6, B.columns.get_loc('131')] = np.nan
cond = dict(zip(des['plex'] + '_' + des['channel'], des['condition']))
def report(tag, a, b):
    la, lb = np.log2(a.drop(columns='131')), np.log2(b.drop(columns='131'))
    off = float(np.nanmedian(lb.mean(axis=1) - la.mean(axis=1)))
    X = pd.concat([la.add_prefix('A_'), lb.add_prefix('B_')], axis=1).replace([np.inf, -np.inf], np.nan).dropna()
    Xc = X.sub(X.mean(axis=1), axis=0).values
    u, s, vt = np.linalg.svd(Xc, full_matrices=False); pc1 = vt[0]
    plex = np.array([c.startswith('B_') for c in X.columns], float); cnd = np.array([cond[c] == 'Treatment' for c in X.columns], float)
    r2 = lambda y: np.corrcoef(pc1, y)[0, 1] ** 2
    print(f'{tag:9s} non-ref plex offset B-A {off:+.3f} | R2(PC1~plex) {r2(plex):.2f} | R2(PC1~condition) {r2(cnd):.2f}')
report('raw', A, B)
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter('always')
    sl = [ns['sample_loading_normalize'](A), ns['sample_loading_normalize'](B)]
    report('SL only', *sl)
    br = ns['irs_scale'](sl, ['131', '131'])
    print('warnings:', sorted({str(x.message)[:60] for x in w}))
report('SL + IRS', *br)
lb = np.log2(br[1])
print('bridged plex B: +inf cells', int(np.isinf(lb.values).sum()), '| NaN rows', int(lb.isna().all(axis=1).sum()), '| of which masked refs:', list(lb.index[lb.isna().all(axis=1)][:6]))
