"""Validate CP10K/log1p restoration, majority labels, confidence, and configured outputs."""
from pathlib import Path

import numpy as np
import pandas as pd
import scanpy as sc

ROOT = Path(r"F:\OpenScience\audits\bio-single-cell-cell-annotation\reaudit-optimized-scientific-skills@2dee47f-20260925")
inp = sc.read_h5ad(ROOT / "data" / "input1_clustered.h5ad")
out = sc.read_h5ad(ROOT / "data" / "input1_annotated.h5ad")

assert out.obs_names.equals(inp.obs_names)
assert out.obs["leiden"].astype(str).equals(inp.obs["leiden"].astype(str))
assert {"cell_type", "annotation_confidence", "high_confidence"}.issubset(out.obs.columns)
assert (ROOT / "data" / "input1_annotation.png").stat().st_size > 1000
assert (ROOT / "data" / "input1_counts.csv").stat().st_size > 20
linear = np.expm1(out.X.toarray() if hasattr(out.X, "toarray") else out.X)
totals = linear.sum(axis=1)
assert np.allclose(totals, 1e4, rtol=2e-4, atol=2.0)


def lineage(value: object) -> str:
    text = str(value).lower()
    if "megakaryo" in text or "platelet" in text:
        return "Mk"
    if "ilc" in text or ("nk" in text and "cell" in text):
        return "NK"
    if "dendritic" in text or text.startswith("dc") or "pdc" in text:
        return "DC"
    if "monocyt" in text or "macrophage" in text:
        return "Mono"
    if "b cell" in text or "plasma" in text or "germinal" in text:
        return "B"
    if any(token in text for token in ("t cell", "tcm", "tem", "treg", "mait", "helper", "cytotoxic")):
        return "T"
    return "other"


truth_map = {
    "CD4 T cells": "T", "CD8 T cells": "T", "NK cells": "NK", "B cells": "B",
    "CD14+ Monocytes": "Mono", "FCGR3A+ Monocytes": "Mono", "Dendritic cells": "DC",
    "Megakaryocytes": "Mk",
}
truth = out.obs["true_cell_type"].map(truth_map)
per_cell = out.obs["predicted_labels"].map(lineage)
majority = out.obs["majority_voting"].map(lineage)
per_acc = float((truth == per_cell).mean())
majority_acc = float((truth == majority).mean())
counts = pd.read_csv(ROOT / "data" / "input1_counts.csv")
assert int(counts.iloc[:, 1].sum()) == out.n_obs
print(f"cp10k_min={totals.min():.2f} cp10k_max={totals.max():.2f}")
print(f"seeded_clusters_preserved={out.obs['leiden'].nunique()}")
print(f"per_cell_lineage_accuracy={per_acc:.3f}")
print(f"majority_lineage_accuracy={majority_acc:.3f}")
print(f"low_confidence={(~out.obs['high_confidence'].astype(bool)).sum()}/{out.n_obs}")
print("configured_outputs=PASS")
