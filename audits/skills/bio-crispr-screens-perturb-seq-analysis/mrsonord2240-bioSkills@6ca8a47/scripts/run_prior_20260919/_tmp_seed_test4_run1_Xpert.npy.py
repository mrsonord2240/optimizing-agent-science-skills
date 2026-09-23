
import numpy as np, pandas as pd, anndata as ad, pertpy as pt

rng = np.random.default_rng(90210)  # fixed data-generation seed so both runs see identical input
n_cells = 1500
n_genes = 250
group = np.array((["PERT"] * (n_cells // 2)) + (["NT"] * (n_cells - n_cells // 2)))
rng.shuffle(group)
baseline = rng.uniform(5, 200, size=n_genes)
X = np.zeros((n_cells, n_genes))
for i in range(n_cells):
    mult = np.where(group[i] == "PERT", 1.8, 1.0)
    X[i, :] = rng.poisson(baseline * mult)

adata = ad.AnnData(X=X, obs=pd.DataFrame({"gene_target": group}, index=[f"c{i}" for i in range(n_cells)]),
                    var=pd.DataFrame(index=[f"g{i}" for i in range(n_genes)]))
adata.layers["counts"] = X.copy()

import scanpy as sc
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=100)

ms = pt.tl.Mixscape()
ms.perturbation_signature(adata=adata, pert_key="gene_target", control="NT", n_neighbors=20, random_state=0)

np.save(r"test4_run1_Xpert.npy", adata.layers["X_pert"])
print("wrote", r"test4_run1_Xpert.npy", adata.layers["X_pert"].shape)
