import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    report = json.load(handle)

assert set(report) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}
assert report["meta"]["source"] == "mrsonord2240/bioSkills@e14c7b581acaa271a9bf643febcb5ff0dd40d966:single-cell/scatac-analysis"
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == report["meta"]["n_inputs"] == 7
assert all(row["executed"] is True and row["execution_note"] for row in inputs)
assert all(3 <= len(row["assertions"]) <= 5 for row in inputs)
assert sum(row["assertions_passed"] for row in inputs) == report["dynamic_score"]["assertion_pass_rate"]["passed"]
assert sum(row["assertions_total"] for row in inputs) == report["dynamic_score"]["assertion_pass_rate"]["total"]
assert round(sum(row["total"] for row in inputs) / len(inputs), 1) == report["dynamic_score"]["execution_avg"]
assert report["final"]["score"] == round(report["final"]["static_weighted"] + report["final"]["dynamic_weighted"])
assert report["veto_gates"]["research_veto"]["code_usability"]["result"] == "PASS"
assert report["final"]["veto_override"] is False and report["final"]["deployable"] is True
print("report_contract=PASS inputs=7 executed=7 source_tip=e14c7b5 veto=M4_PASS")
