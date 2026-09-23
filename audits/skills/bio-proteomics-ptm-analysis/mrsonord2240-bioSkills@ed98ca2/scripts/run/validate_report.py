#!/usr/bin/env python3
"""Schema arithmetic and final-pass metadata checks for this audit report."""
import json
from pathlib import Path

report = Path(__file__).parents[1] / "eval_report_bio-proteomics-ptm-analysis_result.json"
data = json.loads(report.read_text(encoding="utf-8"))
assert data["meta"]["source"] == "mrsonord2240/bioSkills@ed98ca281137434ee3b3ffe1cce5d5ba717d51b6:proteomics/ptm-analysis"
assert data["meta"]["auditor_independent"] is False
assert data["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
inputs = data["dynamic_score"]["inputs"]
assert len(inputs) == data["meta"]["n_inputs"] == 7
for item in inputs:
    assert item["executed"] is True and item["execution_note"]
    assert 3 <= len(item["assertions"]) <= 5
    assert item["basic"] + item["specialized"] == item["total"]
    assert item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"])
assert data["static_score"]["subtotal"] == sum(v["score"] for v in data["static_score"]["categories"].values())
mean = round(sum(i["total"] for i in inputs) / len(inputs), 1)
assert mean == data["dynamic_score"]["execution_avg"]
assert round(data["static_score"]["subtotal"] * .4, 1) == data["final"]["static_weighted"]
assert round(mean * .6, 1) == data["final"]["dynamic_weighted"]
assert round(data["final"]["static_weighted"] + data["final"]["dynamic_weighted"]) == data["final"]["score"]
print("report validation PASS")
