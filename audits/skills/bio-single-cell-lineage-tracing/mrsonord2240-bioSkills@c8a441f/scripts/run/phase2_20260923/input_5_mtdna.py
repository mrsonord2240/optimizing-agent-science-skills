"""Phase 2 Input 5: execute the current mtDNA grouping pattern on fresh synthetic data."""
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist
from sklearn.metrics import silhouette_score, adjusted_rand_score

rng = np.random.default_rng(20260923)
truth = np.repeat(np.arange(4), 10)
profiles = np.zeros((40, 9), dtype=float)
for clone in range(4):
    profiles[truth == clone, clone * 2 : clone * 2 + 2] = 0.9
profiles += rng.normal(0, 0.025, profiles.shape)
profiles = np.clip(profiles, 0, 1)
profiles[:, 8] = 0.95  # recurrent hotspot
het = pd.DataFrame(profiles, index=[f"mt_{i:02d}" for i in range(40)], columns=[f"var_{i}" for i in range(8)] + ["chrM_hotspot"])
het.to_csv("../data/phase2_mtdna_heteroplasmy.csv")

# Literal current SKILL.md logic.
prevalence = (het > 0.1).mean(axis=0)
het_f = het.loc[:, prevalence <= 0.8]
dist = pdist(het_f.values, metric="correlation")
Z = linkage(dist, method="average")
best_k, best_score, best_labels = None, -1, None
for k in range(2, 8):
    labels = fcluster(Z, t=k, criterion="maxclust")
    if len(set(labels)) < 2:
        continue
    score = silhouette_score(het_f.values, labels, metric="correlation")
    if score > best_score:
        best_k, best_score, best_labels = k, score, labels
clones = pd.Series(best_labels, index=het.index, name="mtdna_clone")
ari = adjusted_rand_score(truth, clones)
assert "chrM_hotspot" not in het_f.columns and best_k == 4 and ari == 1.0
print(f"input5 PASS hotspot_dropped=True k={best_k} ARI={ari:.3f}")
