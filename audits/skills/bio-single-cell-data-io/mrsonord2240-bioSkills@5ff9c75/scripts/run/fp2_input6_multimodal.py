"""Phase-2 Input 6: synthetic GEX+ADT feature partition with exact accounting."""
import numpy as np
import pandas as pd
import anndata as ad
from scipy import sparse
rng = np.random.default_rng(5)
x = sparse.csr_matrix(rng.poisson(1, size=(20, 60)).astype('int32'))
var = pd.DataFrame({'feature_types': ['Gene Expression'] * 50 + ['Antibody Capture'] * 10}, index=[f'f{i}' for i in range(60)])
adata = ad.AnnData(X=x, var=var)
gex = adata[:, adata.var['feature_types'].eq('Gene Expression')].copy()
adt = adata[:, adata.var['feature_types'].eq('Antibody Capture')].copy()
print('original', adata.shape, 'gex', gex.shape, 'adt', adt.shape, 'sum_features', gex.n_vars + adt.n_vars)
assert gex.shape == (20, 50) and adt.shape == (20, 10)
assert gex.n_vars + adt.n_vars == adata.n_vars
assert set(gex.var_names).isdisjoint(set(adt.var_names))
print('PASS input6')
