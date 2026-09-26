"""Regression Input 1: canonical MaxQuant LFQ cleaning on the prior synthetic fixture."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


path = Path(__file__).resolve().parents[1] / "data" / "proteinGroups.txt"
pg = pd.read_csv(path, sep="\t", low_memory=False)
if "Protein IDs" not in pg:
    raise ValueError("Expected MaxQuant proteinGroups.txt with a 'Protein IDs' column; this is not that table")
flag_cols = ("Reverse", "Potential contaminant", "Only identified by site")
if not any(c in pg for c in flag_cols):
    raise ValueError("Expected MaxQuant proteinGroups.txt bookkeeping columns; received none of Reverse, Potential contaminant, Only identified by site")
keep = pd.Series(True, index=pg.index)
for col in flag_cols:
    if col in pg:
        keep &= pg[col].fillna("").ne("+")
rows_read, rows_kept = len(pg), int(keep.sum())
pg = pg.loc[keep].copy()
pg["leading_protein"] = pg["Protein IDs"].str.split(";").str[0]
pg["leading_gene"] = pg.get("Gene names", pd.Series("", index=pg.index)).fillna("").str.split(";").str[0]
lfq_cols = [c for c in pg.columns if c.startswith("LFQ intensity ")]
if not lfq_cols:
    raise ValueError("No LFQ intensity columns")
matrix = pg[["leading_protein", "leading_gene"] + lfq_cols].copy()
matrix[lfq_cols] = np.log2(matrix[lfq_cols].replace(0, np.nan))
matrix = matrix[matrix[lfq_cols].notna().any(axis=1)]

result = {
    "rows_read": rows_read,
    "after_bookkeeping": rows_kept,
    "quantified": len(matrix),
    "samples": len(lfq_cols),
    "infinite_values": int(np.isinf(matrix[lfq_cols].to_numpy()).sum()),
    "all_missing_groups": int(matrix[lfq_cols].isna().all(axis=1).sum()),
    "decoy_or_contaminant_survivors": int(pg["Protein IDs"].str.startswith(("REV__", "CON__")).sum()),
}
assert result == {
    "rows_read": 1560,
    "after_bookkeeping": 1500,
    "quantified": 1445,
    "samples": 8,
    "infinite_values": 0,
    "all_missing_groups": 0,
    "decoy_or_contaminant_survivors": 0,
}, result
print(json.dumps(result, indent=2))
