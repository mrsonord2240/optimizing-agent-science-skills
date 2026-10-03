import scanpy as sc, numpy as np
a=sc.read_h5ad(r"F:\OpenScience\audits\bio-machine-learning-atlas-mapping\reaudit-lane3b-20261003\scripts\work\r_none\query_annotated.h5ad")
b=sc.read_h5ad(r"F:\OpenScience\audits\bio-machine-learning-atlas-mapping\tooling-delta-lane3b-20261003\work\none1\query_annotated.h5ad")
print("labels identical:", (a.obs.predicted_label.astype(str).values==b.obs.predicted_label.astype(str).values).all(), "max latent diff", float(np.abs(a.obsm['X_scANVI']-b.obsm['X_scANVI']).max()))
t=a.obs.truth_coarse.astype(str).values if 'truth_coarse' in a.obs else None
p=a.obs.predicted_label.astype(str).values
print("shape",a.shape,"obs cols",list(a.obs.columns)); 
if t is not None: print("accuracy", (p==t).mean())
