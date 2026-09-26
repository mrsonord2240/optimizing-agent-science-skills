"""Prior Stress regression: QC-first all-cluster triage before novelty claims."""
from pathlib import Path

import celltypist
import pandas as pd
import scanpy as sc

DATA = Path(r"F:\OpenScience\audits\_partial-20260911\bio-workflows-scrnaseq-pipeline\data\synthetic_pbmc_8samples")
OUT = Path(r"F:\OpenScience\audits\bio-single-cell-cell-annotation\reaudit-optimized-scientific-skills@2dee47f-20260925\data")
MODEL = Path(r"F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\cache\celltypist\data\models\Immune_All_Low.pkl")
a = sc.read_h5ad(DATA / "all_samples_filtered.h5ad")
truth = pd.read_csv(DATA / "truth_cells.csv").set_index("cell_id").loc[a.obs_names]
a.obs["true_doublet"] = truth["true_doublet"].astype(bool).values
a.obs["true_low_quality"] = truth["true_low_quality"].astype(bool).values
a.layers["counts"] = a.X.copy()
a.var["mt"] = a.var_names.str.startswith("MT-")
sc.pp.calculate_qc_metrics(a, qc_vars=["mt"], percent_top=[20], log1p=True, inplace=True)
sc.pp.normalize_total(a, target_sum=1e4); sc.pp.log1p(a)
sc.pp.highly_variable_genes(a, n_top_genes=2000, flavor="seurat_v3", layer="counts")
sc.tl.pca(a, n_comps=50, mask_var="highly_variable", random_state=29)
sc.pp.neighbors(a, random_state=29)
sc.tl.leiden(a, resolution=1.5, flavor="igraph", n_iterations=2, directed=False, random_state=29)
sc.pp.scrublet(a, batch_key="sample", expected_doublet_rate=0.03, random_state=29)
b = a.copy(); b.X = b.layers["counts"].copy(); sc.pp.normalize_total(b, target_sum=1e4); sc.pp.log1p(b)
pred = celltypist.annotate(
    b,
    model=celltypist.models.Model.load(model=MODEL.resolve().as_posix()),
    majority_voting=True,
    over_clustering="leiden",
)
b = pred.to_adata()
for col in ("leiden", "pct_counts_mt", "n_genes_by_counts", "predicted_doublet", "sample", "true_doublet", "true_low_quality"):
    b.obs[col] = a.obs[col].values

# Current Skill path: every cluster enters QC; confidence is secondary.
qc = b.obs.groupby("leiden", observed=True).agg(
    pct_counts_mt=("pct_counts_mt", "median"),
    n_genes_by_counts=("n_genes_by_counts", "median"),
    doublet_rate=("predicted_doublet", "mean"),
)
qc["batch_purity"] = b.obs.groupby("leiden", observed=True)["sample"].agg(lambda s: s.value_counts(normalize=True).max())
qc["median_conf_score"] = b.obs.groupby("leiden", observed=True)["conf_score"].median()
qc["true_doublet_frac"] = b.obs.groupby("leiden", observed=True)["true_doublet"].mean()
qc["true_lowq_frac"] = b.obs.groupby("leiden", observed=True)["true_low_quality"].mean()
qc["qc_flag"] = (
    (qc["pct_counts_mt"] > 2 * qc["pct_counts_mt"].median())
    | (qc["n_genes_by_counts"] < 0.5 * qc["n_genes_by_counts"].median())
    | (qc["doublet_rate"] > 2 * qc["doublet_rate"].median())
    | (qc["batch_purity"] > 0.9)
)
artifact = (qc["true_doublet_frac"] >= 0.25) | (qc["true_lowq_frac"] >= 0.5)
assert len(qc) == b.obs["leiden"].nunique()
assert int(artifact.sum()) > 0
assert bool(qc.loc[artifact, "qc_flag"].all())
qc.to_csv(OUT / "input5_cluster_qc.csv")
print(qc.round(3).sort_values(["true_doublet_frac", "true_lowq_frac"], ascending=False).to_string())
print(f"all_clusters_screened={len(qc)} artifact_clusters={int(artifact.sum())} artifact_qc_recall=1.000")
print("novel_label_claimed=False")
