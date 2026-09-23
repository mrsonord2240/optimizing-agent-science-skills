"""
Re-audit regression input A (independent of both the original auditor's input3
and the fixer's verification run): build a fresh h5ad with a genuine `.raw`
snapshot from real 10x PBMC 1k v3 filtered data, using different parameters
(800 HVGs instead of 500, a different random seed for PCA) than either prior
run, so this is not just replaying someone else's saved file.
"""
import scanpy as sc
import numpy as np

RAW_H5 = "F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/public-data/pbmc_1k_v3_filtered_feature_bc_matrix.h5"
OUT = "F:/OpenScience/audits/bio-single-cell-data-io/data/ra1_rich.h5ad"

adata = sc.read_10x_h5(RAW_H5)
adata.var_names_make_unique()
print("Loaded filtered:", adata.shape)

adata.layers["counts"] = adata.X.copy()
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)

# categorical obs column, single value (probes sceasy-style coercion note elsewhere,
# but here just a realistic metadata column)
adata.obs["batch"] = "batchA"
adata.obs["batch"] = adata.obs["batch"].astype("category")

# freeze full-gene snapshot BEFORE HVG subsetting -> this is the .raw this test targets
adata.raw = adata

sc.pp.highly_variable_genes(adata, n_top_genes=800)
adata = adata[:, adata.var["highly_variable"]].copy()
sc.pp.pca(adata, n_comps=15, random_state=7)

print("Post-HVG shape:", adata.shape)
print("raw shape:", adata.raw.shape)
print("obsm keys:", list(adata.obsm.keys()))

adata.write_h5ad(OUT, compression="gzip")
print("Wrote", OUT)
