"""Validate Phase 2 report invariants required by the audit protocol."""
import json
from pathlib import Path

path = Path(r"F:\OpenScience\audits\bio-single-cell-trajectory-inference\eval_report_bio-single-cell-trajectory-inference_result.json")
report = json.loads(path.read_text(encoding="utf-8"))
assert report["meta"]["source"] == "mrsonord2240/bioSkills@4ce42c1553b0f2ae3e4c068a8d5f7e1566b5c2d1:single-cell/trajectory-inference"
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == report["meta"]["n_inputs"] == 7
assert all(row["executed"] is True and row["execution_note"] for row in inputs)
assert all(3 <= len(row["assertions"]) <= 5 for row in inputs)
assert all(row["basic"] + row["specialized"] == row["total"] for row in inputs)
assert sum(row["assertions_passed"] for row in inputs) == 28
assert sum(row["assertions_total"] for row in inputs) == 28
assert report["final"]["deployable"] is True and report["final"]["veto_override"] is False
print("json_parse=PASS; dynamic_inputs=7/7_explicit_executed_notes; assertions=28/28; final_metadata=PASS")
