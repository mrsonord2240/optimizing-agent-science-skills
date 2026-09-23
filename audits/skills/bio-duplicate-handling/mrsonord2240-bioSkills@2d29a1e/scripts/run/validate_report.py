"""Schema-level assertions for the fresh Phase 2 JSON report."""
import json
from pathlib import Path

report = Path(__file__).parents[1] / "eval_report_bio-duplicate-handling_result.json"
data = json.loads(report.read_text(encoding="utf-8"))
assert set(data) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}
assert data["meta"]["source"] == "mrsonord2240/bioSkills@2d29a1e3460345c6877ecf9f33c58a210ee5c727:alignment-files/duplicate-handling"
assert data["meta"]["auditor_independent"] is False
assert data["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
categories = data["static_score"]["categories"]
assert len(categories) == 8
assert sum(item["score"] for item in categories.values()) == data["static_score"]["subtotal"]
inputs = data["dynamic_score"]["inputs"]
assert len(inputs) == data["meta"]["n_inputs"] == 7
for item in inputs:
    assert item["executed"] is True
    assert isinstance(item["execution_note"], str) and item["execution_note"]
    assert 3 <= len(item["assertions"]) <= 5
    assert item["basic"] + item["specialized"] == item["total"]
    assert item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"])
    assert item["assertions_total"] == len(item["assertions"])
assert data["dynamic_score"]["assertion_pass_rate"] == {"passed": 34, "total": 35}
average = round(sum(item["total"] for item in inputs) / len(inputs), 1)
assert average == data["dynamic_score"]["execution_avg"]
assert data["final"]["static_weighted"] == 36.8
assert data["final"]["dynamic_weighted"] == 57.5
assert data["final"]["score"] == 94
assert data["final"]["grade"] == "Production Ready"
assert data["final"]["deployable"] is True and data["final"]["veto_override"] is False
assert 2 <= len(data["key_strengths"]) <= 5
print("REPORT_SCHEMA_ASSERTIONS_PASSED")
