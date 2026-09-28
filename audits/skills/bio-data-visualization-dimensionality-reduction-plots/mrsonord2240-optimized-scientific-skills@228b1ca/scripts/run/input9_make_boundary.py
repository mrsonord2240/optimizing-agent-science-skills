"""New input 9: create a valid minimum-shape raw-count dataset with 12 conditions."""
from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import anndata as ad

ROOT = Path(r"F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots\run\boundary")
rng = np.random.default_rng(99)
n_cells, n_genes, n_groups = 100, 2_000, 12
groups = np.arange(n_cells) % n_groups
base = rng.gamma(0.8, 1.2, n_genes)
fold = np.ones((n_cells, n_genes))
for group in range(n_groups):
    fold[np.ix_(groups == group, np.arange(group * 20, (group + 1) * 20))] = 5
counts = rng.poisson(base[None, :] * fold).astype(np.int32)
obs = pd.DataFrame(
    {"condition": pd.Categorical([f"condition_{group:02d}" for group in groups])},
    index=[f"cell_{i:03d}" for i in range(n_cells)],
)
adata = ad.AnnData(counts, obs=obs, var=pd.DataFrame(index=[f"gene_{j:04d}" for j in range(n_genes)]))
path = ROOT / "boundary_100x2000_12conditions.h5ad"
adata.write_h5ad(path)
print(f"wrote {path}: {adata.shape}, conditions={adata.obs['condition'].nunique()}, integer={np.allclose(counts, np.round(counts))}")
