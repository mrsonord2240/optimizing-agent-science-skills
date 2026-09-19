"""Input 4 continued: read the h5ad produced from the Seurat object back in Python
and check what survived vs. what the user asked to verify ('no layers were dropped')."""
import scanpy as sc

p = r"F:\OpenScience\audits\bio-single-cell-data-io\data\input4_from_seurat.h5ad"
adata = sc.read_h5ad(p)
print(f"Loaded: {adata.n_obs} cells x {adata.n_vars} genes")
print("layers:", list(adata.layers.keys()))
print("obsm:", list(adata.obsm.keys()))
print("X corresponds to (per R log): counts assay")
print("Seurat RNA assay had 3 layers (counts, data, scale.data); scale.data is ABSENT here -> silently dropped by as.SingleCellExperiment()")
