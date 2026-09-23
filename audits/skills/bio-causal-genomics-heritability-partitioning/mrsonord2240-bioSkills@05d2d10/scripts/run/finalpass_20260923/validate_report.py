"""Validate final-pass report structure and score arithmetic."""
import json
from pathlib import Path

path = Path(r"F:\OpenScience\audits\bio-causal-genomics-heritability-partitioning\eval_report_bio-causal-genomics-heritability-partitioning_result.json")
report = json.loads(path.read_text(encoding="utf-8"))
inputs = report["dynamic_score"]["inputs"]
assert report["meta"]["n_inputs"] == len(inputs) == 11
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert sum(v["score"] for v in report["static_score"]["categories"].values()) == 93
assert all(i["basic"] + i["specialized"] == i["total"] for i in inputs)
assert all("executed" in i and "execution_note" in i for i in inputs)
assert all(3 <= len(i["assertions"]) <= 5 for i in inputs)
assert sum(i["assertions_passed"] for i in inputs) == 41
assert sum(i["assertions_total"] for i in inputs) == 43
assert round(sum(i["total"] for i in inputs) / len(inputs), 1) == 96.1
assert report["final"]["score"] == round(report["final"]["static_weighted"] + report["final"]["dynamic_weighted"])
print("REPORT_VALID inputs=11 assertions=41/43 score=95")
