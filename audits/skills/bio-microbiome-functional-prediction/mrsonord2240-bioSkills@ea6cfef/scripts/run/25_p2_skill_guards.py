#!/usr/bin/env python3
"""Executed direct-mode checks for route/scope and anti-overclaim outputs."""
from pathlib import Path
skill = Path(r"F:/OpenScience/wt/microbiome-functional-prediction/microbiome/functional-prediction/SKILL.md").read_text(encoding="utf-8")
checks = {
    "marine_route": "Soil / marine / sediment / novel environment, biogeochemical question | FAPROTAX",
    "activity_guard": "Potential, never activity.",
    "circularity_guard": "Predicted function is a DETERMINISTIC function of the ASV table",
    "measured_route": "MEASURED shotgun function",
    "linda_prevalence_guard": "prev.filter = 0.1",
    "q2_route": "q2-picrust2 plugin",
}
for name, phrase in checks.items():
    assert phrase in skill, f"missing {name}: {phrase}"
    print(f"{name}=PASS")
