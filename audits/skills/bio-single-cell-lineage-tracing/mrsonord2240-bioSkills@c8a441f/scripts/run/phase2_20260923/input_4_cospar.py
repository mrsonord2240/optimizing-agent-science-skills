"""Phase 2 Input 4: execute the current CoSpar SKILL.md block on regression data."""
import cospar as cs
import scanpy as sc

# Source-faithful block; the audit supplies the h5ad path and a unique cache key.
adata = cs.hf.read("../data/phase2_lineage_traced.h5ad")
emb = adata.copy()
sc.pp.normalize_total(emb); sc.pp.log1p(emb); sc.pp.pca(emb); sc.pp.neighbors(emb); sc.tl.umap(emb)
adata = cs.pp.initialize_adata_object(
    adata, X_clone=adata.obsm["X_clone"], time_info=adata.obs["time_info"],
    X_pca=emb.obsm["X_pca"], X_emb=emb.obsm["X_umap"], data_des="phase2_20260923",
)
adata = cs.tmap.infer_Tmap_from_multitime_clones(adata, smooth_array=[15, 10, 5], sparsity_threshold=0.1)
cs.tl.fate_bias(adata, selected_fates=["Monocyte", "Neutrophil"])
fate_cols = [c for c in adata.obs.columns if "fate_bias" in c or "fate_map" in c]
assert fate_cols and any(adata.obs[c].notna().any() for c in fate_cols)
print("input4 PASS", "fate_columns", len(fate_cols), "cells", adata.n_obs)
