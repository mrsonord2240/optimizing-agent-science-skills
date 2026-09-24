import inspect, numpy as np
import scanpy.external as sce, harmonypy
print('harmony_integrate sig:', inspect.signature(sce.pp.harmony_integrate))
print('run_harmony sig:', inspect.signature(harmonypy.run_harmony))
import scanpy as sc, pandas as pd
a = sc.read_h5ad(r'F:/OpenScience/audits/bio-single-cell-batch-integration/run/input1_harmony.h5ad')
for th in [0.0, 0.5, 8.0, 50.0]:
    r = harmonypy.run_harmony(a.obsm['X_pca'], a.obs, ['batch'], theta=th, max_iter_harmony=20)
    Z = np.asarray(r.Z_corr).T
    d = np.abs(Z - a.obsm['X_pca']).mean()
    print(f'theta={th}: mean |correction| = {d:.6f}, first cell PC1 = {Z[0,0]:.6f}')
