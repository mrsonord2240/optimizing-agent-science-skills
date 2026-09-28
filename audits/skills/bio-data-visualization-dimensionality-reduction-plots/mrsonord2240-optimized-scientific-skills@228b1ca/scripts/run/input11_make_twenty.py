"""New input 11: create an exact-boundary raw-count dataset with 20 conditions."""
from __future__ import annotations

from pathlib import Path

import anndata as ad
import numpy as np
import pandas as pd

ROOT = Path(r"F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots\run\twenty")
rng = np.random.default_rng(20260927)
n_cells, n_genes, n_groups = 100, 2_000, 20
groups = np.arange(n_cells) % n_groups
base = rng.gamma(0.8, 1.2, n_genes)
fold = np.ones((n_cells, n_genes))
for group in range(n_groups):
    start = group * 15
    fold[np.ix_(groups == group, np.arange(start, start + 15))] = 5
counts = rng.poisson(base[None, :] * fold).astype(np.int32)
obs = pd.DataFrame(
    {"condition": pd.Categorical([f"condition_{group:02d}" for group in groups])},
    index=[f"cell_{index:03d}" for index in range(n_cells)],
)
adata = ad.AnnData(
    counts,
    obs=obs,
    var=pd.DataFrame(index=[f"gene_{index:04d}" for index in range(n_genes)]),
)
path = ROOT / "boundary_100x2000_20conditions.h5ad"
adata.write_h5ad(path)
print(f"wrote {path}: shape={adata.shape}, conditions={adata.obs['condition'].nunique()}")
assert adata.obs["condition"].nunique() == 20
