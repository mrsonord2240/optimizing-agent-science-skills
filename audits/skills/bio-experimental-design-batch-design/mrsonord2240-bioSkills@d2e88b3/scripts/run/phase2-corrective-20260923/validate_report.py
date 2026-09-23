import json
from pathlib import Path

report_path = Path(__file__).parents[2] / "eval_report_bio-experimental-design-batch-design_result.json"
report = json.loads(report_path.read_text(encoding="utf-8"))
inputs = report["dynamic_score"]["inputs"]
assert report["meta"]["source"] == "mrsonord2240/bioSkills@d2e88b38777dd154d642d15cefe7e2ad1ccb2a0f:experimental-design/batch-design"
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert len(inputs) == 9 and all(item["executed"] and item["execution_note"] for item in inputs)
assert sum(item["assertions_passed"] for item in inputs) == 36
assert sum(item["assertions_total"] for item in inputs) == 36
assert round(sum(item["total"] for item in inputs) / len(inputs), 1) == report["dynamic_score"]["execution_avg"]
assert report["veto_gates"]["skill_veto"]["gate"] == "PASS"
assert report["final"]["deployable"] is True and report["final"]["veto_override"] is False
assert report["final"]["score"] == 97 and report["final"]["grade"] == "Production Ready"
print("PASS: report JSON, 9 executed inputs, 36/36 assertions, final-pass metadata, and deployable verdict validate.")
