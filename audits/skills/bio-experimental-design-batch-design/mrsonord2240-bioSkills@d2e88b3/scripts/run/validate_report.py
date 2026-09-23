"""Validate core final-pass report invariants without touching audited source."""
import json
from pathlib import Path

report_path = Path(__file__).parents[1] / "eval_report_bio-experimental-design-batch-design_result.json"
report = json.loads(report_path.read_text(encoding="utf-8"))
inputs = report["dynamic_score"]["inputs"]
assert report["meta"]["source"].startswith("mrsonord2240/bioSkills@d2e88b38777dd154d642d15cefe7e2ad1ccb2a0f:")
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert len(inputs) == 9 and all(item["executed"] and item["execution_note"] for item in inputs)
assert sum(item["assertions_passed"] for item in inputs) == 35
assert sum(item["assertions_total"] for item in inputs) == 36
assert round(sum(item["total"] for item in inputs) / len(inputs), 1) == report["dynamic_score"]["execution_avg"]
assert report["veto_gates"]["skill_veto"]["gate"] == "FAIL"
assert report["final"]["deployable"] is False and report["final"]["veto_override"] is True
print("PASS: report JSON parses and final-pass invariants hold.")
