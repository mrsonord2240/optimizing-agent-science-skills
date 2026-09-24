# Validate the exact-commit re-audit report's required arithmetic and cardinalities.
# Run with: py.sh validate_reaudit_report.py <report.json>
import json
import pathlib
import sys

report = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
assert report["meta"]["source"].startswith("mrsonord2240/bioSkills@25b3d2162f76de9b1d0b5d98533bf76f7c970b05:")
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
categories = report["static_score"]["categories"]
assert len(categories) == 8 and sum(item["score"] for item in categories.values()) == report["static_score"]["subtotal"]
inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == report["meta"]["n_inputs"] == 7
for item in inputs:
    assert 3 <= len(item["assertions"]) <= 5
    assert item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"])
    assert item["assertions_total"] == len(item["assertions"])
    assert item["basic"] + item["specialized"] == item["total"]
average = round(sum(item["total"] for item in inputs) / len(inputs), 1)
assert average == report["dynamic_score"]["execution_avg"]
assert report["dynamic_score"]["assertion_pass_rate"] == {"passed": 28, "total": 28}
assert report["final"]["static_weighted"] == round(report["static_score"]["subtotal"] * .4, 1)
assert report["final"]["dynamic_weighted"] == round(average * .6, 1)
assert report["final"]["score"] == round(report["final"]["static_weighted"] + report["final"]["dynamic_weighted"], 1)
assert report["final"]["grade"] == "Production Ready" and report["final"]["deployable"] is True
print("PASS: report JSON cardinalities, exact source, final-pass metadata, arithmetic, and Production Ready gates")
