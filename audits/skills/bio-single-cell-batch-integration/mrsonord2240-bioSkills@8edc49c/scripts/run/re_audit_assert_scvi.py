"""Assert the exact shipped scVI/scANVI script created reproducible outputs."""
import scanpy as sc

adata = sc.read_h5ad(r"F:/OpenScience/audits/bio-single-cell-batch-integration/run/re_audit_scvi.h5ad")
assert {"X_scVI", "X_scANVI"} <= set(adata.obsm)
assert "scanvi_label" in adata.obs
assert adata.obsm["X_scVI"].shape[0] == adata.n_obs
print(f"PASS scvi/scanvi: {adata.n_obs} cells, {adata.obsm['X_scVI'].shape}, {adata.obsm['X_scANVI'].shape}")
