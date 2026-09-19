"""Input 2 (Variant A) -- "I have 2 hashtags in my scanpy AnnData object with raw HTO
counts in adata.obs. Use hashsolo in scanpy to assign samples when I only have two
hashtags." Follows the Skill's examples/hashsolo_scanpy.py pattern, applied to a
synthetic 2-tag dataset with known ground truth (not real experimental data).
"""
import numpy as np
import pandas as pd
import scanpy as sc
import scanpy.external as sce
import anndata as ad

rng = np.random.default_rng(20260919 + 4)

# --- synthetic 2-tag HTO dataset (equal pooling, moderate background) ---
n_cells = 900
tag_names = np.array(["HTO_A", "HTO_B"])
singlet_rate, doublet_rate = 0.85, 0.08
neg_rate = 1 - singlet_rate - doublet_rate
classes = rng.choice(["singlet", "doublet", "negative"], size=n_cells,
                      p=[singlet_rate, doublet_rate, neg_rate])
counts = np.zeros((n_cells, 2), dtype=int)
true_sample = []
for i, cls in enumerate(classes):
    bg = rng.poisson(10, size=2)
    counts[i] = bg
    if cls == "singlet":
        t = rng.integers(0, 2)
        counts[i, t] += rng.poisson(220)
        true_sample.append(tag_names[t])
    elif cls == "doublet":
        counts[i] += rng.poisson(180, size=2)
        true_sample.append("HTO_A+HTO_B")
    else:
        true_sample.append("Negative")

hto_cols = list(tag_names)
hto_df = pd.DataFrame(counts, columns=hto_cols,
                       index=[f"CELL_{i:05d}" for i in range(n_cells)])

# adata: minimal synthetic GEX matrix, HTOs attached as adata.obs columns per the Skill's pattern
X = rng.poisson(1.5, size=(n_cells, 200)).astype(float)
adata = ad.AnnData(X=X, obs=pd.DataFrame(index=hto_df.index))
adata.obs[hto_cols] = hto_df.loc[adata.obs_names, hto_cols]

sce.pp.hashsolo(adata, cell_hashing_columns=hto_cols, priors=(0.01, 0.8, 0.19))

classification = adata.obs["Classification"].value_counts()
print("=== hashsolo Classification ===")
print(classification)

doublet_rate_obs = (adata.obs["Classification"] == "Doublet").mean()
print(f"\nCross-sample doublet rate: {doublet_rate_obs:.3f}")

singlets = adata[~adata.obs["Classification"].isin(["Negative", "Doublet"])].copy()
print(f"\nSinglets subset shape: {singlets.shape}")

# --- accuracy against ground truth ---
pred_map = {"Negative": "negative", "Doublet": "doublet"}
pred_class = adata.obs["Classification"].map(lambda x: pred_map.get(x, "singlet"))
truth_class = pd.Series(classes, index=adata.obs_names)
agree = (pred_class.values == truth_class.values)
print(f"\nGlobal class agreement with ground truth: {agree.sum()} / {len(agree)} = {agree.mean():.3f}")

truth_sample = pd.Series(true_sample, index=adata.obs_names)
both_singlet = (pred_class == "singlet") & (truth_class == "singlet")
sample_pred = adata.obs.loc[both_singlet, "Classification"]
sample_agree = (sample_pred.values == truth_sample[both_singlet].values)
print(f"Singlet sample-ID agreement (both-singlet subset): {sample_agree.sum()} / {len(sample_agree)} = {sample_agree.mean() if len(sample_agree) else float('nan'):.3f}")

print("\n=== Confusion: predicted class (rows) vs ground truth (cols) ===")
print(pd.crosstab(pred_class, truth_class))
