"""
Re-auditor regression pass, inputs 1-3 (own fresh script, real Paul15 + PBMC data,
mirroring but not copying the original auditor's scripts). Runs the FIXED worktree
SKILL.md's PAGA/DPT/Palantir blocks against real data as regression checks.
"""
import numpy as np
import scanpy as sc

sc.settings.verbosity = 1

print("=" * 70)
print("REGRESSION INPUT 1: PAGA continuum + DPT rooted on MEP marker (Paul15)")
print("=" * 70)
adata = sc.read_h5ad("data/paul15_raw.h5ad")
adata.X = adata.X.astype("float64")
sc.pp.recipe_zheng17(adata)
sc.tl.pca(adata, svd_solver="arpack")

sc.pp.neighbors(adata, n_neighbors=15, use_rep="X_pca")
sc.tl.leiden(adata, resolution=1.0, flavor="igraph", n_iterations=2, directed=False)
sc.tl.paga(adata, groups="leiden")
sc.pl.paga(adata, threshold=0.03, show=False)
sc.tl.umap(adata, init_pos="paga")

sc.tl.diffmap(adata, n_comps=15)
root_candidates = np.flatnonzero(adata.obs["paul15_clusters"] == "7MEP")
adata.uns["iroot"] = int(root_candidates[0])
sc.tl.dpt(adata, n_dcs=10, n_branchings=0)

df = adata.obs[["paul15_clusters", "dpt_pseudotime"]].copy()
means = df.groupby("paul15_clusters", observed=True)["dpt_pseudotime"].mean()
ery_order = ["1Ery", "2Ery", "3Ery", "4Ery", "5Ery", "6Ery"]
ery_vals = [means[c] for c in ery_order if c in means.index]
print("Ery series mean pseudotime:", dict(zip(ery_order, ery_vals)))
mep_mean = means.get("7MEP", np.nan)
mature_mean = means[means.index.isin(["1Ery", "16Neu", "15Mo"])].mean()
print(f"MEP mean pseudotime: {mep_mean:.4f}, mature mean: {mature_mean:.4f}")
print("ASSERTION mep_lower_than_mature:", mep_mean < mature_mean)
adata.write("out_input1_paga_dpt.h5ad")

print()
print("=" * 70)
print("REGRESSION INPUT 2: Palantir fate probabilities + entropy (Paul15)")
print("=" * 70)
import palantir

dm_res = palantir.utils.run_diffusion_maps(adata, n_components=5)
ms_data = palantir.utils.determine_multiscale_space(dm_res)
early_cell = adata.obs_names[int(root_candidates[0])]
pr_res = palantir.core.run_palantir(ms_data, early_cell=early_cell, terminal_states=None, num_waypoints=500)
ent = pr_res.entropy
mep_ent = ent[adata.obs["paul15_clusters"] == "7MEP"].mean()
mature_mask = adata.obs["paul15_clusters"].isin(["1Ery", "16Neu", "15Mo"])
mature_ent = ent[mature_mask.values].mean()
print(f"Palantir entropy MEP: {mep_ent:.4f}, mature: {mature_ent:.4f}")
print("ASSERTION entropy_falls_with_commitment:", mep_ent > mature_ent)
print("Terminal states auto-detected:", len(pr_res.branch_probs.columns) if hasattr(pr_res, "branch_probs") else "n/a")

print()
print("=" * 70)
print("REGRESSION INPUT 3: PAGA continuum-vs-discrete on real PBMC 1k (mature types)")
print("=" * 70)
pbmc = sc.read_h5ad(r"F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\public-data\pbmc_1k_v3_filtered.h5ad")
pbmc.var_names_make_unique()
sc.pp.filter_cells(pbmc, min_genes=200)
sc.pp.filter_genes(pbmc, min_cells=3)
sc.pp.normalize_total(pbmc, target_sum=1e4)
sc.pp.log1p(pbmc)
sc.pp.highly_variable_genes(pbmc, n_top_genes=2000)
pbmc = pbmc[:, pbmc.var.highly_variable].copy()
sc.pp.scale(pbmc, max_value=10)
sc.tl.pca(pbmc, svd_solver="arpack")
sc.pp.neighbors(pbmc, n_neighbors=15, use_rep="X_pca")
sc.tl.leiden(pbmc, resolution=1.0, flavor="igraph", n_iterations=2, directed=False)
sc.tl.paga(pbmc, groups="leiden")
conn = pbmc.uns["paga"]["connectivities"].toarray()
n_clusters = conn.shape[0]
isolated_003 = [i for i in range(n_clusters) if (conn[i] > 0.03).sum() == 0]
isolated_05 = [i for i in range(n_clusters) if (conn[i] > 0.5).sum() == 0]
print(f"{n_clusters} leiden clusters on real discrete PBMC data")
print("Isolated at threshold=0.03:", len(isolated_003), "/", n_clusters)
print("Isolated at threshold=0.5:", len(isolated_05), "/", n_clusters)
nz = conn[conn > 0]
print("Median nonzero connectivity:", np.median(nz))
print("DONE")
