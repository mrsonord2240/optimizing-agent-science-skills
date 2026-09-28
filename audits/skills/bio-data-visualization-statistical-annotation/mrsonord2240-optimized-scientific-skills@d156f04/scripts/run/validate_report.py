"""Validate the emitted report against the skill-auditor reporting contract."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "eval_report_bio-data-visualization-statistical-annotation_result.json"
VIEWER = ROOT / "eval_viewer_bio-data-visualization-statistical-annotation.md"
report = json.loads(REPORT.read_text(encoding="utf-8"))

expected_top = {
    "source",
    "meta",
    "veto_gates",
    "static_score",
    "dynamic_score",
    "final",
    "key_strengths",
    "recommendations",
}
assert set(report) == expected_top
assert report["source"] == (
    "mrsonord2240/optimized-scientific-skills@"
    "d156f04779dcde24d9e20270907be0557c28f654:"
    "skills/bio-data-visualization-statistical-annotation"
)
assert report["meta"]["auditor_independent"] is True
assert report["meta"]["n_inputs"] == 9

skill_veto = report["veto_gates"]["skill_veto"]
assert set(skill_veto) == {"gate", "stability", "contract", "determinism", "security"}
assert all(value == "PASS" for value in skill_veto.values())

research_veto = report["veto_gates"]["research_veto"]
assert set(research_veto) == {
    "applicable",
    "gate",
    "scientific_integrity",
    "practice_boundaries",
    "methodological_ground",
    "code_usability",
}
assert research_veto["applicable"] is True
assert research_veto["gate"] == "PASS"
for key in ("scientific_integrity", "practice_boundaries", "methodological_ground", "code_usability"):
    assert set(research_veto[key]) == {"result", "detail"}
    assert research_veto[key]["result"] == "PASS"

categories = report["static_score"]["categories"]
assert set(categories) == {
    "functional_suitability",
    "reliability",
    "performance_context",
    "agent_usability",
    "human_usability",
    "security",
    "maintainability",
    "agent_specific",
}
assert all(set(value) == {"score", "max", "note"} for value in categories.values())
static_total = sum(value["score"] for value in categories.values())
assert static_total == report["static_score"]["subtotal"] == 91

inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == report["meta"]["n_inputs"] == 9
assert [item["index"] for item in inputs] == list(range(1, 10))
for item in inputs:
    assert item["executed"] is True
    assert item["status"] == "COMPLETED"
    assert item["status_flag"] == "✅"
    assert item["basic"] + item["specialized"] == item["total"]
    assert 3 <= len(item["assertions"]) <= 5
    passes = sum(assertion["result"] == "PASS" for assertion in item["assertions"])
    assert passes == item["assertions_passed"]
    assert len(item["assertions"]) == item["assertions_total"]

execution_avg = round(sum(item["total"] for item in inputs) / len(inputs), 1)
assert execution_avg == report["dynamic_score"]["execution_avg"] == 94.8
passed = sum(item["assertions_passed"] for item in inputs)
total = sum(item["assertions_total"] for item in inputs)
assert report["dynamic_score"]["assertion_pass_rate"] == {"passed": passed, "total": total}
assert (passed, total) == (45, 45)

final = report["final"]
assert final["static_weighted"] == round(static_total * 0.4, 1) == 36.4
assert final["dynamic_weighted"] == round(execution_avg * 0.6, 1) == 56.9
assert final["score"] == round(final["static_weighted"] + final["dynamic_weighted"]) == 93
assert final["grade"] == "Production Ready"
assert final["grade_symbol"] == "⭐"
assert final["deployable"] is True
assert final["veto_override"] is False
assert 2 <= len(report["key_strengths"]) <= 5
priority_order = {"P0": 0, "P1": 1, "P2": 2}
assert [priority_order[item["priority"]] for item in report["recommendations"]] == sorted(
    priority_order[item["priority"]] for item in report["recommendations"]
)
assert all(item["priority"] == "P2" for item in report["recommendations"])
assert VIEWER.is_file() and VIEWER.stat().st_size > 1000

print("Report schema and arithmetic validation passed")
print(f"final={final['score']} grade={final['grade']} executed={len(inputs)}/{len(inputs)} assertions={passed}/{total}")
