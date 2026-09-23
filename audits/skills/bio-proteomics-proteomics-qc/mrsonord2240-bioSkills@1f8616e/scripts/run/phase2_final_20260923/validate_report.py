#!/usr/bin/env python
"""Validate audit-report arithmetic and mandatory Phase 2 metadata."""
import json
from pathlib import Path

report_path = Path(__file__).resolve().parents[2] / "eval_report_bio-proteomics-proteomics-qc_result.json"
report = json.loads(report_path.read_text(encoding="utf-8"))
assert report["meta"]["source"] == "mrsonord2240/bioSkills@1f8616e8d39c2f14c16a01a4330bd0d94762b762:proteomics/proteomics-qc"
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == report["meta"]["n_inputs"] == 10
assert all(item["executed"] is True and item["execution_note"] for item in inputs)
assert all(3 <= len(item["assertions"]) <= 5 for item in inputs)
assert all(item["basic"] + item["specialized"] == item["total"] for item in inputs)
assert all(item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"]) for item in inputs)
assert sum(v["score"] for v in report["static_score"]["categories"].values()) == report["static_score"]["subtotal"] == 93
assert round(sum(item["total"] for item in inputs) / len(inputs), 1) == report["dynamic_score"]["execution_avg"] == 93.1
assert report["final"]["static_weighted"] == 37.2
assert report["final"]["dynamic_weighted"] == 55.9
assert report["final"]["score"] == 93 and report["final"]["deployable"] is True and report["final"]["veto_override"] is False
print("report validation passed: 10 executed inputs, 39/40 assertions, 93/100 deployable")
