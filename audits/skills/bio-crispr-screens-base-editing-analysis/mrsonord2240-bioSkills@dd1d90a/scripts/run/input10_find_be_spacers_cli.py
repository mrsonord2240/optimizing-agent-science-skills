"""New Phase 2 input: exercise the committed library-design CLI end to end.

It writes an engineered FASTA, invokes the byte-matched subject CLI, parses the
TSV, and asserts the reverse-strand target call survives CLI serialization.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pandas as pd

RUN = Path(__file__).resolve().parent
SUBJECT = RUN / "subject_scripts" / "find_be_spacers.py"
work = RUN / "input10_cli_data"
work.mkdir(exist_ok=True)
cds = list("A" * 100)
cds[88] = "G"; cds[71] = "C"; cds[70] = "C"; cds[72] = "A"
for idx in (89, 87, 86, 85): cds[idx] = "A"
fasta = work / "engineered.fa"
out = work / "spacers.tsv"
fasta.write_text(">engineered_reverse_target\n" + "".join(cds) + "\n", encoding="utf-8")
run = subprocess.run([sys.executable, str(SUBJECT), "--cds", str(fasta), "--target-aa", "30", "--target-base", "C", "--editor", "BE4max", "--out", str(out)], text=True, capture_output=True, check=True)
df = pd.read_csv(out, sep="\t")
row = df[(df.strand == "-") & (df.spacer_start == 7)]
assert len(row) == 1 and row.iloc[0].target_positions == "[5]" and row.iloc[0].bystander_positions == "[]"
assert "candidate spacers" in run.stderr
print("INPUT10_CLI_PASS", row.iloc[0].to_dict())
