"""Validate the final-pass report for bio-single-cell-preprocessing.

Usage:
    python validate_report.py
"""

import json
from pathlib import Path


audit_dir = Path(__file__).resolve().parents[2]
report_path = audit_dir / "eval_report_bio-single-cell-preprocessing_result.json"
viewer_path = audit_dir / "eval_viewer_bio-single-cell-preprocessing.md"
data = json.loads(report_path.read_text(encoding="utf-8"))

assert set(data) == {
    "meta",
    "veto_gates",
    "static_score",
    "dynamic_score",
    "final",
    "key_strengths",
    "recommendations",
}

meta = data["meta"]
assert meta["source"] == (
    "mrsonord2240/bioSkills@"
    "a6550a1a7aca3cfa156d65780278acb017e54d94:single-cell/preprocessing"
)
assert meta["auditor_independent"] is False
assert meta["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert meta["n_inputs"] == 7

skill_veto = data["veto_gates"]["skill_veto"]
assert skill_veto == {
    "gate": "PASS",
    "stability": "PASS",
    "contract": "PASS",
    "determinism": "PASS",
    "security": "PASS",
}
research_veto = data["veto_gates"]["research_veto"]
assert research_veto["applicable"] is True
assert research_veto["gate"] == "PASS"
assert all(
    research_veto[key]["result"] == "PASS"
    for key in (
        "scientific_integrity",
        "practice_boundaries",
        "methodological_ground",
        "code_usability",
    )
)

static = data["static_score"]
assert len(static["categories"]) == 8
assert static["subtotal"] == sum(item["score"] for item in static["categories"].values()) == 92

dynamic = data["dynamic_score"]
inputs = dynamic["inputs"]
assert len(inputs) == 7
assert all(item["status"] in {"COMPLETED", "PARTIAL", "ERROR"} for item in inputs)
assert all(3 <= len(item["assertions"]) <= 5 for item in inputs)
assert all(item["basic"] + item["specialized"] == item["total"] for item in inputs)
assert all(
    item["assertions_passed"]
    == sum(assertion["result"] == "PASS" for assertion in item["assertions"])
    == item["assertions_total"]
    for item in inputs
)
assert dynamic["assertion_pass_rate"] == {"passed": 28, "total": 28}
assert dynamic["execution_avg"] == round(sum(item["total"] for item in inputs) / len(inputs), 1) == 92.3

assert data["final"] == {
    "static_weighted": 36.8,
    "dynamic_weighted": 55.4,
    "score": 92,
    "max": 100,
    "grade": "Production Ready",
    "grade_symbol": "⭐",
    "deployable": True,
    "veto_override": False,
}
assert data["recommendations"] == []

viewer = viewer_path.read_text(encoding="utf-8")
assert meta["source"] in viewer
assert "**92/100**" in viewer
assert "**Assertion Pass Rate: 28/28**" in viewer

print("final-pass report JSON and viewer invariants: PASS")
