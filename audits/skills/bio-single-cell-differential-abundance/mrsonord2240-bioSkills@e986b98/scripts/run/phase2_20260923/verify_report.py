"""Validate required audit-report arithmetic and final-pass metadata."""
import json
from pathlib import Path

report = Path(__file__).parents[2] / "eval_report_bio-single-cell-differential-abundance_result.json"
data = json.loads(report.read_text(encoding="utf-8"))
assert data["meta"]["auditor_independent"] is False
assert data["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
inputs = data["dynamic_score"]["inputs"]
assert len(inputs) == data["meta"]["n_inputs"] == 7
for item in inputs:
    assert isinstance(item["executed"], bool) and item["execution_note"]
    assert 3 <= len(item["assertions"]) <= 5
    assert item["basic"] + item["specialized"] == item["total"]
    assert item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"])
    assert item["assertions_total"] == len(item["assertions"])
assert sum(v["score"] for v in data["static_score"]["categories"].values()) == data["static_score"]["subtotal"]
assert round(sum(i["total"] for i in inputs) / len(inputs), 1) == data["dynamic_score"]["execution_avg"]
assert data["final"]["veto_override"] is True and data["final"]["deployable"] is False
assert data["veto_gates"]["research_veto"]["code_usability"]["result"] == "FAIL"
print("REPORT_SCHEMA_AND_ARITHMETIC_OK")
