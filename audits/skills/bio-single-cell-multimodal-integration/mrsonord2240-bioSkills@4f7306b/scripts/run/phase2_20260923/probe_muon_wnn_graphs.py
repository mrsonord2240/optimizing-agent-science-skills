"""Audit-only probe: execute the corrected source through Muon WNN, then inspect graph artifacts."""
import muon as mu
import scanpy as sc

mdata = mu.read_10x_h5("input7_python_wnn/filtered_feature_bc_matrix.h5")
rna = mdata.mod["rna"]
adt = mdata.mod["prot"]
rna.var["mt"] = rna.var_names.str.startswith("MT-")
sc.pp.calculate_qc_metrics(rna, qc_vars=["mt"], percent_top=None, inplace=True)
mu.pp.intersect_obs(mdata)
mask = (rna.obs["n_genes_by_counts"] > 200) & (rna.obs["n_genes_by_counts"] < 5000) & (rna.obs["pct_counts_mt"] < 20)
mdata = mdata[mask].copy()
rna, adt = mdata.mod["rna"], mdata.mod["prot"]
sc.pp.normalize_total(rna, target_sum=1e4)
sc.pp.log1p(rna)
sc.pp.highly_variable_genes(rna, n_top_genes=2000)
sc.pp.scale(rna, max_value=10)
sc.tl.pca(rna, n_comps=30)
sc.pp.neighbors(rna, n_neighbors=15, n_pcs=min(30, rna.obsm["X_pca"].shape[1]))
mu.prot.pp.clr(adt, axis=0)
sc.pp.scale(adt, max_value=10)
sc.tl.pca(adt, n_comps=min(18, adt.n_vars - 1))
sc.pp.neighbors(adt, n_neighbors=15, n_pcs=min(18, adt.obsm["X_pca"].shape[1]))
joint_candidates = min(200, mdata.n_obs - 1)
mu.pp.neighbors(mdata, n_neighbors=min(15, joint_candidates), n_bandwidth_neighbors=min(20, joint_candidates), n_multineighbors=joint_candidates, key_added="wnn")
print("MODALITY_NEIGHBORS", {key: list(mdata.mod[key].uns["neighbors"].keys()) for key in ("rna", "prot")})
print("WNN_CONNECTIVITY", mdata.obsp["wnn_connectivities"].shape, mdata.obsp["wnn_connectivities"].nnz)
print("WNN_UNS", mdata.uns["wnn"])
