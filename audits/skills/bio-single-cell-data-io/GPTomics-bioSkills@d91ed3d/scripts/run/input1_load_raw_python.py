"""
Input 1 (Canonical) - "Load the raw 10X PBMC h5 matrix and report cells x genes,
keeping the antibody/CRISPR features if present."

Follows SKILL.md 'Loading 10X Cell Ranger Output' pattern:
  adata = sc.read_10x_mtx('raw_feature_bc_matrix/', var_names='gene_ids', gex_only=False)
adapted to the h5 file we actually have (sc.read_10x_h5, gex_only=False), since SKILL.md
explicitly documents the h5 variant too ('Load this Cell Ranger h5 and report cells x genes').
"""
import scanpy as sc
import anndata as ad

RAW_H5 = r"F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\public-data\pbmc_1k_v3_raw_feature_bc_matrix.h5"

adata = sc.read_10x_h5(RAW_H5, gex_only=False)
adata.var_names_make_unique()

print("anndata version:", ad.__version__)
print("scanpy version:", sc.__version__)
print(f"Loaded RAW matrix: {adata.n_obs} cells x {adata.n_vars} genes")
print("var columns:", list(adata.var.columns))
if "feature_types" in adata.var.columns:
    print("feature_types counts:\n", adata.var["feature_types"].value_counts())
print("X dtype/sparse:", type(adata.X), "issparse:", __import__("scipy.sparse", fromlist=["issparse"]).issparse(adata.X))
print("gene_ids present:", "gene_ids" in adata.var.columns)
