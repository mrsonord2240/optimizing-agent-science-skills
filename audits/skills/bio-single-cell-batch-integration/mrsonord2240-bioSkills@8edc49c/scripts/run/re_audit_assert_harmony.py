"""Assert the exact shipped Harmony script created required representations."""
import scanpy as sc

adata = sc.read_h5ad(r"F:/OpenScience/audits/bio-single-cell-batch-integration/run/re_audit_harmony.h5ad")
assert {"X_pca", "X_pca_harmony"} <= set(adata.obsm)
assert adata.obs["leiden"].nunique() > 1
print(f"PASS harmony: {adata.n_obs} cells, {adata.obs['leiden'].nunique()} clusters, {sorted(adata.obsm)}")
