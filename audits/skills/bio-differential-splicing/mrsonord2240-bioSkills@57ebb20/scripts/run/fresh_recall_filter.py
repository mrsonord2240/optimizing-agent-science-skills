"""Fresh final-pass input: compare new versus legacy rMATS coverage selection.

Usage: python fresh_recall_filter.py <skill-folder> <SE.MATS.JC.txt>
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pandas as pd


text = (Path(sys.argv[1]) / "SKILL.md").read_text(encoding="utf-8")
match = re.search(r"def has_coverage_in_half_or_more_reps.*?axis=1,\n\)", text, re.DOTALL)
if match is None:
    raise SystemExit("coverage predicate missing from SKILL.md")
function_text, apply_text = match.group(0).split("se['coverage_ok'] = se.apply(\n", 1)
namespace = {"pd": pd}
exec(function_text, namespace)
namespace["se"] = pd.read_csv(sys.argv[2], sep="\t")
exec("se['coverage_ok'] = se.apply(\n" + apply_text, namespace)
se = namespace["se"]

def legacy_minimum(series: pd.Series) -> int:
    return min(int(v) for v in series.split(","))

legacy = (
    se["IJC_SAMPLE_1"].map(legacy_minimum).combine(se["IJC_SAMPLE_2"].map(legacy_minimum), min)
    + se["SJC_SAMPLE_1"].map(legacy_minimum).combine(se["SJC_SAMPLE_2"].map(legacy_minimum), min)
) >= 10
base = (se["FDR"] < 0.05) & (se["IncLevelDifference"].abs() > 0.10)
new_count = int((base & se["coverage_ok"]).sum())
old_count = int((base & legacy).sum())
assert new_count >= old_count, (new_count, old_count)
assert new_count > old_count, "fresh stress input did not demonstrate the intended recall improvement"
print(f"PASS: final predicate retains {new_count} significant events versus {old_count} under the legacy minima rule")
