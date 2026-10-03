import scanpy as sc, numpy as np
a=sc.read_h5ad('work/f_none/query_annotated.h5ad'); b=sc.read_h5ad('work/f_none2/query_annotated.h5ad')
print('shape',a.shape,'obs cols',list(a.obs.columns))
print('labels identical',(a.obs.predicted_label.astype(str).values==b.obs.predicted_label.astype(str).values).mean(),'n',a.n_obs)
print('latent maxdiff',float(np.abs(a.obsm['X_scANVI']-b.obsm['X_scANVI']).max()))
print('uncert maxdiff',float(np.abs(a.obs.transfer_uncertainty.values-b.obs.transfer_uncertainty.values).max()))
