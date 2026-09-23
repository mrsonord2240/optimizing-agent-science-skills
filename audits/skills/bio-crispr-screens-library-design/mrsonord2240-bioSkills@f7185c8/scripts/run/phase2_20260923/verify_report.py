"""Validate final-pass report arithmetic and required final-pass metadata.

Usage: python verify_report.py
"""
from __future__ import annotations

import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


REPORT = Path(__file__).resolve().parents[2] / "eval_report_bio-crispr-screens-library-design_result.json"
data = json.loads(REPORT.read_text(encoding="utf-8"))
inputs = data["dynamic_score"]["inputs"]

assert data["meta"]["source"] == "mrsonord2240/bioSkills@f7185c846de4c345fb2588fad1a43cebcd955b25:crispr-screens/library-design"
assert data["meta"]["auditor_independent"] is False
assert data["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert len(inputs) == data["meta"]["n_inputs"] == 10
assert all(item["executed"] is True and item["execution_note"] for item in inputs)
assert all(item["basic"] + item["specialized"] == item["total"] for item in inputs)
assert all(item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"]) for item in inputs)
assert all(item["assertions_total"] == len(item["assertions"]) for item in inputs)
assert sum(c["score"] for c in data["static_score"]["categories"].values()) == data["static_score"]["subtotal"]
avg = round(sum(item["total"] for item in inputs) / len(inputs), 1)
assert avg == data["dynamic_score"]["execution_avg"]
assert data["dynamic_score"]["assertion_pass_rate"] == {"passed": 39, "total": 40}
assert data["final"]["static_weighted"] == round(data["static_score"]["subtotal"] * 0.4, 1)
assert data["final"]["dynamic_weighted"] == round(data["dynamic_score"]["execution_avg"] * 0.6, 1)
nearest_integer = int(Decimal(str(data["final"]["static_weighted"] + data["final"]["dynamic_weighted"])).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
assert data["final"]["score"] == nearest_integer
assert data["final"] == {"static_weighted": 36.0, "dynamic_weighted": 54.5, "score": 91, "max": 100, "grade": "Production Ready", "grade_symbol": "⭐", "deployable": True, "veto_override": False}
print("report validation: PASS")
