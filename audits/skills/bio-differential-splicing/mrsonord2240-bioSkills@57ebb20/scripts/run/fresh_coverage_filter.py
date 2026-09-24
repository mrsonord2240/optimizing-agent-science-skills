"""Fresh final-pass input: execute the coverage code embedded in SKILL.md.

Usage: python fresh_coverage_filter.py <run/skill folder>
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
namespace["se"] = pd.DataFrame(
    {
        "IJC_SAMPLE_1": ["5,100", "4,4"],
        "SJC_SAMPLE_1": ["100,5", "4,4"],
        "IJC_SAMPLE_2": ["7,50", "3,3"],
        "SJC_SAMPLE_2": ["50,7", "3,3"],
    }
)
exec("se['coverage_ok'] = se.apply(\n" + apply_text, namespace)
got = namespace["se"]["coverage_ok"].tolist()
assert got == [True, False], got
print("PASS: discordant-minima event retained; shallow event rejected")
