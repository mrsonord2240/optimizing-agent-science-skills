"""Validate the report arithmetic and final-pass metadata before handoff."""
import json
from pathlib import Path

report = json.loads(Path("../../eval_report_bio-single-cell-multimodal-integration_result.json").read_text(encoding="utf-8"))
assert report["source"].startswith("mrsonord2240/bioSkills@187625ad0a1a89640fcb91cae6b727d63dc8fac1:")
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == report["meta"]["n_inputs"] == 10
for item in inputs:
    assert item["executed"] is True and item["execution_note"]
    assert 3 <= len(item["assertions"]) <= 5
    assert item["basic"] + item["specialized"] == item["total"]
    assert item["assertions_passed"] == sum(row["result"] == "PASS" for row in item["assertions"])
assert report["static_score"]["subtotal"] == sum(v["score"] for v in report["static_score"]["categories"].values())
assert report["dynamic_score"]["execution_avg"] == round(sum(row["total"] for row in inputs) / len(inputs), 1)
assert report["dynamic_score"]["assertion_pass_rate"] == {"passed": 41, "total": 45}
assert report["final"]["static_weighted"] == 30.8
assert report["final"]["dynamic_weighted"] == 48.8
assert report["final"]["score"] == 80
assert report["final"]["veto_override"] is True and report["final"]["deployable"] is False
assert report["veto_gates"]["research_veto"]["code_usability"]["result"] == "FAIL"
print("PHASE2_REPORT_VALID inputs=10 assertions=41/45 final=80 veto=M4")
