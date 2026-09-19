"""
Input 3 (Edge) - "Convert this AnnData to a SingleCellExperiment, keeping reducedDims
and raw, and confirm nothing silently changed axes or got dropped."

Step A (Python): build a realistic AnnData off the real PBMC 1k filtered matrix,
populated exactly the way SKILL.md's 'AnnData Object Structure' section instructs:
  - layers['counts'] = integer UMIs
  - X = log-normalized
  - .raw = frozen full-gene snapshot before HVG subsetting
  - obsm['X_pca'] = an embedding (stands in for a real reducedDim)
  - a categorical obs column (batch) -- SKILL.md/usage-guide warns categoricals can be
    coerced to character/NA on cross-ecosystem hops
Then subset to HVGs (so raw != X shape) and write h5ad, per the documented pattern.
"""
import scanpy as sc
import numpy as np
import pandas as pd

FILTERED_H5 = r"F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\public-data\pbmc_1k_v3_filtered_feature_bc_matrix.h5"
OUT = r"F:\OpenScience\audits\bio-single-cell-data-io\data\input3_rich.h5ad"

adata = sc.read_10x_h5(FILTERED_H5)
adata.var_names_make_unique()

# categorical batch label, deliberately single-value like a real single-sample object
# (usage-guide.md explicitly warns tools like sceasy drop single-value columns)
adata.obs["batch"] = pd.Categorical(["sample1"] * adata.n_obs)
adata.obs["pct_counts_mt"] = np.random.default_rng(0).uniform(0, 5, size=adata.n_obs)

adata.layers["counts"] = adata.X.copy()
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)

adata.raw = adata  # frozen full-gene log-norm snapshot

sc.pp.highly_variable_genes(adata, n_top_genes=500)
adata_hvg = adata[:, adata.var["highly_variable"]].copy()

# a fake embedding standing in for a real PCA/UMAP reducedDim
rng = np.random.default_rng(0)
adata_hvg.obsm["X_pca"] = rng.normal(size=(adata_hvg.n_obs, 10)).astype("float32")

print(f"Before write: X {adata_hvg.shape} (cells x genes)")
print(f"  layers: {list(adata_hvg.layers.keys())}")
print(f"  obsm: {list(adata_hvg.obsm.keys())}")
print(f"  raw: {adata_hvg.raw.shape if adata_hvg.raw is not None else None}")
print(f"  obs['batch'] dtype: {adata_hvg.obs['batch'].dtype}, unique: {adata_hvg.obs['batch'].unique().tolist()}")
print(f"  var columns: {list(adata_hvg.var.columns)}")

adata_hvg.write_h5ad(OUT, compression="gzip")
print(f"Wrote {OUT}")

# record ground truth for the round-trip check downstream
import json
truth = {
    "n_obs": int(adata_hvg.n_obs),
    "n_vars": int(adata_hvg.n_vars),
    "raw_n_vars": int(adata_hvg.raw.shape[1]),
    "has_counts_layer": "counts" in adata_hvg.layers,
    "has_obsm_pca": "X_pca" in adata_hvg.obsm,
    "batch_is_categorical_single_value": True,
}
with open(r"F:\OpenScience\audits\bio-single-cell-data-io\data\input3_truth.json", "w") as f:
    json.dump(truth, f, indent=2)
print("Ground truth:", truth)
