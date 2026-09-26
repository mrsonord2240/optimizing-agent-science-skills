"""Canonical regression: prepare the prior synthetic PBMC fixture for the shipped CLI."""
import json
from pathlib import Path

import pandas as pd
import scanpy as sc

DATA = Path(r"F:\OpenScience\audits\_partial-20260911\bio-workflows-scrnaseq-pipeline\data\synthetic_pbmc_8samples")
OUT = Path(r"F:\OpenScience\audits\bio-single-cell-cell-annotation\reaudit-optimized-scientific-skills@2dee47f-20260925\data")

a = sc.read_h5ad(DATA / "all_samples_filtered.h5ad")
truth = pd.read_csv(DATA / "truth_cells.csv").set_index("cell_id").loc[a.obs_names]
a.obs["true_cell_type"] = truth["true_cell_type"].astype(str).values
keep = ~(truth["true_doublet"].astype(bool) | truth["true_low_quality"].astype(bool))
a = a[keep.values].copy()
a.layers["counts"] = a.X.copy()
sc.pp.normalize_total(a, target_sum=1e4)
sc.pp.log1p(a)
sc.pp.highly_variable_genes(a, n_top_genes=2000, flavor="seurat_v3", layer="counts")
sc.tl.pca(a, n_comps=50, mask_var="highly_variable", random_state=17)
sc.pp.neighbors(a, random_state=17)
sc.tl.leiden(a, resolution=1.2, flavor="igraph", n_iterations=2, directed=False, random_state=17)
sc.tl.umap(a, random_state=17)
a.write_h5ad(OUT / "input1_clustered.h5ad")
(OUT / "input1_seed.json").write_text(
    json.dumps({"seed": 17, "cells": a.n_obs, "genes": a.n_vars, "clusters": int(a.obs["leiden"].nunique())}, indent=2),
    encoding="utf-8",
)
print(f"prepared cells={a.n_obs} genes={a.n_vars} clusters={a.obs['leiden'].nunique()} seed=17")
