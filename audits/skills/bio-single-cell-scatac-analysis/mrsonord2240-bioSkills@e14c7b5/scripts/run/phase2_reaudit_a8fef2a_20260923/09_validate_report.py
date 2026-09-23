# Purpose: Validate the audit JSON's key contract fields and arithmetic.
# Usage: python 09_validate_report.py <report.json>
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    report = json.load(handle)

assert report["meta"]["source"].startswith("mrsonord2240/bioSkills@a8fef2a02c45b710257e1f5606171fa462e817a8:")
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == report["meta"]["n_inputs"] == 7
assert all("executed" in row and "execution_note" in row for row in inputs)
assert all(row["executed"] is True for row in inputs)
assert sum(row["assertions_passed"] for row in inputs) == report["dynamic_score"]["assertion_pass_rate"]["passed"]
assert sum(row["assertions_total"] for row in inputs) == report["dynamic_score"]["assertion_pass_rate"]["total"]
assert round(sum(row["total"] for row in inputs) / len(inputs), 1) == report["dynamic_score"]["execution_avg"]
assert report["final"]["score"] == round(report["final"]["static_weighted"] + report["final"]["dynamic_weighted"])
assert report["veto_gates"]["research_veto"]["code_usability"]["result"] == "FAIL"
assert report["final"]["veto_override"] is True and report["final"]["deployable"] is False
print("report_contract=PASS inputs=7 executed=7 source_tip=a8fef2a veto=M4_FAIL")
