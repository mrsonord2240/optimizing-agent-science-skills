"""Prepare a small, stratified synthetic fixture for post-fix executable validation."""
from pathlib import Path
import numpy as np
import pandas as pd
import scanpy as sc

DATA = Path(r"F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples")
SOURCE = DATA / "all_samples_filtered.h5ad"
OUT = Path(r"F:/OpenScience/audits/bio-single-cell-batch-integration/run/re_audit_subset.h5ad")
rng = np.random.default_rng(20260924)
adata = sc.read_h5ad(SOURCE)
take = []
for batch in sorted(adata.obs["batch"].unique()):
    ids = np.flatnonzero(adata.obs["batch"].to_numpy() == batch)
    take.extend(rng.choice(ids, size=min(200, len(ids)), replace=False))
adata = adata[np.sort(take)].copy()
truth = pd.read_csv(DATA / "truth_cells.csv").set_index("cell_id")
adata.obs["cell_type"] = truth.loc[adata.obs_names, "true_cell_type"].to_numpy()
labels = pd.Categorical(adata.obs["cell_type"].astype(str))
masked = rng.random(adata.n_obs) < 0.4
labels = labels.astype(object)
labels[masked] = "Unknown"
adata.obs["cell_type_partial"] = pd.Categorical(labels)
adata.write_h5ad(OUT)
print(f"prepared {adata.n_obs} cells; batches={adata.obs['batch'].value_counts().to_dict()}; unknown={masked.sum()}")
