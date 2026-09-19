"""Re-audit baseline: reproduce the ORIGINAL (pre-fix, unfixed) hashsolo pattern from the
pre-fix SKILL.md / examples/hashsolo_scanpy.py -- i.e. sce.pp.hashsolo() called WITHOUT
number_of_noise_barcodes on exactly 2 hashtags -- on fresh synthetic data to confirm the
silent-Negative failure still reproduces before judging whether the fix resolves it.
"""
import pandas as pd
import scanpy as sc
import scanpy.external as sce
import anndata as ad

df = pd.read_csv("hto_2tag_fresh.csv", index_col=0)
hto_cols = ["TAG_1", "TAG_2"]
truth_class = df["true_class"]
truth_sample = df["true_sample"]

X = df[hto_cols].values.astype(float) * 0 + 1.5  # dummy GEX matrix, unused by hashsolo
import numpy as np
rng = np.random.default_rng(1)
X = rng.poisson(1.5, size=(len(df), 200)).astype(float)
adata = ad.AnnData(X=X, obs=pd.DataFrame(index=df.index))
adata.obs[hto_cols] = df[hto_cols]

# ORIGINAL (unfixed) pattern -- no number_of_noise_barcodes argument
sce.pp.hashsolo(adata, cell_hashing_columns=hto_cols, priors=(0.01, 0.8, 0.19))

classification = adata.obs["Classification"].value_counts()
print("=== UNFIXED pattern: hashsolo Classification ===")
print(classification)
neg_frac = classification.get("Negative", 0) / len(adata)
print(f"Negative fraction: {neg_frac:.3f}")

pred_map = {"Negative": "negative", "Doublet": "doublet"}
pred_class = adata.obs["Classification"].map(lambda x: pred_map.get(x, "singlet"))
agree = (pred_class.values == truth_class.values)
print(f"Global class agreement with ground truth: {agree.sum()} / {len(agree)} = {agree.mean():.3f}")
