"""Regression input 1: fixed PCA recipe on archived synthetic bulk counts."""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

AUDIT = Path(r"F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots")
counts = pd.read_csv(AUDIT / "data" / "bulk_counts.csv", index_col=0)
meta = pd.read_csv(AUDIT / "data" / "bulk_meta.csv", index_col=0)

# Fixed recipe: library-size normalization, log transform, scale, deterministic full SVD.
cpm = counts.to_numpy() / counts.sum(axis=1).to_numpy()[:, None] * 1e6
logged = np.log2(cpm + 1)
scale = logged.std(axis=0)
scale[scale == 0] = 1
X = (logged - logged.mean(axis=0)) / scale
pca = PCA(n_components=10, svd_solver="full")
scores = pca.fit_transform(X)
repeat = PCA(n_components=10, svd_solver="full").fit_transform(X)
variance = pca.explained_variance_ratio_
loadings = pca.components_.T

_, singular, _ = np.linalg.svd(X - X.mean(axis=0), full_matrices=False)
truth = singular**2 / np.sum(singular**2)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), constrained_layout=True)
conditions = meta["condition"].astype("category")
colors = plt.colormaps["tab10"](np.arange(len(conditions.cat.categories)))
for index, condition in enumerate(conditions.cat.categories):
    selected = np.asarray(conditions == condition)
    axes[0].scatter(scores[selected, 0], scores[selected, 1], color=colors[index], label=condition, s=24)
strongest = np.argsort(np.linalg.norm(loadings[:, :2], axis=1))[-5:]
arrow_scale = 0.12 * min(np.ptp(scores[:, 0]), np.ptp(scores[:, 1]))
loading_scale = arrow_scale / np.linalg.norm(loadings[strongest, :2], axis=1).max()
for gene_index in strongest:
    dx, dy = loadings[gene_index, :2] * loading_scale
    axes[0].arrow(0, 0, dx, dy, color="black", width=0.02)
    axes[0].annotate(counts.columns[gene_index], (dx, dy), fontsize=6)
axes[0].set_xlabel(f"PC1 ({variance[0] * 100:.1f}%)")
axes[0].set_ylabel(f"PC2 ({variance[1] * 100:.1f}%)")
axes[0].legend(title="condition")
legend_labels = [text.get_text() for text in axes[0].get_legend().get_texts()]
axes[1].plot(np.arange(1, 11), variance, "o-")
axes[1].set(xlabel="Principal component", ylabel="Variance explained")
out = AUDIT / "figs" / "input1_bulk_pca.png"
fig.savefig(out, dpi=200)
plt.close(fig)

raw_scores = PCA(n_components=3, svd_solver="full").fit_transform(counts)
raw_lib_corr = np.corrcoef(raw_scores[:, 0], meta["libfactor"])[0, 1]
norm_lib_corr = np.corrcoef(scores[:, 0], meta["libfactor"])[0, 1]
print(f"full solver: {pca._fit_svd_solver}")
print(f"repeat bit-identical: {np.array_equal(scores, repeat)}")
print(f"max variance-ratio difference vs independent SVD: {np.max(np.abs(variance - truth[:10])):.3g}")
print(f"PC1 percent: {variance[0] * 100:.1f}; independent: {truth[0] * 100:.1f}")
print(f"PC1 correlation with planted library factor: raw={raw_lib_corr:+.3f}, normalized={norm_lib_corr:+.3f}")
print(f"legend labels: {legend_labels}")
print(f"loading arrows: {len(strongest)}; figure bytes: {out.stat().st_size}")
assert np.array_equal(scores, repeat)
assert np.allclose(variance, truth[:10], atol=1e-12)
assert abs(norm_lib_corr) < 0.3
assert legend_labels == ["ctrl", "trtA", "trtB"]
assert out.stat().st_size > 10_000
