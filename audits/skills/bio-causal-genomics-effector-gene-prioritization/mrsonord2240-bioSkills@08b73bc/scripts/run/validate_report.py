"""Validate the audit report's required Phase-2 invariants."""
import json
from pathlib import Path

audit = Path(r"F:\OpenScience\audits\bio-causal-genomics-effector-gene-prioritization")
report = json.loads((audit / "eval_report_bio-causal-genomics-effector-gene-prioritization_result.json").read_text(encoding="utf-8"))

assert report["meta"]["source"] == "mrsonord2240/bioSkills@08b73bcd2fbccf8b3b667d3805881c98d3b4e6b5:causal-genomics/effector-gene-prioritization"
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == report["meta"]["n_inputs"] == 10
assert all("executed" in row and "execution_note" in row for row in inputs)
assert all(3 <= len(row["assertions"]) <= 5 for row in inputs)
assert all(row["basic"] + row["specialized"] == row["total"] for row in inputs)
assert sum(row["total"] for row in inputs) / len(inputs) == report["dynamic_score"]["execution_avg"]
assert sum(row["assertions_passed"] for row in inputs) == report["dynamic_score"]["assertion_pass_rate"]["passed"]
assert sum(row["assertions_total"] for row in inputs) == report["dynamic_score"]["assertion_pass_rate"]["total"]
assert report["final"] == {"static_weighted": 37.2, "dynamic_weighted": 56.7, "score": 94, "max": 100, "grade": "Production Ready", "grade_symbol": "⭐", "deployable": True, "veto_override": False}
assert (audit / "eval_viewer_bio-causal-genomics-effector-gene-prioritization.md").is_file()
print("REPORT ASSERTIONS PASS: source tip, final-pass metadata, ten explicit inputs, scores, assertions, and viewer are valid.")
