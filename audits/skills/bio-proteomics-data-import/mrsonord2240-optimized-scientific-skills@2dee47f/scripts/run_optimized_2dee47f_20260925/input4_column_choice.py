"""Regression Input 4a: verify LFQ, raw Intensity, and iBAQ guidance on a weak-loading run."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


path = Path(__file__).resolve().parents[1] / "data" / "proteinGroups_failed.txt"
pg = pd.read_csv(path, sep="\t", low_memory=False)
keep = pd.Series(True, index=pg.index)
for col in ("Reverse", "Potential contaminant", "Only identified by site"):
    if col in pg:
        keep &= pg[col].fillna("").ne("+")
pg = pg.loc[keep].copy()


def family(prefix: str) -> pd.DataFrame:
    cols = [c for c in pg.columns if c.startswith(prefix)]
    return np.log2(pg[cols].replace(0, np.nan)).rename(columns=lambda c: c.removeprefix(prefix))


intensity = family("Intensity ")
ibaq = family("iBAQ ")
lfq = family("LFQ intensity ")
assert list(intensity.columns) == list(ibaq.columns) == list(lfq.columns)
weak = "T4"
others = [c for c in lfq.columns if c != weak]


def weak_residual(frame: pd.DataFrame) -> float:
    return float((frame[weak] - frame[others].mean(axis=1)).median())


ratio_sd = np.nanmax(np.nanstd((ibaq - intensity).to_numpy(), axis=1))
result = {
    "samples": len(lfq.columns),
    "intensity_T4_residual_log2": round(weak_residual(intensity), 3),
    "ibaq_T4_residual_log2": round(weak_residual(ibaq), 3),
    "lfq_T4_residual_log2": round(weak_residual(lfq), 3),
    "max_within_protein_sd_log2_ibaq_over_intensity": round(float(ratio_sd), 8),
    "recommendation": "LFQ intensity for between-sample comparison; iBAQ only as a within-sample molar proxy.",
}
assert result["intensity_T4_residual_log2"] < -1.0, result
assert result["ibaq_T4_residual_log2"] < -1.0, result
assert abs(result["lfq_T4_residual_log2"]) < 0.2, result
assert result["max_within_protein_sd_log2_ibaq_over_intensity"] == 0.0, result
print(json.dumps(result, indent=2))
