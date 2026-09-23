"""Validate the final-pass audit JSON cardinality and arithmetic contract."""
from pathlib import Path
import json

report = Path(__file__).resolve().parents[2] / "eval_report_bio-crispr-screens-in-vivo-screens_result.json"
data = json.loads(report.read_text(encoding="utf-8"))
assert data["meta"]["auditor_independent"] is False
assert data["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert data["meta"]["source"] == "mrsonord2240/bioSkills@afcf1e65250223117c255217b1974abc625f5741:crispr-screens/in-vivo-screens"
categories = data["static_score"]["categories"]
assert len(categories) == 8
assert sum(v["score"] for v in categories.values()) == data["static_score"]["subtotal"]
inputs = data["dynamic_score"]["inputs"]
assert len(inputs) == data["meta"]["n_inputs"] == 7
for row in inputs:
    assert row["executed"] is True and row["execution_note"]
    assert 3 <= len(row["assertions"]) <= 5
    assert row["basic"] + row["specialized"] == row["total"]
    assert row["assertions_passed"] == sum(a["result"] == "PASS" for a in row["assertions"])
    assert row["assertions_total"] == len(row["assertions"])
assert sum(row["assertions_passed"] for row in inputs) == 27
assert sum(row["assertions_total"] for row in inputs) == 28
assert sum(row["total"] for row in inputs) / len(inputs) == data["dynamic_score"]["execution_avg"]
assert data["final"]["static_weighted"] == 37.6
assert data["final"]["dynamic_weighted"] == 54.6
assert data["final"]["score"] == 92
assert data["final"]["deployable"] is True and data["final"]["veto_override"] is False
assert all(data["recommendations"][i]["priority"] <= data["recommendations"][i + 1]["priority"] for i in range(len(data["recommendations"]) - 1))
print("report_schema_and_arithmetic=PASS; inputs=7; assertions=27/28; final=92")
