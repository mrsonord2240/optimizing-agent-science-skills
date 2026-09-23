"""Phase 2 Input 4: create a known-null split then invoke the current stability script."""
from pathlib import Path
import subprocess
import sys

import numpy as np
import pandas as pd
import scanpy as sc

AUDIT = Path(r"F:\OpenScience\audits\bio-single-cell-cell-communication")
OUT = AUDIT / "run" / "phase2_20260923"
SCRIPT = Path(r"F:\OpenScience\wt\single-cell-cell-communication\single-cell\cell-communication\scripts\condition_stability.py")
adata = sc.read_h5ad(AUDIT / "data" / "adata_annotated.h5ad")
rng = np.random.default_rng(20260923)
assignment = pd.Series(index=adata.obs_names, dtype=object)
for _, barcode_index in adata.obs.groupby("cell_type", observed=True).groups.items():
    barcodes = np.asarray(list(barcode_index), dtype=object)
    rng.shuffle(barcodes)
    assignment.loc[barcodes[:len(barcodes) // 2]] = "control"
    assignment.loc[barcodes[len(barcodes) // 2:]] = "stimulated"
adata.obs["condition"] = assignment
assert adata.obs["condition"].notna().all()
prepared = OUT / "known_null_conditions.h5ad"
adata.write(prepared)

command = [sys.executable, str(SCRIPT), str(prepared), "--cond-a", "control", "--cond-b", "stimulated",
           "--groupby", "cell_type", "--condition", "condition", "--n-null", "2", "--n-perms", "1000",
           "--seed", "1337", "--out", str(OUT / "condition_stability.tsv")]
completed = subprocess.run(command, check=True, text=True, capture_output=True)
(OUT / "condition_stability.stdout.txt").write_text(completed.stdout, encoding="utf-8")
(OUT / "condition_stability.stderr.txt").write_text(completed.stderr, encoding="utf-8")
out = pd.read_csv(OUT / "condition_stability.tsv", sep="\t")
assert {"direction", "null_freq", "noise_prone"}.issubset(out.columns)
assert len(out) > 0
print(completed.stdout, end="")
print("STABILITY_ROWS", len(out))
print("NOISE_PRONE_ROWS", int(out["noise_prone"].astype(str).str.lower().eq("true").sum()))
