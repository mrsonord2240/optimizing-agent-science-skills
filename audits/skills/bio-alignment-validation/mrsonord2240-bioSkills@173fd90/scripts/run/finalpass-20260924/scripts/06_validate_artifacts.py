"""Validate the final-pass report's required schema relationships.

Usage: python 06_validate_artifacts.py
"""
import json
from pathlib import Path


root = Path("/mnt/openscience/audits/bio-alignment-validation")
report_path = root / "eval_report_bio-alignment-validation_result.json"
viewer_path = root / "eval_viewer_bio-alignment-validation.md"
report = json.loads(report_path.read_text(encoding="utf-8"))

required_top_level = {
    "meta", "veto_gates", "static_score", "dynamic_score",
    "final", "key_strengths", "recommendations",
}
assert required_top_level <= report.keys()
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert len(report["dynamic_score"]["inputs"]) == report["meta"]["n_inputs"] == 7
categories = report["static_score"]["categories"]
assert len(categories) == 8
assert sum(item["score"] for item in categories.values()) == report["static_score"]["subtotal"]

for item in report["dynamic_score"]["inputs"]:
    assert 3 <= len(item["assertions"]) <= 5
    assert item["assertions_passed"] == sum(
        assertion["result"] == "PASS" for assertion in item["assertions"]
    )
    assert item["assertions_total"] == len(item["assertions"])
    assert item["basic"] + item["specialized"] == item["total"]

assert report["dynamic_score"]["assertion_pass_rate"] == {"passed": 28, "total": 28}
assert report["final"]["score"] == round(
    report["final"]["static_weighted"] + report["final"]["dynamic_weighted"]
)
assert report["final"]["grade"] == "Production Ready"
assert report["final"]["deployable"] is True
assert report["final"]["veto_override"] is False
assert len(report["key_strengths"]) in range(2, 6)
assert report["recommendations"] == []
assert "not an independent re-audit" in viewer_path.read_text(encoding="utf-8")
print("report_schema=PASS viewer=PASS score=95 auditor_independent=false")
