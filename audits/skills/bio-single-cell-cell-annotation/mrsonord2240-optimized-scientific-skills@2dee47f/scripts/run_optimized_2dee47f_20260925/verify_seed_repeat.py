"""Confirm identical majority-voted labels across repeated use of the same seeded clusters."""
from pathlib import Path

import celltypist
import numpy as np
import scanpy as sc

ROOT = Path(r"F:\OpenScience\audits\bio-single-cell-cell-annotation\reaudit-optimized-scientific-skills@2dee47f-20260925")
MODEL = Path(r"F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\cache\celltypist\data\models\Immune_All_Low.pkl")
a = sc.read_h5ad(ROOT / "data" / "input1_clustered.h5ad")[:1000].copy()
model = celltypist.models.Model.load(model=MODEL.resolve().as_posix())
runs = []
for _ in range(2):
    q = a.copy(); q.X = q.layers["counts"].copy(); sc.pp.normalize_total(q, target_sum=1e4); sc.pp.log1p(q)
    runs.append(celltypist.annotate(q, model=model, majority_voting=True, over_clustering="leiden").to_adata())
labels_equal = runs[0].obs["majority_voting"].astype(str).equals(runs[1].obs["majority_voting"].astype(str))
confidence_equal = np.allclose(runs[0].obs["conf_score"], runs[1].obs["conf_score"], rtol=0, atol=0)
assert labels_equal and confidence_equal
print(f"cells={a.n_obs} seeded_clusters={a.obs['leiden'].nunique()}")
print(f"majority_labels_identical={labels_equal}")
print(f"confidence_identical={confidence_equal}")
