"""
Re-auditor regression, input 4 (RNA velocity), fresh script transcribed verbatim from
the FIXED worktree SKILL.md's "RNA Velocity" deterministic-mode code block, run
end-to-end against real scv.datasets.pancreas()-equivalent cached data
(pancreas_raw.h5ad, already the real dataset used by the original audit).
"""
import scanpy as sc
import scvelo as scv
import numpy as np

scv.settings.verbosity = 3

adata = sc.read_h5ad("data/pancreas_raw.h5ad")

# --- verbatim from fixed SKILL.md RNA Velocity code block ---
scv.pp.filter_and_normalize(adata, min_shared_counts=20)
adata.layers['normalized_X'] = adata.X.copy()
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)
adata = adata[:, adata.var['highly_variable']].copy()
adata.X = adata.layers.pop('normalized_X')
scv.pp.moments(adata, n_pcs=30, n_neighbors=30)
scv.tl.velocity(adata, mode='deterministic')
scv.tl.velocity_graph(adata, n_jobs=1, show_progress_bar=False)
scv.tl.velocity_confidence(adata)
scv.tl.velocity_pseudotime(adata)
# --- end verbatim block ---

print("EXIT OK, adata shape:", adata.shape)
print("mean velocity_confidence:", float(adata.obs["velocity_confidence"].mean()))

if "clusters" in adata.obs.columns:
    means = adata.obs.groupby("clusters", observed=True)["velocity_pseudotime"].mean().sort_values()
    print("\nMean velocity_pseudotime per cluster (should be low in Ductal progenitor, high in terminal fates):")
    print(means)
    ductal = means.get("Ductal", np.nan)
    print("ASSERTION ductal_is_low:", bool(ductal == means.min()) if not np.isnan(ductal) else "no Ductal label")
else:
    print("No 'clusters' column found; columns are:", list(adata.obs.columns))

print("DONE")
