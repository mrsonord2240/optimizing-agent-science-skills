"""Phase-2 Input 3 fixture: fresh rich AnnData built from real PBMC data."""
import scanpy as sc
import h5py
src = "F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/public-data/pbmc_1k_v3_filtered_feature_bc_matrix.h5"
out = "F:/OpenScience/audits/bio-single-cell-data-io/data/fp2_rich.h5ad"
adata = sc.read_10x_h5(src)
adata.var_names_make_unique()
adata.layers["counts"] = adata.X.copy()
sc.pp.normalize_total(adata, target_sum=10000)
sc.pp.log1p(adata)
adata.obs["batch"] = "phase2"
adata.obs["batch"] = adata.obs["batch"].astype("category")
adata.raw = adata
sc.pp.highly_variable_genes(adata, n_top_genes=700)
adata = adata[:, adata.var["highly_variable"]].copy()
sc.pp.pca(adata, n_comps=12, random_state=23)
adata.write_h5ad(out, compression="gzip")
with h5py.File(out, "r") as f:
    raw_shape = tuple(f["raw/X"].attrs["shape"])
print("hvg_shape", adata.shape, "raw_shape", raw_shape, "obsm", list(adata.obsm.keys()))
assert adata.shape == (1222, 700)
assert raw_shape == (1222, 33538)
print("PASS input3_fixture")
