"""Execute the repaired Step 6b MAGeCK MLE command on archived real HAP1 data.

Inputs: mle_subsample.count.txt and mle_design.txt created for the archived Input 6.
Usage: python final_pass_mle.py
Writes: finalpass_mle_round10.* and final_pass_mle.json in this directory.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pandas as pd


RUN = Path(__file__).parent
ROOT = Path(r"F:\OpenScience")
PYTHON = ROOT / "audit-envs" / "crispr-screen-analyst" / "Scripts" / "python.exe"
MAGECK = ROOT / "audit-envs" / "crispr-screen-analyst" / "Scripts" / "mageck"
PREFIX = RUN / "finalpass_mle_round10"


def main() -> None:
    command = [
        str(PYTHON), str(MAGECK), "mle",
        "--count-table", str(RUN / "mle_subsample.count.txt"),
        "--design-matrix", str(RUN / "mle_design.txt"),
        "--output-prefix", str(PREFIX),
        "--norm-method", "median",
        "--permutation-round", "10",
    ]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    gene_summary = Path(f"{PREFIX}.gene_summary.txt")
    assert gene_summary.is_file() and gene_summary.stat().st_size > 100, gene_summary
    result = pd.read_csv(gene_summary, sep="\t")
    assert len(result) >= 1000, len(result)
    assert any(column.endswith("|fdr") for column in result.columns), list(result.columns)
    payload = {
        "command": command,
        "gene_summary": str(gene_summary),
        "n_genes": len(result),
        "fdr_columns": [column for column in result.columns if column.endswith("|fdr")],
        "stdout_tail": completed.stdout[-1000:],
        "stderr_tail": completed.stderr[-1000:],
    }
    (RUN / "final_pass_mle.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
