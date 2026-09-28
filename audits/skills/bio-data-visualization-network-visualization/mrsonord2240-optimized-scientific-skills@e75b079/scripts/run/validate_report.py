"""Validate the canonical final network-visualization audit report."""

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
    "e75b079fdd97b9186aabc46bda2e5ecaedd74d1c:"
    "skills/bio-data-visualization-network-visualization"
)
assert report["meta"]["n_inputs"] == 14
assert report["veto_gates"]["skill_veto"]["gate"] == "PASS"
assert report["veto_gates"]["research_veto"]["gate"] == "PASS"

categories = report["static_score"]["categories"]
assert len(categories) == 8
assert sum(item["score"] for item in categories.values()) == 98

inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == 14
assert [item["index"] for item in inputs] == list(range(1, 15))
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
assert execution_avg == report["dynamic_score"]["execution_avg"] == 95.7
assert (passed, total) == (70, 70)
assert report["dynamic_score"]["assertion_pass_rate"] == {
    "passed": passed,
    "total": total,
}

final = report["final"]
assert final["static_weighted"] == 39.2
assert final["dynamic_weighted"] == 57.4
assert final["score"] == round(39.2 + 57.4) == 97
assert final["grade"] == "Production Ready"
assert final["deployable"] is True
assert final["veto_override"] is False
assert report["recommendations"] == []

viewer = VIEWER.read_text(encoding="utf-8")
for expected in (
    "14 inputs",
    "97/100",
    "70/70",
    "0/0/0",
    "all 15 intended labels were individually read",
):
    assert expected in viewer, expected

print("VALID: 97/100 Production Ready; executed 14/14; assertions 70/70; P0/P1/P2 0/0/0")
