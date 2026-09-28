"""Validate the canonical round-2 JSON report and evidence contract."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(r"F:\OpenScience\audits\bio-data-visualization-dimensionality-reduction-plots")
report = json.loads((ROOT / "eval_report_bio-data-visualization-dimensionality-reduction-plots_result.json").read_text(encoding="utf-8"))
assert report["meta"]["n_inputs"] == 11
assert report["meta"]["source"].startswith("mrsonord2240/optimized-scientific-skills@228b1caf")
assert report["veto_gates"]["skill_veto"]["gate"] == "PASS"
assert report["veto_gates"]["research_veto"]["gate"] == "PASS"
categories = report["static_score"]["categories"]
assert len(categories) == 8
assert sum(value["score"] for value in categories.values()) == report["static_score"]["subtotal"] == 96
inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == 11
assert all(item["basic"] + item["specialized"] == item["total"] for item in inputs)
assert all(3 <= len(item["assertions"]) <= 5 for item in inputs)
assert all(item["assertions_passed"] == sum(assertion["result"] == "PASS" for assertion in item["assertions"]) for item in inputs)
passed = sum(item["assertions_passed"] for item in inputs)
total = sum(item["assertions_total"] for item in inputs)
assert (passed, total) == (55, 55)
average = round(sum(item["total"] for item in inputs) / len(inputs), 1)
assert average == report["dynamic_score"]["execution_avg"] == 94.5
assert report["final"]["static_weighted"] == 38.4
assert report["final"]["dynamic_weighted"] == 56.7
assert report["final"]["score"] == 95
assert report["final"]["grade"] == "Production Ready"
assert report["final"]["deployable"] is True
assert report["recommendations"] == []
assert (ROOT / "eval_viewer_bio-data-visualization-dimensionality-reduction-plots.md").is_file()
print(f"validated inputs={len(inputs)} assertions={passed}/{total} average={average} final={report['final']['score']} recommendations=0")
