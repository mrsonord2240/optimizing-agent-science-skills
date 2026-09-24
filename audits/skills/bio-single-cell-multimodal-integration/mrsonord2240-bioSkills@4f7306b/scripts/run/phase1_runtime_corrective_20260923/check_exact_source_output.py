import sys

import muon as mu

mdata = mu.read_h5mu(sys.argv[1])
assert mdata.n_obs == 90
assert "wnn" in mdata.uns
assert "wnn_clusters" in mdata.obs
assert "X_umap" in mdata.obsm and mdata.obsm["X_umap"].shape == (90, 2)
assert mdata.obsp["wnn_connectivities"].nnz > 0
print(
    "exact_source_output_clean_exit "
    f"cells={mdata.n_obs} wnn_nonzero={mdata.obsp['wnn_connectivities'].nnz} "
    f"umap_shape={mdata.obsm['X_umap'].shape} clusters={mdata.obs['wnn_clusters'].nunique()}"
)
