"""Fresh Input 7: reject a protein-looking table with no MaxQuant bookkeeping columns."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


path = Path(__file__).resolve().parents[1] / "data" / "wrong_table_no_bookkeeping.tsv"
pg = pd.read_csv(path, sep="\t", low_memory=False)
flag_cols = ("Reverse", "Potential contaminant", "Only identified by site")
try:
    if "Protein IDs" not in pg:
        raise ValueError("Expected MaxQuant proteinGroups.txt with a 'Protein IDs' column; this is not that table")
    if not any(c in pg for c in flag_cols):
        raise ValueError("Expected MaxQuant proteinGroups.txt bookkeeping columns; received none of Reverse, Potential contaminant, Only identified by site")
except ValueError as exc:
    result = {"rejected": True, "exception": type(exc).__name__, "message": str(exc), "input_rows_unchanged": len(pg)}
else:
    raise AssertionError("Unsupported table was accepted")

assert result["input_rows_unchanged"] == 2, result
assert "received none" in result["message"], result
print(json.dumps(result, indent=2))
