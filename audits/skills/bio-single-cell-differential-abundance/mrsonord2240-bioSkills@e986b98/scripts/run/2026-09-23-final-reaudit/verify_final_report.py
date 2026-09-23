"""Validate final-pass report schema arithmetic and repaired-source evidence."""
import json
from pathlib import Path

run_dir = Path(__file__).parent
audit_root = run_dir.parents[1]
report = audit_root / "eval_report_bio-single-cell-differential-abundance_result.json"
data = json.loads(report.read_text(encoding="utf-8"))
assert data["meta"]["source"].endswith("e986b98c85b38b4ad31ee9289f5aa39f6bec212b:single-cell/differential-abundance")
assert data["meta"]["auditor_independent"] is False
assert data["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert data["veto_gates"]["skill_veto"]["gate"] == "PASS"
assert data["veto_gates"]["research_veto"]["gate"] == "PASS"
assert data["veto_gates"]["research_veto"]["code_usability"]["result"] == "PASS"
inputs = data["dynamic_score"]["inputs"]
assert len(inputs) == data["meta"]["n_inputs"] == 7
for item in inputs:
    assert item["executed"] is True and item["execution_note"]
    assert 3 <= len(item["assertions"]) <= 5
    assert item["basic"] + item["specialized"] == item["total"]
    assert item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"])
    assert item["assertions_total"] == len(item["assertions"])
assert sum(v["score"] for v in data["static_score"]["categories"].values()) == data["static_score"]["subtotal"]
assert round(sum(i["total"] for i in inputs) / len(inputs), 1) == data["dynamic_score"]["execution_avg"]
assert data["final"]["static_weighted"] == 34.4
assert data["final"]["dynamic_weighted"] == 55.3
assert data["final"]["score"] == 90
assert data["final"]["deployable"] is True and data["final"]["veto_override"] is False
assert "PASS_MILO_INLINE_FULL_PATH" in (run_dir / "input6_milo_inline_full_path.log").read_text(encoding="utf-8", errors="replace")
assert "PASS_SCCODA_INLINE_FULL_PATH" in (run_dir / "input7_sccoda_inline_full_path.log").read_text(encoding="utf-8", errors="replace")
print("FINAL_REPORT_SCHEMA_ARITHMETIC_AND_M4_EVIDENCE_OK")
