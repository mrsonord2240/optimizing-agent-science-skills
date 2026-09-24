"""Run the documented drugZ branch on the archived synthetic drug screen.

Usage: python final_pass_drugz.py
Writes: finalpass_drugz_output.txt and final_pass_drugz.json.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pandas as pd


ROOT = Path(r"F:\OpenScience")
RUN = Path(__file__).parent
PYTHON = ROOT / "audit-envs" / "crispr-screen-analyst" / "Scripts" / "python.exe"
DRUGZ = ROOT / "audit-envs" / "crispr-screen-analyst" / "tools" / "dl" / "drugz" / "drugz.py"
OUTPUT = RUN / "finalpass_drugz_output.txt"


def main() -> None:
    command = [
        str(PYTHON), str(DRUGZ),
        "-i", str(RUN / "synth_drug_screen.count.txt"),
        "-o", str(OUTPUT),
        "-c", "Veh", "-x", "Drug", "-p", "5",
    ]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    assert OUTPUT.is_file() and OUTPUT.stat().st_size > 100
    result = pd.read_csv(OUTPUT, sep="\t")
    assert len(result) == 200 and "fdr_synth" in result.columns
    payload = {
        "command": command,
        "n_genes": len(result),
        "minimum_fdr_synth": float(result["fdr_synth"].min()),
        "stdout_tail": completed.stdout[-1000:],
        "stderr_tail": completed.stderr[-1000:],
    }
    (RUN / "final_pass_drugz.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
