"""INPUT 2: score S05/S06 output on planted v2 truth. arg: planted|null"""
import sys, numpy as np, pandas as pd, scanpy as sc
mode = sys.argv[1]; R = '/mnt/openscience/audits/bio-single-cell-splicing/run'
a = sc.read_h5ad(f'{R}/out/in2_{mode}/brie_quant.h5ad'); truth = pd.read_csv(f'{R}/data/v2_{mode}/truth.tsv', sep='\t', keep_default_na=False).set_index('gene')
cells = pd.read_csv(f'{R}/data/v2_{mode}/cells.tsv', sep='\t').set_index('cell')
lrt = pd.DataFrame({'ELBO_gain': a.varm['ELBO_gain'][:, 0], 'pval': a.varm['pval'][:, 0], 'fdr': a.varm['fdr'][:, 0], 'cell_coeff': a.varm['cell_coeff'][:, 0]}, index=a.var_names)
t = truth.loc[a.var_names]; lrt['cls'] = t.cls; lrt['dtrue'] = t.psiB - t.psiA   # grp01=1 is B
print('events kept by the silent gene filter:', a.n_vars, 'of', len(truth), '; by class', lrt.cls.value_counts().to_dict(), ' (planted totals', truth.cls.value_counts().to_dict(), ')')
print(lrt.groupby('cls').agg(n=('fdr', 'size'), fdr05=('fdr', lambda x: int((x < .05).sum())), p05=('pval', lambda x: int((x < .05).sum())), elbo_gt3=('ELBO_gain', lambda x: int((x > 3).sum()))))
hits = lrt[lrt.fdr < 0.05]
pl = lrt[lrt.cls != 'null']
if len(pl):
    print('sign(cell_coeff)==sign(psiB-psiA) among planted fdr<0.05:', (np.sign(pl[pl.fdr < .05].cell_coeff) == np.sign(pl[pl.fdr < .05].dtrue)).mean().round(3), 'n', int((pl.fdr < .05).sum()))
    print('FDP among fdr<0.05 calls:', round((hits.cls == 'null').sum() / max(len(hits), 1), 3))
dense = lambda m: np.asarray(m.todense() if hasattr(m, 'todense') else m)
i1, i2 = dense(a.layers['isoform1']), dense(a.layers['isoform2']); u = i1 + i2
psi = a.layers['Psi']; low = cells.loc[a.obs_names, 'lowcov'].values.astype(bool); grp = cells.loc[a.obs_names, 'group'].values
tp = np.array([[truth.loc[g, 'psiA'] if gr == 'A' else truth.loc[g, 'psiB'] for g in a.var_names] for gr in grp])
print(f'mean|Psi - true group PSI|: normal cells {np.abs(psi[~low] - tp[~low]).mean():.3f}, low-coverage cells {np.abs(psi[low] - tp[low]).mean():.3f}; unique reads/event: normal {u[~low].mean():.2f}, low {u[low].mean():.2f}')
gA = grp == 'A'; gB = ~gA
pA = i1[gA].sum(0) / np.maximum(u[gA].sum(0), 1); pB = i1[gB].sum(0) / np.maximum(u[gB].sum(0), 1)
naive = pd.Series(pB - pA, index=a.var_names)
if len(pl):
    print('independent naive pooled count-PSI (isoform1/(iso1+iso2)) dPSI vs planted dPSI, Pearson:', np.corrcoef(naive[pl.index], pl.dtrue)[0, 1].round(3))
if mode == 'planted':
    big = lrt[lrt.cls == 'big']; assert (big.fdr < .05).mean() >= .8, 'big effects missed'
    print('ASSERT OK: >=80% of big planted events at fdr<0.05:', int((big.fdr < .05).sum()), '/', len(big))
else:
    print('NULL RESULT: events', len(lrt), 'fdr<0.05', int((lrt.fdr < .05).sum()), 'raw p<0.05', int((lrt.pval < .05).sum()), 'ELBO_gain>3', int((lrt.ELBO_gain > 3).sum()))
    assert (lrt.fdr < .05).sum() == 0
