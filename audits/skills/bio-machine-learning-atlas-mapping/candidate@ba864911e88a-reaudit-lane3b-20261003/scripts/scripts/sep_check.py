import scanpy as sc, numpy as np
a=sc.read_h5ad(r"F:\OpenScience\audits\bio-machine-learning-atlas-mapping\reaudit-lane3b-20261003\scripts\work\r_none\query_annotated.h5ad")
p=a.obs.predicted_label.astype(str).values; t=a.obs.truth_coarse.astype(str).values; u=a.obs.transfer_uncertainty.values
ok=p==t; print("acc",ok.mean(),"mean unc correct",u[ok].mean(),"wrong",u[~ok].mean(),"unknown",(p=='Unknown').mean())
