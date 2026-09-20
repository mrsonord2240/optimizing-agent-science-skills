"""
Re-auditor's independent determinism check for the P2 fix: random_state=0 added
to all perturbation_signature() call sites (SKILL.md x2, examples/run_pertpy.py).

Independent of the fixer's fixture: different seed, different cell/gene count
(1,500 cells x 250 genes vs. the fixer's 2,000 x unspecified), and run as two
genuinely separate OS processes (not two calls in the same Python session) so
there is no chance of shared global RNG state carrying over between runs.
"""
import subprocess
import sys
import numpy as np
import pandas as pd
import anndata as ad

SCRIPT = r"""
import numpy as np, pandas as pd, anndata as ad, pertpy as pt

rng = np.random.default_rng(90210)  # fixed data-generation seed so both runs see identical input
n_cells = 1500
n_genes = 250
group = np.array((["PERT"] * (n_cells // 2)) + (["NT"] * (n_cells - n_cells // 2)))
rng.shuffle(group)
baseline = rng.uniform(5, 200, size=n_genes)
X = np.zeros((n_cells, n_genes))
for i in range(n_cells):
    mult = np.where(group[i] == "PERT", 1.8, 1.0)
    X[i, :] = rng.poisson(baseline * mult)

adata = ad.AnnData(X=X, obs=pd.DataFrame({"gene_target": group}, index=[f"c{i}" for i in range(n_cells)]),
                    var=pd.DataFrame(index=[f"g{i}" for i in range(n_genes)]))
adata.layers["counts"] = X.copy()

import scanpy as sc
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=100)

ms = pt.tl.Mixscape()
ms.perturbation_signature(adata=adata, pert_key="gene_target", control="NT", n_neighbors=20, random_state=0)

np.save(r"__OUTFILE__", adata.layers["X_pert"])
print("wrote", r"__OUTFILE__", adata.layers["X_pert"].shape)
"""

out1 = "test4_run1_Xpert.npy"
out2 = "test4_run2_Xpert.npy"

for out in (out1, out2):
    script = SCRIPT.replace("__OUTFILE__", out)
    with open(f"_tmp_seed_{out}.py", "w") as f:
        f.write(script)

python_exe = sys.executable
print(f"Using interpreter: {python_exe}")

for out in (out1, out2):
    r = subprocess.run([python_exe, f"_tmp_seed_{out}.py"], capture_output=True, text=True)
    print(r.stdout)
    if r.returncode != 0:
        print(r.stderr)
    assert r.returncode == 0, f"subprocess for {out} failed"

a = np.load(out1)
b = np.load(out2)
print(f"\nrun1 shape: {a.shape}, run2 shape: {b.shape}")
n_diff = np.sum(np.any(np.abs(a - b) > 0, axis=1)) if a.ndim > 1 else np.sum(a != b)
max_abs_diff = np.max(np.abs(a - b))
print(f"Cells differing between two independent-process runs: {n_diff} / {a.shape[0]}")
print(f"Max abs diff: {max_abs_diff}")
byte_identical = np.array_equal(a, b)
print(f"Byte-identical (np.array_equal): {byte_identical}")
assert byte_identical, "Expected byte-identical X_pert across two independent seeded runs"
print("\nPASS: random_state=0 produces byte-identical perturbation_signature() output "
      "across two independent OS processes on an independently-generated synthetic dataset.")
