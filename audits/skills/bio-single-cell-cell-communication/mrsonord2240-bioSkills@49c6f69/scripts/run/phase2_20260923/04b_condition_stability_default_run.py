"""Phase 2 deep check: invoke the current stability script at its documented default n-null=10."""
from pathlib import Path
import subprocess
import sys

AUDIT = Path(r"F:\OpenScience\audits\bio-single-cell-cell-communication")
OUT = AUDIT / "run" / "phase2_20260923"
SCRIPT = Path(r"F:\OpenScience\wt\single-cell-cell-communication\single-cell\cell-communication\scripts\condition_stability.py")
command = [sys.executable, str(SCRIPT), str(OUT / "known_null_conditions.h5ad"),
           "--cond-a", "control", "--cond-b", "stimulated", "--groupby", "cell_type", "--condition", "condition",
           "--out", str(OUT / "condition_stability_default.tsv")]
completed = subprocess.run(command, check=True, text=True, capture_output=True)
(OUT / "04b_condition_stability_default.stdout.txt").write_text(completed.stdout, encoding="utf-8")
(OUT / "04b_condition_stability_default.stderr.txt").write_text(completed.stderr, encoding="utf-8")
print(completed.stdout, end="")
