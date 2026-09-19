"""Re-audit: run the FIXED hashsolo pattern (post fix/sc-hashing, commit 0de5e44) on the
same fresh 2-tag data as baseline_unfixed_hashsolo.py, to confirm the fix genuinely
resolves the silent-Negative failure on data the fixer never saw.
"""
import pandas as pd
import numpy as np
import scanpy as sc
import scanpy.external as sce
import anndata as ad

df = pd.read_csv("hto_2tag_fresh.csv", index_col=0)
hto_cols = ["TAG_1", "TAG_2"]
truth_class = df["true_class"]
truth_sample = df["true_sample"]

rng = np.random.default_rng(1)
X = rng.poisson(1.5, size=(len(df), 200)).astype(float)
adata = ad.AnnData(X=X, obs=pd.DataFrame(index=df.index))
adata.obs[hto_cols] = df[hto_cols]

# FIXED pattern per single-cell/hashing-demultiplexing/SKILL.md @ 0de5e44
sce.pp.hashsolo(adata, cell_hashing_columns=hto_cols, priors=(0.01, 0.8, 0.19),
                 number_of_noise_barcodes=1 if len(hto_cols) <= 3 else None)

classification = adata.obs["Classification"].value_counts()
print("=== FIXED pattern: hashsolo Classification ===")
print(classification)
neg_frac = classification.get("Negative", 0) / len(adata)
print(f"Negative fraction: {neg_frac:.3f}")
if neg_frac > 0.9:
    raise RuntimeError("hashsolo classified >90% of cells Negative - guard would fire here")

pred_map = {"Negative": "negative", "Doublet": "doublet"}
pred_class = adata.obs["Classification"].map(lambda x: pred_map.get(x, "singlet"))
agree = (pred_class.values == truth_class.values)
print(f"Global class agreement with ground truth: {agree.sum()} / {len(agree)} = {agree.mean():.3f}")

both_singlet = (pred_class == "singlet") & (truth_class == "singlet")
sample_pred = adata.obs.loc[both_singlet, "Classification"]
sample_agree = (sample_pred.values == truth_sample[both_singlet].values)
print(f"Singlet sample-ID agreement: {sample_agree.sum()} / {len(sample_agree)} = "
      f"{(sample_agree.mean() if len(sample_agree) else float('nan')):.3f}")

# Reproducibility check: rerun to confirm determinism (T3 gate)
adata2 = ad.AnnData(X=X, obs=pd.DataFrame(index=df.index))
adata2.obs[hto_cols] = df[hto_cols]
sce.pp.hashsolo(adata2, cell_hashing_columns=hto_cols, priors=(0.01, 0.8, 0.19),
                 number_of_noise_barcodes=1)
same = (adata.obs["Classification"].values == adata2.obs["Classification"].values).all()
print(f"Determinism check (identical input, 2 runs): classifications identical = {same}")
