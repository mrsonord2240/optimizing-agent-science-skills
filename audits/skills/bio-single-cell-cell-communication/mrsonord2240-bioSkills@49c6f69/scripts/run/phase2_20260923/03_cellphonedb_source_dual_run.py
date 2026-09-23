"""Phase 2 Input 2: invoke the current shipped CellPhoneDB script twice, unchanged."""
from pathlib import Path
import subprocess
import sys

import numpy as np
import pandas as pd

AUDIT = Path(r"F:\OpenScience\audits\bio-single-cell-cell-communication")
OUT = AUDIT / "run" / "phase2_20260923"
SCRIPT = Path(r"F:\OpenScience\wt\single-cell-cell-communication\single-cell\cell-communication\scripts\cellphonedb_statistical.py")
ZIP = AUDIT / "run" / "cpdb_db" / "cellphonedb.zip"
META = AUDIT / "run" / "meta.tsv"
COUNTS = AUDIT / "run" / "counts_normalized.h5ad"

for run_name in ("cpdb_run1", "cpdb_run2"):
    destination = OUT / run_name
    command = [sys.executable, str(SCRIPT), str(ZIP), str(META), str(COUNTS),
               "--out-dir", str(destination), "--iterations", "1000", "--threads", "1", "--seed", "1337"]
    completed = subprocess.run(command, check=True, text=True, capture_output=True)
    (OUT / f"{run_name}.stdout.txt").write_text(completed.stdout, encoding="utf-8")
    (OUT / f"{run_name}.stderr.txt").write_text(completed.stderr, encoding="utf-8")
    print(run_name, "EXIT", completed.returncode)

def latest_table(folder: Path, needle: str) -> Path:
    paths = sorted(folder.glob(f"*{needle}*.txt"))
    if not paths:
        raise AssertionError(f"No {needle} table in {folder}")
    return paths[-1]

p1 = pd.read_csv(latest_table(OUT / "cpdb_run1", "pvalues"), sep="\t")
p2 = pd.read_csv(latest_table(OUT / "cpdb_run2", "pvalues"), sep="\t")
assert p1.shape == p2.shape and p1.shape[0] > 100 and p1.shape[1] > 10
meta = {"id_cp_interaction", "interacting_pair", "partner_a", "partner_b", "gene_a", "gene_b", "secreted",
        "receptor_a", "receptor_b", "annotation_strategy", "is_integrin", "directionality", "classification"}
numeric = [column for column in p1.columns if column not in meta]
a1, a2 = p1[numeric].to_numpy(float), p2[numeric].to_numpy(float)
identical = np.array_equal(a1, a2)
flips = int(((a1 < 0.05) != (a2 < 0.05)).sum())
print("PVALUES_SHAPE", p1.shape)
print("BIT_IDENTICAL_THREADS1", identical)
print("SIGNIFICANCE_FLAG_FLIPS", flips)
assert identical and flips == 0
