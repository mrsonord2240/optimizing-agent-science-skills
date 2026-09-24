import json
import sys

report = json.load(open(sys.argv[1], encoding="utf-8"))
assert set(report) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}
assert report["meta"]["source"] == "mrsonord2240/bioSkills@4f7306b54e8c445d251d352bb85e01ced4c7a3b4:single-cell/multimodal-integration"
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == report["meta"]["n_inputs"] == 10
assert all(row["executed"] is True and row["execution_note"] for row in inputs)
assert all(3 <= len(row["assertions"]) <= 5 for row in inputs)
assert sum(row["assertions_passed"] for row in inputs) == report["dynamic_score"]["assertion_pass_rate"]["passed"]
assert sum(row["assertions_total"] for row in inputs) == report["dynamic_score"]["assertion_pass_rate"]["total"]
assert round(sum(row["total"] for row in inputs) / len(inputs), 1) == report["dynamic_score"]["execution_avg"]
assert report["final"]["score"] == round(report["final"]["static_weighted"] + report["final"]["dynamic_weighted"])
assert report["veto_gates"]["research_veto"]["code_usability"]["result"] == "PASS"
assert report["final"]["deployable"] is True and report["final"]["veto_override"] is False
print("report_contract=PASS inputs=10 executed=10 source_tip=4f7306b M4=PASS")
