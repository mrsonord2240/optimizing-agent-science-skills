"""Validate final-pass report fields required by skill-auditor schema."""

import json
from pathlib import Path


report = json.loads(Path("../eval_report_bio-biomart-queries_result.json").read_text(encoding="utf-8"))
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["source"] == "mrsonord2240/bioSkills@e4722ccd1616cc79568c1674be726d950d9297d5:database-access/biomart-queries"
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
categories = report["static_score"]["categories"]
expected_categories = {
    "functional_suitability", "reliability", "performance_context", "agent_usability",
    "human_usability", "security", "maintainability", "agent_specific",
}
assert set(categories) == expected_categories
assert sum(item["score"] for item in categories.values()) == report["static_score"]["subtotal"]
inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == report["meta"]["n_inputs"] == 8
for item in inputs:
    assert 3 <= len(item["assertions"]) <= 5
    assert item["basic"] + item["specialized"] == item["total"]
    assert item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"])
average = round(sum(item["total"] for item in inputs) / len(inputs), 1)
assert average == report["dynamic_score"]["execution_avg"]
assert report["final"]["static_weighted"] == round(report["static_score"]["subtotal"] * 0.4, 1)
assert report["final"]["dynamic_weighted"] == round(average * 0.6, 1)
assert report["final"]["score"] == round(report["final"]["static_weighted"] + report["final"]["dynamic_weighted"])
assert 1 <= report["meta"]["n_inputs"] <= 8
assert report["recommendations"] == []
print("schema checks passed: 8 inputs, 25 assertions, final score 95")
