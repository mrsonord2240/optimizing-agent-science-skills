"""Phase 2 input 3: seeded E-distance/E-test on a planted perturbation effect."""
import numpy as np
import anndata as ad
import pertpy as pt
import scanpy as sc

rng = np.random.default_rng(23)
x = np.vstack([rng.normal(0, 1, (80, 12)), rng.normal(1.2, 1, (80, 12))])
adata = ad.AnnData(x)
adata.obs["gene_target"] = ["NT"] * 80 + ["STAT1"] * 80
sc.pp.pca(adata, n_comps=8)
np.random.seed(23)
result = pt.tl.DistanceTest("edistance", n_perms=99)(adata, groupby="gene_target", contrast="NT")
print(result.to_string())
assert result["pvalue"].min() <= 0.05
print(f"PASS E-test planted effect: columns={list(result.columns)}, min_pvalue={result['pvalue'].min():.4f}")
