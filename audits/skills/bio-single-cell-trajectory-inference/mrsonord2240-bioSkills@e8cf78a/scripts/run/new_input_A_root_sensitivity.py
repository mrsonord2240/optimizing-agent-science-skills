"""
Re-auditor NEW input A (not in the original 7, not verified by the fixer): empirically
test the Governing Principle's rule 3 claim -- "Root-cell choice flips every gene
trend... the sign of every trend and which cells are 'early' invert with the root" --
on real Paul15 data, by running DPT from the correct MEP-anchored root vs. a
deliberately wrong root (a mature/terminal Neu cell), and checking whether the
resulting pseudotime orderings are (near-)reversed, as the Skill claims.
"""
import numpy as np
import scanpy as sc

sc.settings.verbosity = 0

adata = sc.read_h5ad("data/paul15_raw.h5ad")
adata.X = adata.X.astype("float64")
sc.pp.recipe_zheng17(adata)
sc.tl.pca(adata, svd_solver="arpack")
sc.pp.neighbors(adata, n_neighbors=15, use_rep="X_pca")
sc.tl.diffmap(adata, n_comps=15)

mep_idx = int(np.flatnonzero(adata.obs["paul15_clusters"] == "7MEP")[0])
neu_candidates = np.flatnonzero(adata.obs["paul15_clusters"] == "16Neu")
neu_idx = int(neu_candidates[0])

# Root 1: correct, MEP-anchored (progenitor)
adata.uns["iroot"] = mep_idx
sc.tl.dpt(adata, n_dcs=10, n_branchings=0)
pt_correct = adata.obs["dpt_pseudotime"].copy()

# Root 2: deliberately wrong, a mature terminal neutrophil cell
adata.uns["iroot"] = neu_idx
sc.tl.dpt(adata, n_dcs=10, n_branchings=0)
pt_wrong = adata.obs["dpt_pseudotime"].copy()

corr = np.corrcoef(pt_correct.values, pt_wrong.values)[0, 1]
print(f"Correlation between MEP-rooted and Neu-rooted pseudotime: {corr:.4f}")
print("ASSERTION root_choice_materially_changes_ordering (|corr| < 0.9):", abs(corr) < 0.9)

means_correct = adata.obs.assign(pt=pt_correct).groupby("paul15_clusters", observed=True)["pt"].mean()
means_wrong = adata.obs.assign(pt=pt_wrong).groupby("paul15_clusters", observed=True)["pt"].mean()
print("\nMEP-rooted: MEP mean pt =", means_correct.get("7MEP"), " Neu mean pt =", means_correct.get("16Neu"))
print("Neu-rooted: MEP mean pt =", means_wrong.get("7MEP"), " Neu mean pt =", means_wrong.get("16Neu"))
flips = (means_correct.get("7MEP") < means_correct.get("16Neu")) and (means_wrong.get("7MEP") > means_wrong.get("16Neu"))
print("ASSERTION early_vs_late_label_inverts_with_root:", bool(flips))
print("DONE")
