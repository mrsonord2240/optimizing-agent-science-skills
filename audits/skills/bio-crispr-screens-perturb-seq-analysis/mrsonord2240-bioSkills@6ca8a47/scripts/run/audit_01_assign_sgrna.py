"""Fresh dense/CSR regression for the shipped sgRNA assignment script."""
from pathlib import Path
import importlib.util
import numpy as np
import anndata as ad
from scipy import sparse

AUDIT = Path(r"F:\OpenScience\audits\bio-crispr-screens-perturb-seq-analysis")
SKILL = AUDIT / "run" / "shipped_assign_sgrna.py"
spec = importlib.util.spec_from_file_location("assign_sgrna", SKILL)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

rng = np.random.default_rng(20260923)
n_cells, n_guides = 240, 6
counts = rng.poisson(1, size=(n_cells, n_guides)).astype(np.int64)
truth = np.full(n_cells, "none", dtype=object)
for i in range(0, 150):
    j = i % n_guides
    counts[i, j] = 20
    truth[i] = f"sg_{j}"
for i in range(150, 180):
    counts[i, i % n_guides] = 20
    counts[i, (i + 1) % n_guides] = 17
    truth[i] = "multiplet"
var = {"feature_type": ["sgRNA"] * n_guides}
names = [f"sg_{i}" for i in range(n_guides)]
dense = ad.AnnData(X=np.zeros((n_cells, n_guides)), var=var)
dense.layers["sgrna_counts"] = counts
dense.var_names = names
sparse_a = dense.copy()
sparse_a.layers["sgrna_counts"] = sparse.csr_matrix(counts)
out_d = mod.assign_sgrna(dense, threshold=10).obs["sgrna_assignment"].to_numpy()
out_s = mod.assign_sgrna(sparse_a, threshold=10).obs["sgrna_assignment"].to_numpy()
np.testing.assert_array_equal(out_d, truth)
np.testing.assert_array_equal(out_s, truth)
np.testing.assert_array_equal(out_d, out_s)
dense.write_h5ad(AUDIT / "data" / "assign_fixture_dense.h5ad")
sparse_a.write_h5ad(AUDIT / "data" / "assign_fixture_csr.h5ad")
print(f"dense_correct={(out_d == truth).sum()}/{n_cells}")
print(f"csr_correct={(out_s == truth).sum()}/{n_cells}")
print(f"dense_csr_mismatches={(out_d != out_s).sum()}")
print("class_counts=" + repr(dict(zip(*np.unique(out_d, return_counts=True)))))
