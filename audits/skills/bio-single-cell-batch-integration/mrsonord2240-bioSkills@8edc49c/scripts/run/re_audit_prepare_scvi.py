"""Add partially hidden synthetic truth labels for the exact-commit scVI/scANVI run."""
from pathlib import Path
import numpy as np
import pandas as pd
import scanpy as sc

data = Path(r"F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples")
adata = sc.read_h5ad(data / "all_samples_filtered.h5ad")
truth = pd.read_csv(data / "truth_cells.csv").set_index("cell_id")
adata.obs["cell_type_partial"] = truth.loc[adata.obs_names, "true_cell_type"].to_numpy()
rng = np.random.default_rng(20260924)
mask = rng.random(adata.n_obs) < 0.4
labels = adata.obs["cell_type_partial"].astype(str).to_numpy()
labels[mask] = "Unknown"
adata.obs["cell_type_partial"] = pd.Categorical(labels)
out = Path(r"F:/OpenScience/audits/bio-single-cell-batch-integration/run/re_audit_scvi_input.h5ad")
adata.write_h5ad(out)
print(f"prepared {adata.n_obs} cells; unknown={mask.sum()}")
