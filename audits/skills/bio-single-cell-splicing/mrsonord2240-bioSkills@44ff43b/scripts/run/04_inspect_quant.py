"""Input 1 step D: what does brie-quant actually write? Run the Skill's snippet `sc.read_h5ad(...)` + inspection, then test the example script helper functions."""
import sys, numpy as np, pandas as pd, scanpy as sc
R='/mnt/openscience/audits/bio-single-cell-splicing/run'
ad_ = sc.read_h5ad(f'{R}/out/real_quant.h5ad')
print(ad_)
print('varm keys', list(ad_.varm.keys()))
print('var cols', list(ad_.var.columns))
print('layers', list(ad_.layers.keys()))
print('obsm', list(ad_.obsm.keys()) if hasattr(ad_,'obsm') else None)
print('uns keys', list(ad_.uns.keys()))
print(ad_.var.head(4).T)
for k in ad_.varm.keys():
    print(k, ad_.varm[k].shape if hasattr(ad_.varm[k],'shape') else type(ad_.varm[k]))
Psi=ad_.layers['Psi']
print('Psi range', np.nanmin(Psi), np.nanmax(Psi), 'nan frac', np.isnan(Psi).mean())
