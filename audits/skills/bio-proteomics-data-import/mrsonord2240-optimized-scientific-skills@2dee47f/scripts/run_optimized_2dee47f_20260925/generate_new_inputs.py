"""Generate two deterministic synthetic fixtures unique to the independent re-audit."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


AUDIT_ROOT = Path(__file__).resolve().parents[1]
DATA = AUDIT_ROOT / "data"
RNG = np.random.default_rng(20260925)


def make_tmt() -> dict:
    n_rows = 400
    channels = [f"Reporter intensity corrected {126 + i}" for i in range(10)]
    values = RNG.lognormal(mean=16.0, sigma=0.55, size=(n_rows, len(channels)))
    values[20, 3] = 0.0
    values[21, :] = 0.0
    frame = pd.DataFrame(values, columns=channels)
    frame.insert(0, "Only identified by site", "")
    frame.insert(0, "Potential contaminant", "")
    frame.insert(0, "Reverse", "")
    frame.insert(0, "Gene names", [f"GENE{i};ALT{i}" if i % 37 == 0 else f"GENE{i}" for i in range(n_rows)])
    frame.insert(0, "Protein IDs", [f"P{i:05d};Q{i:05d}" if i % 41 == 0 else f"P{i:05d}" for i in range(n_rows)])
    frame.loc[0:4, "Reverse"] = "+"
    frame.loc[5:7, "Potential contaminant"] = "+"
    frame.loc[8:9, "Only identified by site"] = "+"
    path = DATA / "tmt_proteinGroups.txt"
    frame.to_csv(path, sep="\t", index=False)
    return {
        "file": path.name,
        "rows": n_rows,
        "bookkeeping_rows": 10,
        "target_rows": 390,
        "channels": channels,
        "all_zero_target_rows": 1,
    }


def make_wrong_table() -> dict:
    frame = pd.DataFrame(
        {
            "Protein IDs": ["P00001", "P00002"],
            "Gene names": ["A", "B"],
            "LFQ intensity S1": [1000.0, 2000.0],
            "LFQ intensity S2": [1100.0, 1900.0],
        }
    )
    path = DATA / "wrong_table_no_bookkeeping.tsv"
    frame.to_csv(path, sep="\t", index=False)
    return {"file": path.name, "rows": len(frame), "bookkeeping_columns": 0}


truth = {"seed": 20260925, "tmt": make_tmt(), "wrong_table": make_wrong_table()}
(DATA / "new_input_truth.json").write_text(json.dumps(truth, indent=2) + "\n", encoding="utf-8")
print(json.dumps(truth, indent=2))
