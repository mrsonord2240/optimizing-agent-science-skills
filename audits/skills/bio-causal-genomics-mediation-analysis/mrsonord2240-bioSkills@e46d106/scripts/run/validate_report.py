"""Validate the Phase 2 report's schema-critical arithmetic and required execution evidence."""
import json
from pathlib import Path

path = Path(r"F:\OpenScience\audits\bio-causal-genomics-mediation-analysis\eval_report_bio-causal-genomics-mediation-analysis_result.json")
report = json.loads(path.read_text(encoding="utf-8"))
assert set(report) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}
assert report["meta"]["n_inputs"] == len(report["dynamic_score"]["inputs"]) == 14
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
categories = report["static_score"]["categories"]
assert len(categories) == 8
assert report["static_score"]["subtotal"] == sum(v["score"] for v in categories.values())
inputs = report["dynamic_score"]["inputs"]
assert all(item["executed"] is True and item["execution_note"] for item in inputs)
assert all(3 <= len(item["assertions"]) <= 5 for item in inputs)
assert all(item["basic"] + item["specialized"] == item["total"] for item in inputs)
assert all(item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"]) for item in inputs)
assert report["dynamic_score"]["assertion_pass_rate"] == {"passed": 42, "total": 42}
assert round(sum(item["total"] for item in inputs) / len(inputs), 1) == report["dynamic_score"]["execution_avg"]
assert report["final"]["static_weighted"] == round(report["static_score"]["subtotal"] * 0.4, 1)
assert report["final"]["dynamic_weighted"] == round(report["dynamic_score"]["execution_avg"] * 0.6, 1)
assert report["final"]["score"] == round(report["final"]["static_weighted"] + report["final"]["dynamic_weighted"])
assert report["final"]["deployable"] is True and report["final"]["veto_override"] is False
print("REPORT VALID: 14 executed inputs, 42/42 assertions, scores and final-pass metadata consistent")
