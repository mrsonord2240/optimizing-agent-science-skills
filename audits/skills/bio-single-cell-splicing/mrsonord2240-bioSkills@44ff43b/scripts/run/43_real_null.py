"""Input 3 (edge): the real 130-cell Smart-seq2 brie-quant run with a RANDOM binary label (null) and a log-depth covariate. Count LRT hits."""
import scanpy as sc, numpy as np, pandas as pd
R='/mnt/openscience/audits/bio-single-cell-splicing/run'
a=sc.read_h5ad(f'{R}/out/real_quant.h5ad'); print(a.shape, 'of 50 events survive brie-quant gene filters (minCount 50, minUniq 10, minCell 30, minMIF 0.001)')
print('LRT columns present: ELBO_gain', a.varm['ELBO_gain'].shape, ' pval', a.varm['pval'].shape, ' fdr', a.varm['fdr'].shape, ' Xc_ids', list(a.uns['Xc_ids']))
for j,nm in enumerate(a.uns['Xc_ids']):
    e=a.varm['ELBO_gain'][:,j]; p=a.varm['pval'][:,j]; f=a.varm['fdr'][:,j]
    print(f'{nm}: n={len(p)}  raw p<0.05: {(p<0.05).sum()}  FDR<0.05: {(f<0.05).sum()}  ELBO_gain>3: {(e>3).sum()}  max ELBO_gain {e.max():.2f}')
psi=a.layers['Psi']; print('per-cell Psi 95% CI mean width (real data, mostly <5 reads/cell/event):', float(np.nanmean(a.layers['Psi_95CI'])) if a.layers['Psi_95CI'].ndim==2 else a.layers['Psi_95CI'].shape)
