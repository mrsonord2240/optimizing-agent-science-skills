"""Input 5 (Stress) - two TMT10 plexes, pooled reference in 131, SL then IRS (SKILL.md lines 147-164, verbatim),
with a normalization report and a missing/zero reference channel for some proteins.
Data: SYNTHETIC tmt_plexA.csv / tmt_plexB.csv / tmt_design.csv (shared generator; plex B offset ~2x, MS2 compression ~0.6).
"""
import numpy as np
import pandas as pd

D = 'F:/OpenScience/audits/bio-proteomics-quantification/data/'
A = pd.read_csv(D + 'tmt_plexA.csv', index_col=0)
B = pd.read_csv(D + 'tmt_plexB.csv', index_col=0)
design = pd.read_csv(D + 'tmt_design.csv', dtype={'channel': str})
truth = pd.read_csv(D + 'truth_proteins.csv', index_col=0)
A.columns = [f'A_{c}' for c in A.columns]
B.columns = [f'B_{c}' for c in B.columns]


# ---------------- the Skill's code, verbatim
def sample_loading_normalize(plex):
    target = plex.sum(axis=0).mean()    # common target = mean column sum within the plex
    return plex * (target / plex.sum(axis=0))


def irs_scale(plexes, ref_cols):
    refs = pd.concat([p[ref] for p, ref in zip(plexes, ref_cols)], axis=1)
    geomean = np.exp(np.log(refs.replace(0, np.nan)).mean(axis=1))    # per-protein geometric mean of references
    out = []
    for p, ref in zip(plexes, ref_cols):
        factor = geomean / p[ref]    # per-protein per-plex scaling factor
        out.append(p.mul(factor, axis=0))
    return out


def report(tag, a, b):
    """Normalization report: plex effect on NON-reference channels (not the tautological ref check)."""
    la, lb = np.log2(a.drop(columns='A_131')), np.log2(b.drop(columns='B_131'))
    allm = pd.concat([la, lb], axis=1).replace([np.inf, -np.inf], np.nan).dropna()
    x = allm.sub(allm.mean(axis=1), axis=0).values.T                         # samples x proteins, row-centred
    u, s, vt = np.linalg.svd(x - x.mean(axis=0), full_matrices=False)
    pc1 = u[:, 0] * s[0]
    plex = np.array([c[0] for c in allm.columns])
    cond = np.array(['T' if '_T' in design.set_index(design['plex'] + '_' + design['channel']).loc[c, 'sample'] else 'C' for c in allm.columns])
    r2 = lambda lab: 1 - sum(((pc1[lab == g] - pc1[lab == g].mean()) ** 2).sum() for g in set(lab)) / ((pc1 - pc1.mean()) ** 2).sum()
    offset = (lb.median(axis=1) - la.median(axis=1)).median()
    print(f'{tag:<22} proteins={len(allm):4d}  median per-protein plex offset B-A={offset:+.3f} log2  '
          f'PC1 var={s[0]**2/(s**2).sum():.2f}  R2(PC1~plex)={r2(plex):.2f}  R2(PC1~condition)={r2(cond):.2f}')
    return allm


print('column sums (1e9) plex A raw:', (A.sum() / 1e9).round(2).tolist())
raw = report('raw', A, B)
sl = [sample_loading_normalize(A), sample_loading_normalize(B)]
print('column sums (1e9) plex A after SL:', (sl[0].sum() / 1e9).round(2).tolist())
report('SL only', *sl)
bridged = irs_scale(sl, ['A_131', 'B_131'])
irs = report('SL + IRS', *bridged)

# truth recovery on the bridged matrix (cross-plex condition contrast)
dsg = design.assign(col=design['plex'] + '_' + design['channel']).set_index('col')
Tcols = [c for c in irs.columns if dsg.loc[c, 'condition'] == 'Treatment']
Ccols = [c for c in irs.columns if dsg.loc[c, 'condition'] == 'Control']
lfc = irs[Tcols].mean(axis=1) - irs[Ccols].mean(axis=1)
t = truth.reindex(lfc.index)
de = t['class'].isin(['up', 'down'])
slope = np.polyfit(t.loc[de, 'true_log2fc'], lfc[de], 1)[0]
print(f'DE proteins in TMT set: {int(de.sum())}; slope(observed log2FC ~ true log2FC) = {slope:.2f}  (MS2 compression; not removed by SL/IRS)')

# ---------------- stress: reference value 0 / NaN for some proteins in plex B
A2, B2 = A.copy(), B.copy()
p0, pn = B2.index[:3], B2.index[3:6]
B2.loc[p0, 'B_131'] = 0.0          # MaxQuant/PD-style 0 = not quantified
B2.loc[pn, 'B_131'] = np.nan       # missing reporter
sl2 = [sample_loading_normalize(A2), sample_loading_normalize(B2)]
br2 = irs_scale(sl2, ['A_131', 'B_131'])
print('\nstress: B_131 = 0 for', list(p0), '| NaN for', list(pn))
print('  plex B rows after IRS (ref = 0):\n', br2[1].loc[p0].iloc[:, :4].to_string())
print('  plex B rows after IRS (ref = NaN):\n', br2[1].loc[pn].iloc[:, :4].to_string())
print('  plex A rows for the same proteins (geomean now = plex A ref only):\n', (br2[0].loc[p0.append(pn)].iloc[:, :3] / sl2[0].loc[p0.append(pn)].iloc[:, :3]).round(3).to_string())
lb = np.log2(br2[1])
print(f'  log2 of bridged plex B: +inf cells = {int(np.isposinf(lb.values).sum())}, NaN cells = {int(lb.isna().sum().sum())}')
print('  column medians of log2 bridged plex B still finite?', bool(np.isfinite(lb.median()).all()),
      '| column means finite?', bool(np.isfinite(lb.mean()).all()))
# SL on a plex that contains a NaN reporter: target and factors
print('  SL factors plex B with NaNs (sum skips NaN):', (sl2[1].sum() / B2.sum()).round(4).tolist()[:4], '...')
