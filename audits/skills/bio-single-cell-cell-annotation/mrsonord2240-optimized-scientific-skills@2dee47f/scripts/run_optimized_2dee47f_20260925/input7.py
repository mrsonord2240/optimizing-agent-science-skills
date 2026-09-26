"""New use case: compare two plausible CellTypist immune references and flag disagreements."""
from pathlib import Path

import celltypist
import numpy as np
import pandas as pd
import scanpy as sc

ROOT = Path(r"F:\OpenScience\audits\bio-single-cell-cell-annotation\reaudit-optimized-scientific-skills@2dee47f-20260925")
PUBLIC = Path(r"F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\public-data\pbmc_1k_v3_filtered.h5ad")
MODELS = Path(r"F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\cache\celltypist\data\models")
a = sc.read_h5ad(PUBLIC)
rng = np.random.default_rng(41)
take = np.sort(rng.choice(a.n_obs, size=min(800, a.n_obs), replace=False))
a = a[take].copy()
a.layers["counts"] = a.X.copy()
sc.pp.normalize_total(a, target_sum=1e4); sc.pp.log1p(a)
sc.pp.highly_variable_genes(a, n_top_genes=2000, flavor="seurat_v3", layer="counts")
sc.tl.pca(a, n_comps=40, mask_var="highly_variable", random_state=41)
sc.pp.neighbors(a, random_state=41)
sc.tl.leiden(a, resolution=1.2, flavor="igraph", n_iterations=2, directed=False, random_state=41)

labels = {}
confidence = {}
for model_name in ("Immune_All_Low.pkl", "Immune_All_High.pkl"):
    model = celltypist.models.Model.load(model=(MODELS / model_name).resolve().as_posix())
    pred = celltypist.annotate(a, model=model, majority_voting=True, over_clustering="leiden")
    annotated = pred.to_adata()
    labels[model_name] = annotated.obs["majority_voting"].astype(str).values
    confidence[model_name] = annotated.obs["conf_score"].astype(float).values
    assert len(labels[model_name]) == a.n_obs
    assert np.isfinite(confidence[model_name]).all()

comparison = pd.DataFrame(labels, index=a.obs_names)
comparison["low_conf"] = confidence["Immune_All_Low.pkl"]
comparison["high_conf"] = confidence["Immune_All_High.pkl"]
comparison["exact_agreement"] = comparison["Immune_All_Low.pkl"] == comparison["Immune_All_High.pkl"]


def lineage(value: object) -> str:
    text = str(value).lower()
    if "megakaryo" in text or "platelet" in text:
        return "Mk"
    if "dendritic" in text or text.startswith("dc") or "pdc" in text:
        return "DC"
    if "monocyt" in text or "macrophage" in text:
        return "Mono"
    if "natural killer" in text or "nk cell" in text or "ilc" in text:
        return "NK"
    if "b cell" in text or "plasma" in text or "germinal" in text or text.startswith(("naive b", "memory b")):
        return "B"
    if any(token in text for token in ("t cell", "tcm", "tem", "treg", "mait", "helper", "cytotoxic")):
        return "T"
    return "Other"


comparison["low_lineage"] = comparison["Immune_All_Low.pkl"].map(lineage)
comparison["high_lineage"] = comparison["Immune_All_High.pkl"].map(lineage)
comparison["coarse_agreement"] = comparison["low_lineage"] == comparison["high_lineage"]
comparison["needs_review"] = (~comparison["coarse_agreement"]) | (comparison[["low_conf", "high_conf"]].min(axis=1) < 0.5)
comparison.to_csv(ROOT / "data" / "input7_model_comparison.csv")
assert comparison["needs_review"].any()
print(f"real_pbmc_cells={a.n_obs} seeded_clusters={a.obs['leiden'].nunique()}")
print(f"exact_label_agreement={comparison['exact_agreement'].mean():.3f}")
print(f"coarse_lineage_agreement={comparison['coarse_agreement'].mean():.3f}")
print(f"cells_flagged_for_review={comparison['needs_review'].sum()}")
print(f"low_model_mean_conf={comparison['low_conf'].mean():.3f}")
print(f"high_model_mean_conf={comparison['high_conf'].mean():.3f}")
print("disagreements_flagged_for_manual_review=True")
print("either_model_treated_as_ground_truth=False")
