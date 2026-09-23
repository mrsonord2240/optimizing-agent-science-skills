"""Validate Phase 2 report arithmetic and mandatory final-pass metadata."""
from pathlib import Path
import json

root = Path(r"F:\OpenScience\audits\bio-single-cell-cell-communication")
report = json.loads((root / "eval_report_bio-single-cell-cell-communication_result.json").read_text(encoding="utf-8"))
assert report["meta"]["source"] == "mrsonord2240/bioSkills@49c6f6943243f8faebc9848429c877be240d10d6:single-cell/cell-communication"
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == report["meta"]["n_inputs"] == 8
for item in inputs:
    assert "executed" in item and "execution_note" in item
    assert item["basic"] + item["specialized"] == item["total"]
    assert item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"])
    assert item["assertions_total"] == len(item["assertions"])
assert sum(v["score"] for v in report["static_score"]["categories"].values()) == report["static_score"]["subtotal"]
assert round(sum(i["total"] for i in inputs) / len(inputs), 1) == report["dynamic_score"]["execution_avg"]
assert report["dynamic_score"]["assertion_pass_rate"] == {"passed": 33, "total": 34}
assert report["final"]["static_weighted"] == 38.4
assert report["final"]["dynamic_weighted"] == 55.8
assert report["final"]["score"] == 94 and report["final"]["deployable"] is True
print("REPORT_VALID")
