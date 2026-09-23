"""Schema and arithmetic validation for the Phase 2 report."""
from __future__ import annotations

import json
from pathlib import Path

report = Path(__file__).resolve().parents[2] / "eval_report_bio-crispr-screens-combinatorial-screens_result.json"
data = json.loads(report.read_text(encoding="utf-8"))
assert data["meta"]["auditor_independent"] is False
assert data["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert data["meta"]["source"] == "mrsonord2240/bioSkills@72e75e17c8e64d89ddcf4af7587012a52cc5103a:crispr-screens/combinatorial-screens"
categories = data["static_score"]["categories"]
assert len(categories) == 8
assert sum(v["score"] for v in categories.values()) == data["static_score"]["subtotal"] == 92
inputs = data["dynamic_score"]["inputs"]
assert len(inputs) == data["meta"]["n_inputs"] == 9
for item in inputs:
    assert item["executed"] is True
    assert isinstance(item["execution_note"], str) and item["execution_note"]
    assert 3 <= len(item["assertions"]) <= 5
    assert item["basic"] + item["specialized"] == item["total"]
    assert item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"])
assert sum(i["assertions_passed"] for i in inputs) == 35
assert sum(i["assertions_total"] for i in inputs) == 36
assert round(sum(i["total"] for i in inputs) / len(inputs), 1) == data["dynamic_score"]["execution_avg"]
assert data["final"] == {"static_weighted": 36.8, "dynamic_weighted": 55.6, "score": 92, "max": 100, "grade": "Production Ready", "grade_symbol": "⭐", "deployable": True, "veto_override": False}
print("ASSERT PASS: report has required final-pass meta, valid arithmetic, 9 explicitly executed inputs with execution notes, and 35/36 assertions.")
