"""Run every shipped Python example from the fresh dispatched Skill copy."""
from __future__ import annotations

import os
import py_compile
import subprocess
import sys
from pathlib import Path

RUN = Path(__file__).resolve().parent
EX = RUN / "skill" / "examples"
WORK = RUN / "example_noargs_work"
WORK.mkdir(exist_ok=True)
examples = sorted(EX.glob("*.py"))
expect = {
    "a2m_a3m_io.py": "match columns per row",
    "analyze_alignment.py": "Alignment: 6 sequences, 20 columns",
    "clean_alignment.py": "Saved to cleaned_alignment.fasta",
    "consensus_sequence.py": "Consensus (100% threshold)",
    "find_conserved.py": "Fully conserved positions",
    "gap_analysis.py": "Gaps per sequence",
    "henikoff_weights.py": "Kish effective sample size",
    "mi_apc.py": "exceed the null",
    "neff.py": "Neff (62% threshold",
}
for path in examples:
    py_compile.compile(str(path), doraise=True)
    if path.name in expect:
        result = subprocess.run([sys.executable, str(path)], cwd=WORK, text=True, capture_output=True,
                                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        assert result.returncode == 0 and expect[path.name] in result.stdout, (path.name, result.stderr, result.stdout)
        print(f"PASS {path.name}: {expect[path.name]}")

usage = subprocess.run([sys.executable, str(EX / "muscle5_column_confidence.py")], cwd=WORK,
                       text=True, capture_output=True)
assert usage.returncode != 0 and "usage:" in (usage.stdout + usage.stderr)
print("PASS muscle5_column_confidence.py: clear usage exit without arguments")
print(f"ALL {len(examples)} EXAMPLES PY_COMPILE; 10 EXECUTABLE ENTRYPOINT CHECKS PASS")
