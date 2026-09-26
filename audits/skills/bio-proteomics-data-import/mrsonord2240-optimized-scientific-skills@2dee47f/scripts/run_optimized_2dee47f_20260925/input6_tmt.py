"""Fresh Input 6: import already-corrected MaxQuant TMT reporter channels."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


path = Path(__file__).resolve().parents[1] / "data" / "tmt_proteinGroups.txt"
pg = pd.read_csv(path, sep="\t", low_memory=False)
flag_cols = ("Reverse", "Potential contaminant", "Only identified by site")
if "Protein IDs" not in pg or not any(c in pg for c in flag_cols):
    raise ValueError("Expected MaxQuant proteinGroups.txt with Protein IDs and at least one bookkeeping column")
keep = pd.Series(True, index=pg.index)
for col in flag_cols:
    if col in pg:
        keep &= pg[col].fillna("").ne("+")
pg = pg.loc[keep].copy()
pg["leading_protein"] = pg["Protein IDs"].str.split(";").str[0]
pg["leading_gene"] = pg.get("Gene names", pd.Series("", index=pg.index)).fillna("").str.split(";").str[0]
reporter_cols = [c for c in pg.columns if c.startswith("Reporter intensity corrected ")]
if not reporter_cols:
    raise ValueError("No 'Reporter intensity corrected <channel>' columns")
tmt = pg[["leading_protein", "leading_gene"] + reporter_cols].copy()
tmt[reporter_cols] = np.log2(tmt[reporter_cols].replace(0, np.nan))
tmt = tmt[tmt[reporter_cols].notna().any(axis=1)]

result = {
    "protein_groups": len(tmt),
    "reporter_channels": len(reporter_cols),
    "matrix_columns_including_labels": len(tmt.columns),
    "infinite_values": int(np.isinf(tmt[reporter_cols].to_numpy()).sum()),
    "missing_values": int(tmt[reporter_cols].isna().sum().sum()),
    "single_group_total_intensity_used": "Intensity" in reporter_cols,
}
assert result == {
    "protein_groups": 389,
    "reporter_channels": 10,
    "matrix_columns_including_labels": 12,
    "infinite_values": 0,
    "missing_values": 1,
    "single_group_total_intensity_used": False,
}, result
print(json.dumps(result, indent=2))
