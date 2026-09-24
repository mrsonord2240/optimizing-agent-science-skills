"""Validate the final-pass report invariants required by report_json_schema.md."""
import json
from pathlib import Path

report = Path(__file__).parents[1] / "eval_report_bio-alignment-sorting_result.json"
data = json.loads(report.read_text(encoding="utf-8"))
assert set(data) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}
assert data["meta"]["auditor_independent"] is False
assert data["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert len(data["dynamic_score"]["inputs"]) == data["meta"]["n_inputs"] == 7
assert round(sum(item["total"] for item in data["dynamic_score"]["inputs"]) / 7, 1) == data["dynamic_score"]["execution_avg"]
assert sum(item["assertions_passed"] for item in data["dynamic_score"]["inputs"]) == 28
assert sum(item["assertions_total"] for item in data["dynamic_score"]["inputs"]) == 28
assert sum(item["score"] for item in data["static_score"]["categories"].values()) == data["static_score"]["subtotal"] == 94
assert data["final"] == {"static_weighted": 37.6, "dynamic_weighted": 57.7, "score": 95, "max": 100, "grade": "Production Ready", "grade_symbol": "⭐", "deployable": True, "veto_override": False}
assert data["recommendations"] == []
print("PASS: schema structure and final-pass invariants are valid")
