#!/usr/bin/env python3
"""Validate the final-pass report arithmetic and required Phase 2 metadata."""
import json
from pathlib import Path

report = Path(__file__).resolve().parent.parent / "eval_report_bio-reference-operations_result.json"
data = json.loads(report.read_text(encoding="utf-8"))
assert data["meta"]["source"] == "mrsonord2240/bioSkills@0f829d1619132fc9033b2437205d51ecb74df5d3:alignment-files/reference-operations"
assert data["meta"]["auditor_independent"] is False
assert data["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
inputs = data["dynamic_score"]["inputs"]
assert len(inputs) == data["meta"]["n_inputs"] == 10
assert all(item["executed"] is True and item["execution_note"] for item in inputs)
assert all(item["basic"] + item["specialized"] == item["total"] for item in inputs)
assert all(3 <= len(item["assertions"]) <= 5 for item in inputs)
passed = sum(a["result"] == "PASS" for item in inputs for a in item["assertions"])
total = sum(len(item["assertions"]) for item in inputs)
assert (passed, total) == (29, 30)
avg = round(sum(item["total"] for item in inputs) / len(inputs), 1)
assert avg == data["dynamic_score"]["execution_avg"] == 91.4
static = sum(x["score"] for x in data["static_score"]["categories"].values())
assert static == data["static_score"]["subtotal"] == 89
assert round(static * 0.4, 1) == data["final"]["static_weighted"] == 35.6
assert round(avg * 0.6, 1) == data["final"]["dynamic_weighted"] == 54.8
assert round(data["final"]["static_weighted"] + data["final"]["dynamic_weighted"]) == data["final"]["score"] == 90
assert data["final"]["deployable"] is True and data["final"]["veto_override"] is False
print("REPORT_VALID 10 inputs, 29/30 assertions, score 90")
