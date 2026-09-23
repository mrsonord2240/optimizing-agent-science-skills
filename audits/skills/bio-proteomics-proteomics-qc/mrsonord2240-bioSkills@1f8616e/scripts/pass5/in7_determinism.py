# Pass-5 confirmation audit, Input 7 (NEW this pass).
# Researcher request: "Our QC PCA printed p=0.0000 for PC3 ~ batch yesterday and something else today,
# on the same file. Is our data unstable, or is your code?"
#
# Tests the fixer's claim that PCA is now seeded: "six unseeded fits gave six p-values, seeded gives one."
# (a) the FIXED SKILL.md pca_batch_check, called 6x -> stdout must be byte-identical
# (b) the PRE-FIX construction `PCA(n_components=n_pc)` on the same matrix, 6x -> must vary
# (c) the same on a wide 20x600 matrix, the shape the fixed SKILL.md's Common Errors row cites
import io, contextlib, sys
import numpy as np, pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy.stats import f_oneway
from skill import S

D = '../data/'
pg = pd.read_csv(D + 'proteinGroups.txt', sep='\t', low_memory=False)
info = pd.read_csv(D + 'sample_annotation.csv').set_index('sample')
clean = S['strip_contaminant_rows'](pg)
lfq = clean[[f'LFQ intensity {s}' for s in info.index]].replace(0, np.nan)
lfq.columns = info.index
log2 = np.log2(lfq)
filt = S['completeness_filter'](log2, info['condition'], 0.7).dropna(how='any')
print(f'matrix: {filt.shape[0]} complete proteins x {filt.shape[1]} samples')

print('\n(a) FIXED SKILL.md pca_batch_check, 6 identical calls:')
outs = []
for _ in range(6):
    b = io.StringIO()
    with contextlib.redirect_stdout(b):
        S['pca_batch_check'](filt, info, batch_col='batch')
    outs.append(b.getvalue())
print('   distinct stdout across 6 runs:', len(set(outs)))
print('   ' + outs[0].strip().replace('\n', '\n   '))

print('\n(b) PRE-FIX construction PCA(n_components=n_pc) -- no svd_solver, no random_state -- 6 calls:')


def prefix_pca(mat, sample_info, batch_col='batch'):
    complete = mat.dropna(how='any')
    n_samples = mat.shape[1]
    n_pc = min(5, n_samples - 1)
    scaled = StandardScaler().fit_transform(complete.T)
    pcs = PCA(n_components=n_pc).fit(scaled)            # exactly the pre-fix line
    coords = pd.DataFrame(pcs.transform(scaled), columns=[f'PC{i+1}' for i in range(n_pc)],
                          index=complete.columns).join(sample_info)
    ps = []
    for pc in coords.columns[:min(3, n_pc)]:
        groups = [coords[coords[batch_col] == b][pc] for b in coords[batch_col].unique()]
        ps.append(f_oneway(*groups)[1])
    return ps


rows = [prefix_pca(filt, info) for _ in range(6)]
for i, r in enumerate(rows):
    print('   run %d: ' % (i + 1) + '  '.join(f'PC{j+1} p={v:.6f}' for j, v in enumerate(r)))
print('   distinct PC3 p-values across 6 unseeded runs:', len({round(r[2], 9) for r in rows}))

print('\n(c) wide 20 x 600 matrix (the shape SKILL.md cites), unseeded vs seeded:')
rng = np.random.default_rng(1)
M = pd.DataFrame(rng.normal(size=(600, 20)), columns=[f's{i}' for i in range(20)])
bi = pd.DataFrame({'batch': ['b1'] * 10 + ['b2'] * 10}, index=M.columns)
M.loc[:, bi.index[:10]] += rng.normal(0.4, 0.05, size=(600, 1))   # a real PC1 batch effect
u = [prefix_pca(M, bi) for _ in range(6)]
print('   unseeded distinct PC3 p-values:', len({round(r[2], 9) for r in u}),
      '| values:', [f'{r[2]:.5f}' for r in u])
s = []
for _ in range(6):
    b = io.StringIO()
    with contextlib.redirect_stdout(b):
        S['pca_batch_check'](M, bi, batch_col='batch')
    s.append(b.getvalue())
print('   SEEDED (fixed SKILL.md) distinct stdout:', len(set(s)))
print('   ' + s[0].strip().replace('\n', '\n   '))
