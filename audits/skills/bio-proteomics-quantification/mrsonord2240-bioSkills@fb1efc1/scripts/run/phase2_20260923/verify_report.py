"""Validate the final-pass report's required arithmetic and per-input execution metadata."""
import json
from pathlib import Path

report = Path(r"F:\OpenScience\audits\bio-proteomics-quantification\eval_report_bio-proteomics-quantification_result.json")
d = json.loads(report.read_text(encoding="utf-8"))
inputs = d["dynamic_score"]["inputs"]
assert len(inputs) == d["meta"]["n_inputs"] == 13
assert d["meta"]["auditor_independent"] is False and "final pass" in d["meta"]["note"]
assert all("executed" in x and "execution_note" in x for x in inputs)
assert all(3 <= len(x["assertions"]) <= 5 for x in inputs)
assert all(x["basic"] + x["specialized"] == x["total"] for x in inputs)
assert all(x["assertions_passed"] == sum(a["result"] == "PASS" for a in x["assertions"]) for x in inputs)
assert round(sum(x["total"] for x in inputs) / len(inputs), 1) == d["dynamic_score"]["execution_avg"]
assert d["static_score"]["subtotal"] == sum(x["score"] for x in d["static_score"]["categories"].values())
assert d["final"]["veto_override"] and not d["final"]["deployable"] and d["final"]["grade"] == "Reject"
print("report=valid inputs=13 executed=12 assertions=48/52 final=Reject veto_override=true")
