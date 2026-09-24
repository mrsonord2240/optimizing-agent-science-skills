import sys
import muon as mu

mdata = mu.read_h5mu(sys.argv[1])
assert mdata.n_obs == 90
assert "wnn" in mdata.uns
assert "wnn_clusters" in mdata.obs
assert mdata.obsm["X_umap"].shape == (90, 2)
assert mdata.obsp["wnn_connectivities"].nnz == 1738
assert mdata.obs["wnn_clusters"].nunique() == 3
print("python_wnn_clean_exit cells=90 graph_nonzeros=1738 umap=(90,2) clusters=3")
