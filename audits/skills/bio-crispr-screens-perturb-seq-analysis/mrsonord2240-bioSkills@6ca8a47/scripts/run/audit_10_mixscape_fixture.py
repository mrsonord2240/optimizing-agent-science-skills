"""Fresh fixture for the shipped mixscape_filter.py CLI."""
from pathlib import Path
import numpy as np
import anndata as ad
import scanpy as sc

out = Path(r"F:\OpenScience\audits\bio-crispr-screens-perturb-seq-analysis\data\mixscape_fixture.h5ad")
rng = np.random.default_rng(2026092310)
n_control, n_ko, genes = 160, 160, 60
x = rng.poisson(3, size=(n_control + n_ko, genes)).astype(np.int32)
x[n_control:, :12] += rng.poisson(10, size=(n_ko, 12))
adata = ad.AnnData(x)
adata.obs["sgrna_assignment"] = ["NTC"] * n_control + ["GENE_A"] * n_ko
adata.var_names = [f"g{i}" for i in range(genes)]
sc.pp.normalize_total(adata)
sc.pp.log1p(adata)
adata.write_h5ad(out)
print(f"wrote={out} cells={adata.n_obs} genes={adata.n_vars}")
