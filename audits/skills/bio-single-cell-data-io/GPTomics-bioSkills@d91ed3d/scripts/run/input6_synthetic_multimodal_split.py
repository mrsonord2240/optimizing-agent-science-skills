"""
Input 6 (Scope Boundary) - "Load the raw 10X matrix but keep CRISPR guide and antibody
features separate from gene expression, and save each to its own file."

The real cached PBMC 1k v3 dataset is GEX-only (confirmed in Input 1: feature_types has
only 'Gene Expression'), so it cannot exercise the gex_only=False / feature_types split
path SKILL.md documents. This is a SYNTHETIC minimal multi-modal object (50 genes +
10 antibody-capture features x 20 cells) built to test that exact documented pattern:
    adata = sc.read_10x_h5(..., gex_only=False)
    # split later by adata.var['feature_types']
"""
import anndata as ad
import numpy as np
import pandas as pd
import scipy.sparse as sp

rng = np.random.default_rng(1)
n_cells, n_genes, n_adt = 20, 50, 10
n_vars = n_genes + n_adt

X = sp.random(n_cells, n_vars, density=0.3, format="csr", random_state=1, data_rvs=lambda s: rng.integers(1, 20, size=s))
var = pd.DataFrame({
    "gene_ids": [f"ENSG{i:05d}" for i in range(n_genes)] + [f"ADT{i:03d}" for i in range(n_adt)],
    "feature_types": ["Gene Expression"] * n_genes + ["Antibody Capture"] * n_adt,
}, index=[f"GENE{i}" for i in range(n_genes)] + [f"CD{i}" for i in range(n_adt)])
obs = pd.DataFrame(index=[f"CELL{i}" for i in range(n_cells)])

adata = ad.AnnData(X=X.astype("float32"), obs=obs, var=var)
print(f"Synthetic combined object: {adata.n_obs} cells x {adata.n_vars} features")
print(adata.var["feature_types"].value_counts())

# Exercise the documented split-by-feature_types pattern
gex = adata[:, adata.var["feature_types"] == "Gene Expression"].copy()
adt = adata[:, adata.var["feature_types"] == "Antibody Capture"].copy()
print(f"\nGEX split: {gex.n_obs} x {gex.n_vars} (expect {n_cells} x {n_genes})")
print(f"ADT split: {adt.n_obs} x {adt.n_vars} (expect {n_cells} x {n_adt})")

assert gex.n_vars == n_genes and adt.n_vars == n_adt, "split lost or gained features"
assert gex.n_obs == n_cells and adt.n_obs == n_cells, "cell count changed by var-slicing"
print("\nOK: feature_types split preserved exact cell count and partitioned genes/ADT correctly.")

gex.write_h5ad(r"F:\OpenScience\audits\bio-single-cell-data-io\data\input6_gex.h5ad")
adt.write_h5ad(r"F:\OpenScience\audits\bio-single-cell-data-io\data\input6_adt.h5ad")
print("Wrote input6_gex.h5ad and input6_adt.h5ad")
