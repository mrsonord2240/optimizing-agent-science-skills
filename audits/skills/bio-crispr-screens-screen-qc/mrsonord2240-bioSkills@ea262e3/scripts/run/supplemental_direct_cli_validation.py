"""Demonstrate whether the advertised direct representation CLI enforces SKILL.md validation."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
AUDIT = ROOT.parent
PY = Path(r"F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts\python.exe")
CLI = ROOT / "source_copy" / "scripts" / "library_representation.py"

# The table has the documented Gene column and numeric samples but deliberately loses sgRNA IDs:
# its first column is the bare integer range that SKILL.md says must be rejected.
bad = pd.DataFrame({"sgRNA": range(6), "Gene": ["G1"] * 6, "S1": [10, 11, 12, 13, 14, 15]})
path = AUDIT / "data" / "supplemental_default_index.count.txt"
bad.to_csv(path, sep="\t", index=False)
proc = subprocess.run([str(PY), str(CLI), str(path)], text=True, capture_output=True, check=False)
result = (f"$ {PY} {CLI} {path}\n\n[exit] {proc.returncode}\n[stdout]\n{proc.stdout}\n[stderr]\n{proc.stderr}\n")
(ROOT / "supplemental_direct_cli_validation.log").write_text(result, encoding="utf-8")
print(result)
if proc.returncode != 0:
    raise SystemExit("The direct CLI correctly rejected the missing sgRNA IDs.")
print("FINDING: direct CLI accepted a default integer sgRNA index and produced metrics, contrary to SKILL.md Input Validation.")
