"""Validate the canonical round-two network-visualization audit report."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "eval_report_bio-data-visualization-network-visualization_result.json"
VIEWER = ROOT / "eval_viewer_bio-data-visualization-network-visualization.md"

report = json.loads(REPORT.read_text(encoding="utf-8"))
assert set(report) == {
    "meta",
    "veto_gates",
    "static_score",
    "dynamic_score",
    "final",
    "key_strengths",
    "recommendations",
}
assert report["meta"]["source"] == (
    "mrsonord2240/optimized-scientific-skills@"
    "83008933c5298af81fe4b4604a39b291817bb47f:"
    "skills/bio-data-visualization-network-visualization"
)
assert report["meta"]["n_inputs"] == 12
assert report["veto_gates"]["skill_veto"]["gate"] == "PASS"
assert report["veto_gates"]["research_veto"]["gate"] == "PASS"

categories = report["static_score"]["categories"]
assert len(categories) == 8
assert sum(item["score"] for item in categories.values()) == 96

inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == 12
assert [item["index"] for item in inputs] == list(range(1, 13))
assert all(item["executed"] for item in inputs)
assert all(item["basic"] + item["specialized"] == item["total"] for item in inputs)
assert all(3 <= len(item["assertions"]) <= 5 for item in inputs)
assert all(
    item["assertions_passed"]
    == sum(check["result"] == "PASS" for check in item["assertions"])
    for item in inputs
)
assert all(
    item["assertions_total"] == len(item["assertions"])
    for item in inputs
)

execution_avg = round(sum(item["total"] for item in inputs) / len(inputs), 1)
passed = sum(item["assertions_passed"] for item in inputs)
total = sum(item["assertions_total"] for item in inputs)
assert execution_avg == report["dynamic_score"]["execution_avg"] == 94.7
assert (passed, total) == (59, 60)
assert report["dynamic_score"]["assertion_pass_rate"] == {
    "passed": passed,
    "total": total,
}

final = report["final"]
assert final["static_weighted"] == 38.4
assert final["dynamic_weighted"] == 56.8
assert final["score"] == round(38.4 + 56.8) == 95
assert final["grade"] == "Production Ready"
assert final["deployable"] is True
assert final["veto_override"] is False
assert [item["priority"] for item in report["recommendations"]] == ["P2"]

viewer = VIEWER.read_text(encoding="utf-8")
for expected in (
    "12 inputs",
    "95/100",
    "59/60",
    "0/0/1",
    "Improve Cytoscape label legibility after fitting",
):
    assert expected in viewer, expected

print("VALID: 95/100 Production Ready; executed 12/12; assertions 59/60; P0/P1/P2 0/0/1")
