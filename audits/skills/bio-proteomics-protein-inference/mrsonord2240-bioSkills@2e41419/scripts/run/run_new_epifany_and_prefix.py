"""Two fresh Phase-2 cases: EPIFANY output contract and a wrong-prefix negative test."""
from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
OUT = RUN / "outputs"
DATA = RUN.parent / "data"
PY = Path(r"F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/Scripts/python.exe")
SCRIPTS = RUN / "skill_scripts"


def call(*args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run([str(PY), *args], text=True, capture_output=True, check=False)
    print("$", " ".join(args))
    print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")
    assert result.returncode == expected, (result.returncode, expected)
    return result


# Fresh Input 8: Bayesian route, then its group-level FDR companion.
epifany = OUT / "new8_epifany.tsv"
call(str(SCRIPTS / "epifany_inference.py"), str(DATA / "peptides_1pct_fdr_std.idXML"), "--out", str(epifany))
with epifany.open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle, delimiter="\t"))
assert len(rows) == 749 and all(0.0 <= float(r["probability"]) <= 1.0 for r in rows)
picked = OUT / "new8_epifany_picked.tsv"
call(str(SCRIPTS / "picked_group_fdr.py"), str(epifany), "--decoy-prefix", "DECOY_", "--out", str(picked))
with picked.open(encoding="utf-8", newline="") as handle:
    passing = list(csv.DictReader(handle, delimiter="\t"))
assert len(passing) == 586
print("new8 ASSERT: EPIFANY=749 bounded posteriors; picked-group output=586 targets")

# Fresh Input 9: same data, deliberately incompatible MaxQuant prefix.  The documented guard
# must fail before it could produce a target-looking result.
wrong = call(str(SCRIPTS / "picked_group_fdr.py"), str(epifany), "--decoy-prefix", "REV__", expected=1)
assert "no decoy groups with prefix" in wrong.stderr
print("new9 ASSERT: incompatible REV__ prefix is rejected explicitly")
