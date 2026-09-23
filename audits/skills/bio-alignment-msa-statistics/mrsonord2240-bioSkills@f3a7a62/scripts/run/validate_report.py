"""Validate the final-pass report's essential schema arithmetic and evidence markers."""
import json
from pathlib import Path

AUDIT = Path(__file__).resolve().parent.parent
report = json.loads((AUDIT / "eval_report_bio-alignment-msa-statistics_result.json").read_text(encoding="utf-8"))
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert report["meta"]["source"] == "mrsonord2240/bioSkills@f3a7a62091e42f6e98653b5b626de94c6f7bfff7:alignment/msa-statistics"
assert len(report["dynamic_score"]["inputs"]) == report["meta"]["n_inputs"] == 11
assert all(item["executed"] is True and item["execution_note"] and item["status"] == "COMPLETED" for item in report["dynamic_score"]["inputs"])
assert all(len(item["assertions"]) in range(3, 6) for item in report["dynamic_score"]["inputs"])
assert all(item["basic"] + item["specialized"] == item["total"] for item in report["dynamic_score"]["inputs"])
assert sum(item["assertions_passed"] for item in report["dynamic_score"]["inputs"]) == 54
assert sum(item["assertions_total"] for item in report["dynamic_score"]["inputs"]) == 54
assert report["static_score"]["subtotal"] == sum(category["score"] for category in report["static_score"]["categories"].values())
assert report["final"]["score"] == round(report["final"]["static_weighted"] + report["final"]["dynamic_weighted"])
assert report["final"]["deployable"] and not report["final"]["veto_override"]
print("report schema arithmetic PASS; 11 completed inputs; 54/54 assertions; score 97")
