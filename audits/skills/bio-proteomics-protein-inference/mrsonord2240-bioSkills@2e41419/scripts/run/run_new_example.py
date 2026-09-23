"""Fresh Phase-2 case: execute the standalone parsimony/picked-FDR example copy."""
from __future__ import annotations
import subprocess
from pathlib import Path

RUN = Path(__file__).resolve().parent
PY = Path(r"F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/Scripts/python.exe")
example = RUN / "skill_scripts" / "protein_groups.py"
result = subprocess.run([str(PY), str(example)], text=True, capture_output=True, check=False)
print(result.stdout, end="")
if result.stderr:
    print(result.stderr, end="")
assert result.returncode == 0
assert "Parsimony kept 7 groups out of 8 candidate groups" in result.stdout
assert "Protein groups passing 1% picked-group FDR: 2" in result.stdout
assert "P_E-2" in result.stdout and "P_E" in result.stdout
print("new9-example ASSERT: deterministic isoform grouping and picked-FDR demo output are present")
