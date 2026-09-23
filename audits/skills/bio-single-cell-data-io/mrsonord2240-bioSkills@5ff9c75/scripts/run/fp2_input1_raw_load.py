"""Phase-2 Input 1: real raw 10x PBMC H5 load with Scanpy."""
import scanpy as sc
import scipy.sparse as sp
path = "F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/public-data/pbmc_1k_v3_raw_feature_bc_matrix.h5"
adata = sc.read_10x_h5(path, gex_only=False)
adata.var_names_make_unique()
print("shape", adata.shape)
print("sparse", sp.issparse(adata.X))
print("gene_ids", "gene_ids" in adata.var.columns)
print("feature_types", sorted(adata.var["feature_types"].astype(str).unique().tolist()))
assert adata.shape == (6794880, 33538)
assert sp.issparse(adata.X)
assert "gene_ids" in adata.var.columns
print("PASS input1")
