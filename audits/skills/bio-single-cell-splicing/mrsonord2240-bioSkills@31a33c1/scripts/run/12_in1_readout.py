"""INPUT 1: show what SKILL.md block S06 (BRIE2 readout) yields on the real brie_quant.h5ad, and cross-check fdr against an independent LRT p-value BH."""
import scanpy as sc, pandas as pd, numpy as np
from statsmodels.stats.multitest import multipletests
a = sc.read_h5ad('/mnt/openscience/audits/bio-single-cell-splicing/run/out/in1/brie_quant.h5ad')
lrt = pd.DataFrame({'ELBO_gain': a.varm['ELBO_gain'][:, 0], 'pval': a.varm['pval'][:, 0], 'fdr': a.varm['fdr'][:, 0], 'cell_coeff': a.varm['cell_coeff'][:, 0]}, index=a.var_names)
print(lrt.sort_values('fdr').head(5).round(4)); print('n fdr<0.05 (random group covariate):', int((lrt.fdr < 0.05).sum()), ' raw p<0.05:', int((lrt.pval < 0.05).sum()))
bh = multipletests(lrt.pval, method='fdr_bh')[1]
print('fdr vs independent BH of pval, max abs diff:', np.abs(bh - lrt.fdr).max().round(4))
# second column = log_depth covariate
lrt2 = pd.DataFrame({'ELBO_gain': a.varm['ELBO_gain'][:, 1], 'pval': a.varm['pval'][:, 1], 'fdr': a.varm['fdr'][:, 1]}, index=a.var_names)
print('log_depth covariate: n fdr<0.05', int((lrt2.fdr < 0.05).sum()))
psi = a.layers['Psi']; print('Psi range', np.nanmin(psi).round(3), np.nanmax(psi).round(3), 'nan', int(np.isnan(psi).sum()), '95CI', a.layers['Psi_95CI'].mean().round(3), 'Z_std', a.layers['Z_std'].mean().round(3))
assert np.nanmin(psi) >= 0 and np.nanmax(psi) <= 1
