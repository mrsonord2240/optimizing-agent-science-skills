import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import logomaker

out = os.path.dirname(os.path.abspath(__file__))
counts = pd.DataFrame({"A": [10, 0, 5, 8], "C": [0, 8, 5, 1],
                       "G": [0, 2, 0, 0], "T": [0, 0, 0, 1]})
background = np.array([0.29, 0.21, 0.21, 0.29])
ic = logomaker.transform_matrix(counts, from_type="counts", to_type="information",
                                background=background, pseudocount=0)
p = counts.to_numpy(float) / counts.to_numpy(float).sum(axis=1, keepdims=True)
with np.errstate(divide="ignore", invalid="ignore"):
    expected = np.where(p > 0, p * np.sum(np.where(p > 0, p * np.log2(p / background), 0), axis=1, keepdims=True), 0)
assert np.allclose(ic.to_numpy(), expected)
fig, ax = plt.subplots(figsize=(6, 2))
logo = logomaker.Logo(ic, ax=ax, color_scheme="classic", shade_below=0.5, fade_below=0.5)
assert logo.fig is fig
logo.style_xticks(rotation=0)
logo.ax.set_ylabel("Bits")
fig.savefig(os.path.join(out, "logomaker_information.png"), dpi=120, bbox_inches="tight")
plt.close(fig)

weight = logomaker.transform_matrix(counts, from_type="counts", to_type="weight",
                                    background=background, pseudocount=0)
assert np.isfinite(weight.to_numpy()).all() is False or (weight.to_numpy() < 0).any()
fig, ax = plt.subplots(figsize=(6, 2))
logo = logomaker.Logo(weight, ax=ax, color_scheme="classic", flip_below=True)
assert logo.fig is fig
fig.savefig(os.path.join(out, "logomaker_weight.png"), dpi=120, bbox_inches="tight")
plt.close(fig)
for name in ("logomaker_information.png", "logomaker_weight.png"):
    assert os.path.getsize(os.path.join(out, name)) > 1000

small_counts = pd.DataFrame({"A": [5], "C": [0], "G": [0], "T": [0]})
small_default = logomaker.transform_matrix(
    small_counts, from_type="counts", to_type="information",
    background=[0.25] * 4,
).to_numpy().sum()
small_zero = logomaker.transform_matrix(
    small_counts, from_type="counts", to_type="information",
    background=[0.25] * 4, pseudocount=0,
).to_numpy().sum()
posterior = np.array([6, 1, 1, 1], dtype=float) / 9
expected_default = 2 + np.sum(posterior * np.log2(posterior))
assert np.isclose(small_default, expected_default)
assert np.isclose(small_zero, 2.0)
assert not np.isclose(small_default, small_zero)
print("logomaker_version=" + logomaker.__version__)
print(f"small_n_default={small_default:.9f} small_n_zero={small_zero:.9f}")
print("assertions=information_relative_entropy,pseudocount_zero,ax_binding,signed_weight,rendered_pngs,small_n_default")
