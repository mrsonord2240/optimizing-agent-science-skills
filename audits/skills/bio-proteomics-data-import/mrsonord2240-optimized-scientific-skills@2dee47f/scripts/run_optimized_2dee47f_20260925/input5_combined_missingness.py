"""Regression Input 5: compare DDA/DIA missingness after applying each documented import contract."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


root = Path(__file__).resolve().parents[1]

pg = pd.read_csv(root / "data" / "proteinGroups.txt", sep="\t", low_memory=False)
keep = pd.Series(True, index=pg.index)
for col in ("Reverse", "Potential contaminant", "Only identified by site"):
    if col in pg:
        keep &= pg[col].fillna("").ne("+")
pg = pg.loc[keep].copy()
pg["leading_protein"] = pg["Protein IDs"].str.split(";").str[0]
lfq_cols = [c for c in pg.columns if c.startswith("LFQ intensity ")]
dda = pg.set_index("leading_protein")[lfq_cols].replace(0, np.nan)
dda = np.log2(dda)
dda = dda[dda.notna().any(axis=1)]

raw = pd.read_parquet(root / "data" / "report.parquet")
raw = raw[(raw["Q.Value"] <= 0.01) & (raw["PG.Q.Value"] <= 0.01) & (raw["Global.PG.Q.Value"] <= 0.01)]
dia = raw.pivot_table(index="Protein.Group", columns="Run", values="PG.MaxLFQ", aggfunc="first")
dia = np.log2(dia.replace(0, np.nan))


def diagnose(frame: pd.DataFrame) -> dict:
    missing = frame.isna().sum(axis=1)
    corr = frame.mean(axis=1).corr(missing)
    return {
        "protein_groups": len(frame),
        "samples": frame.shape[1],
        "missing_percent": round(float(100 * frame.isna().sum().sum() / frame.size), 3),
        "abundance_missing_corr": round(float(corr), 3),
    }


result = {
    "dda": diagnose(dda),
    "dia": diagnose(dia),
    "overlap": len(set(dda.index).intersection(dia.index)),
    "recommendation": "Both correlations are negative; choose a left-censored or censoring-aware downstream method rather than assuming MCAR.",
}
assert result["dda"]["protein_groups"] == 1445, result
assert result["dia"]["protein_groups"] == 887, result
assert result["dda"]["abundance_missing_corr"] < -0.4, result
assert result["dia"]["abundance_missing_corr"] < -0.3, result
assert result["dia"]["missing_percent"] < result["dda"]["missing_percent"], result
assert result["overlap"] > 700, result
print(json.dumps(result, indent=2))
