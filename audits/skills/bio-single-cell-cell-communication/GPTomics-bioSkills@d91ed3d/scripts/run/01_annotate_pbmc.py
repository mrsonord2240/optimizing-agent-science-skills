\
# Prepares an annotated PBMC 1k v3 AnnData for the cell-communication audit.
# Real 10x data (not synthetic): F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\public-data\
# QC -> normalize -> cluster (Leiden) -> CellTypist Immune_All_Low annotation.
import scanpy as sc
import celltypist
import numpy as np

sc.settings.verbosity = 1

adata = sc.read_10x_h5(
    r"F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\public-data\pbmc_1k_v3_filtered_feature_bc_matrix.h5"
)
adata.var_names_make_unique()
print("Loaded:", adata.shape)

adata.var["mt"] = adata.var_names.str.startswith("MT-")
sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], inplace=True, percent_top=None)
adata = adata[(adata.obs["n_genes_by_counts"] >= 200) & (adata.obs["pct_counts_mt"] < 20)].copy()
sc.pp.filter_genes(adata, min_cells=3)
print("After QC:", adata.shape)

adata.layers["counts"] = adata.X.copy()
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
adata.raw = adata

sc.pp.highly_variable_genes(adata, n_top_genes=2000)
adata_hvg = adata[:, adata.var.highly_variable].copy()
sc.pp.scale(adata_hvg, max_value=10)
sc.tl.pca(adata_hvg, n_comps=30)
sc.pp.neighbors(adata_hvg, n_neighbors=15)
sc.tl.leiden(adata_hvg, resolution=1.0)
adata.obs["leiden"] = adata_hvg.obs["leiden"]
adata.obsm["X_pca"] = adata_hvg.obsm["X_pca"]
adata.obsp = adata_hvg.obsp
adata.uns["neighbors"] = adata_hvg.uns["neighbors"]

print("Leiden clusters:", adata.obs["leiden"].value_counts().to_dict())

model = celltypist.models.Model.load(
    model=r"F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\cache\celltypist\data\models\Immune_All_Low.pkl"
)
pred = celltypist.annotate(adata, model=model, majority_voting=True)
adata = pred.to_adata()
print("CellTypist majority_voting counts:")
print(adata.obs["majority_voting"].value_counts())

adata.obs["cell_type"] = adata.obs["majority_voting"].astype(str)
# Collapse to coarse labels used downstream for CCC groupby
coarse_map = {}
for ct in adata.obs["cell_type"].unique():
    c = ct
    if "T cell" in ct or "T cells" in ct:
        c = "T_cell"
    elif "B cell" in ct or "B cells" in ct or "Plasma" in ct:
        c = "B_cell"
    elif "Monocyte" in ct or "Macrophage" in ct or "DC" in ct or "Dendritic" in ct:
        c = "Myeloid"
    elif "NK" in ct:
        c = "NK_cell"
    coarse_map[ct] = c
adata.obs["cell_type_coarse"] = adata.obs["cell_type"].map(coarse_map)
print("Coarse cell types:")
print(adata.obs["cell_type_coarse"].value_counts())

adata.write(r"F:\OpenScience\audits\bio-single-cell-cell-communication\data\adata_annotated.h5ad")
print("Saved adata_annotated.h5ad, shape:", adata.shape)
