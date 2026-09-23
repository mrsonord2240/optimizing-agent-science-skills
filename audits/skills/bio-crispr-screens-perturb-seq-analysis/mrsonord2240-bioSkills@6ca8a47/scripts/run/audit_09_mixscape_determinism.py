"""Fresh separate-process determinism target for pertpy Mixscape signatures."""
from pathlib import Path
import sys
import numpy as np
import anndata as ad
import pertpy as pt

out = Path(sys.argv[1])
rng = np.random.default_rng(2026092309)
n_control, n_ko, genes = 90, 90, 50
x = rng.poisson(3, size=(n_control + n_ko, genes)).astype(float)
x[n_control:, :6] += 9
adata = ad.AnnData(x)
adata.obs["guide"] = ["NTC"] * n_control + ["GENE_A"] * n_ko
mix = pt.tl.Mixscape()
mix.perturbation_signature(adata, pert_key="guide", control="NTC", n_neighbors=20, random_state=0)
np.save(out, adata.layers["X_pert"])
print(f"saved={out} shape={adata.layers['X_pert'].shape} sum={float(adata.layers['X_pert'].sum()):.6f}")
