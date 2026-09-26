"""Prepare the exact four-lane SingleR query as a sparse Matrix Market input without Seurat."""
from pathlib import Path

import pandas as pd
import scanpy as sc
from scipy.io import mmwrite

DATA = Path(r"F:\OpenScience\audits\_partial-20260911\bio-workflows-scrnaseq-pipeline\data\synthetic_pbmc_8samples")
OUT = Path(r"F:\OpenScience\audits\bio-single-cell-cell-annotation\reaudit-optimized-scientific-skills@2dee47f-20260925\data")
a = sc.read_h5ad(DATA / "all_samples_filtered.h5ad")
truth = pd.read_csv(DATA / "truth_cells.csv").set_index("cell_id").loc[a.obs_names]
keep = a.obs["sample"].astype(str).isin(["S1", "S2", "S3", "S4"])
keep &= ~truth["true_doublet"].astype(bool) & ~truth["true_low_quality"].astype(bool)
a = a[keep.values].copy()
truth = truth.loc[a.obs_names]
mmwrite(OUT / "input2_counts.mtx", a.X.T)
pd.Series(a.var_names).to_csv(OUT / "input2_genes.tsv", sep="\t", index=False, header=False)
pd.DataFrame({"cell_id": a.obs_names, "true_cell_type": truth["true_cell_type"].astype(str).values}).to_csv(
    OUT / "input2_cells.csv", index=False
)
print(f"prepared_sparse_matrix={a.n_vars}x{a.n_obs}")
