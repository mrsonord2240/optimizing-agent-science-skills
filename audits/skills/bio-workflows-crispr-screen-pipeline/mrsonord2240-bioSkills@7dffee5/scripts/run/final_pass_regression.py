"""Final-pass regression checks for bio-workflows-crispr-screen-pipeline.

Inputs: final-pass worktree and the archived real HAP1 count matrix.
Usage: python final_pass_regression.py
Writes: final_pass_regression.json beside this script.
"""
from __future__ import annotations

import json
import re
import subprocess
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(r"F:\OpenScience")
SKILL = ROOT / "worktrees" / "bio-workflows-crispr-screen-pipeline-finalpass" / "workflows" / "crispr-screen-pipeline" / "SKILL.md"
EXAMPLE = SKILL.parent / "examples" / "crispr_pipeline.sh"
COUNT_TABLE = ROOT / "audits" / "bio-workflows-crispr-screen-pipeline" / "data" / "experiment.count.txt"
MAGECK = ROOT / "audit-envs" / "crispr-screen-analyst" / "Scripts" / "mageck"
PYTHON = ROOT / "audit-envs" / "crispr-screen-analyst" / "Scripts" / "python.exe"
OUT = Path(__file__).with_name("final_pass_regression.json")


def condition(sample_name: str) -> str:
    return re.sub(r"_(?:[Rr]ep|[Rr])?\d+$|_[A-Z]$", "", sample_name)


def main() -> None:
    text = SKILL.read_text(encoding="utf-8")
    required = {
        "MLE command uses 10 rounds": "--output-prefix timecourse_mle --norm-method median --permutation-round 10",
        "MLE caveat is present": "default-round boundary call as stable",
        "Pearson floor is consistent": "Replicate Pearson on log-counts >=0.8 (MAGeCK-VISPR floor); >0.85 acceptable",
        "bundled example is discoverable": "examples/crispr_pipeline.sh",
        "ambiguous input preflight remains present": "Step 0: Confirm Made-Once Commitments",
    }
    for label, expected in required.items():
        assert expected in text, f"{label}: expected {expected!r}"
    assert EXAMPLE.is_file(), "referenced example is missing"

    count = pd.read_csv(COUNT_TABLE, sep="\t")
    sample_cols = list(count.columns[2:])
    log_counts = np.log10(count[sample_cols] + 1)
    pearson = log_counts.corr()
    groups: dict[str, list[str]] = {}
    for column in sample_cols:
        groups.setdefault(condition(column), []).append(column)
    pairs = [pearson.loc[a, b] for cols in groups.values() for a, b in combinations(cols, 2)]
    assert pairs, "real count matrix had no within-condition replicate pairs"
    real_within_condition = float(np.mean(pairs))
    assert 0.75 < real_within_condition < 1.0, real_within_condition

    # Fresh input: a different supported label convention must preserve condition grouping.
    fresh_labels = ["Day0", "Vehicle_rep1", "Vehicle_rep2", "Drug_r1", "Drug_r2", "Drug_r3"]
    fresh_groups: dict[str, list[str]] = {}
    for label in fresh_labels:
        fresh_groups.setdefault(condition(label), []).append(label)
    assert fresh_groups == {
        "Day0": ["Day0"],
        "Vehicle": ["Vehicle_rep1", "Vehicle_rep2"],
        "Drug": ["Drug_r1", "Drug_r2", "Drug_r3"],
    }, fresh_groups

    help_text = subprocess.run(
        [str(PYTHON), str(MAGECK), "mle", "--help"], check=True, capture_output=True, text=True
    ).stdout
    assert "Suggested value: 10" in help_text and "Default 2" in help_text
    result = {
        "source_commit": "7dffee58a50f7b4ef25d5922a1b95960f886a3f2",
        "real_hap1_within_condition_pearson": real_within_condition,
        "real_sample_groups": groups,
        "fresh_label_groups": fresh_groups,
        "mageck_help_confirms": "--permutation-round suggested value 10; default 2",
        "checks": len(required) + 5,
    }
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
