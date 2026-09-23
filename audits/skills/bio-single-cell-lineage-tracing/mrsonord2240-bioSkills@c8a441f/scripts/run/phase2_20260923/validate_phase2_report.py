"""Validate Phase 2 report arithmetic and explicit execution fields."""
import json
from pathlib import Path

report = Path(__file__).parents[2] / "eval_report_bio-single-cell-lineage-tracing_result.json"
payload = json.loads(report.read_text(encoding="utf-8"))
inputs = payload["dynamic_score"]["inputs"]
assert len(inputs) == payload["meta"]["n_inputs"] == 7
assert all(item["executed"] is True and item["execution_note"] for item in inputs)
assert all(item["basic"] + item["specialized"] == item["total"] for item in inputs)
assert sum(item["assertions_passed"] for item in inputs) == 26
assert sum(item["assertions_total"] for item in inputs) == 26
assert round(sum(item["total"] for item in inputs) / len(inputs), 1) == 89.7
assert sum(v["score"] for v in payload["static_score"]["categories"].values()) == 91
assert payload["final"]["score"] == 90 and payload["final"]["deployable"] is True
assert payload["meta"]["auditor_independent"] is False
assert payload["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
print("report validation PASS: 7 executed inputs, 26/26 assertions, score 90")
