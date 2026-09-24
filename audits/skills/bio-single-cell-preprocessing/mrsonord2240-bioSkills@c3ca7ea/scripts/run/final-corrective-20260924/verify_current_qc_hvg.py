"""Execute the corrected QC guard and per-batch HVG helper on audit fixtures."""

import warnings

import numpy as np
import scanpy as sc
from scipy.stats import median_abs_deviation


DATA = "F:/OpenScience/audits/bio-single-cell-preprocessing/data"


def is_outlier(adata, metric, nmads):
    values = adata.obs[metric]
    mad = median_abs_deviation(values)
    print(f"{metric}: median={np.median(values):.3f}, MAD={mad:.3f}")
    if mad == 0:
        raise ValueError(
            f"MAD collapsed for {metric}; use documented fixed cutoffs instead of MAD filtering"
        )
    return (values < np.median(values) - nmads * mad) | (
        np.median(values) + nmads * mad < values
    )


def filter_genes_per_batch(adata, batch_key, min_cells=3):
    keep_by_batch = []
    for _, positions in adata.obs.groupby(batch_key, observed=True).indices.items():
        detected = np.asarray((adata.X[positions] > 0).sum(axis=0)).ravel()
        keep_by_batch.append(detected >= min_cells)
    keep = np.logical_and.reduce(keep_by_batch)
    if not keep.any():
        raise ValueError(
            "No genes meet the per-batch min_cells requirement; "
            "lower min_cells or inspect the shallow batch"
        )
    return adata[:, keep].copy()


nuclei = sc.read_h5ad(DATA + "/tiny_nuclei.h5ad")
nuclei.var["mt"] = nuclei.var_names.str.startswith("MT-")
sc.pp.calculate_qc_metrics(
    nuclei, qc_vars=["mt"], percent_top=[20], log1p=True, inplace=True
)
try:
    is_outlier(nuclei, "log1p_total_counts", 5)
except ValueError as exc:
    print("PASS: nuclei MAD guard stopped:", exc)
else:
    raise AssertionError("zero-MAD nuclei fixture did not stop")

mito_hard_caps = {
    "nuclei": None,
    "pbmc": 8,
    "cardiac": 30,
    "hepatic": 30,
    "skeletal_muscle": 40,
    "unknown": None,
}
assert mito_hard_caps["nuclei"] is None and mito_hard_caps["unknown"] is None
print("PASS: nuclei and unknown tissues use MAD-only mitochondrial filtering")

adata = sc.read_h5ad(DATA + "/depth_imbalanced.h5ad")
adata.layers["counts"] = adata.X.copy()
filtered = filter_genes_per_batch(adata, batch_key="sample", min_cells=3)
print(f"per-batch filter retained {filtered.n_vars}/{adata.n_vars} genes")
with warnings.catch_warnings(record=True) as caught:
    warnings.simplefilter("always")
    sc.pp.highly_variable_genes(
        filtered,
        n_top_genes=2000,
        flavor="seurat_v3",
        layer="counts",
        batch_key="sample",
    )
assert int(filtered.var["highly_variable"].sum()) == 2000
assert not any("reciprocal condition number" in str(w.message) for w in caught)
print("PASS: per-batch seurat_v3 HVG completed with 2000 genes")
