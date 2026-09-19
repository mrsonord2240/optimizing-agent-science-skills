import scanpy as sc
import scvelo as scv
adata = sc.read_h5ad('../data/pancreas_raw.h5ad')
scv.pp.filter_and_normalize(adata, min_shared_counts=20)
adata.layers['normalized_X'] = adata.X.copy()
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)
adata = adata[:, adata.var['highly_variable']].copy()
adata.X = adata.layers.pop('normalized_X')
scv.pp.moments(adata, n_pcs=30, n_neighbors=30)
try:
    scv.tl.recover_dynamics(adata, var_names=adata.var_names.to_numpy())
    print('WORKAROUND SUCCEEDED with var_names=ndarray')
except Exception as e:
    print('WORKAROUND with ndarray FAILED:', type(e).__name__, e)
