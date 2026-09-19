"""Regression check for Input 1 (raw 10x load, Python) -- unaffected by this fix."""
import scanpy as sc

RAW_H5 = "F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/public-data/pbmc_1k_v3_raw_feature_bc_matrix.h5"
adata = sc.read_10x_h5(RAW_H5, gex_only=False)
adata.var_names_make_unique()
print("RAW matrix:", adata.shape, "-- expect 6794880 x 33538")
assert adata.shape == (6794880, 33538)
import scipy.sparse as sp
assert sp.issparse(adata.X), "X should stay sparse"
print("CONFIRMED: Input 1 (raw 10x load) regression holds.")
