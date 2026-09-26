"""Regression Input 2: execute the bundled DIA-NN loader and check its FDR/zero contract."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd


root = Path(__file__).resolve().parents[1]
module_path = root / "run" / "source_examples" / "load_diann.py"
spec = importlib.util.spec_from_file_location("audited_load_diann", module_path)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)

path = root / "data" / "report.parquet"
raw = pd.read_parquet(path)
matrix = module.load_diann(path)
lowconf = set(raw.loc[raw["Global.PG.Q.Value"] > 0.01, "Protein.Group"])
result = {
    "raw_rows": len(raw),
    "protein_groups": matrix.shape[0],
    "runs": matrix.shape[1],
    "lowconf_groups_in_matrix": len(lowconf.intersection(matrix.index)),
    "infinite_values": int(np.isinf(matrix.to_numpy()).sum()),
}
assert result["protein_groups"] == 887, result
assert result["runs"] == 8, result
assert result["lowconf_groups_in_matrix"] == 0, result
assert result["infinite_values"] == 0, result
print(json.dumps(result, indent=2))
