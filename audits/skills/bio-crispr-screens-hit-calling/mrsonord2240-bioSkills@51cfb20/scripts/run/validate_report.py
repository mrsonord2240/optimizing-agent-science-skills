#!/usr/bin/env python
"""Validate the final-pass JSON contract and reported arithmetic."""
from __future__ import annotations
import json
from pathlib import Path

report_path = Path(__file__).resolve().parent.parent / "eval_report_bio-crispr-screens-hit-calling_result.json"
r = json.loads(report_path.read_text(encoding="utf-8"))
assert r["meta"]["auditor_independent"] is False
assert r["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert r["meta"]["source"] == "mrsonord2240/bioSkills@51cfb2078674ff6e8cb4412b9ae229f173a0b19d:crispr-screens/hit-calling"
assert set(r) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}
categories = r["static_score"]["categories"]
assert len(categories) == 8
assert sum(x["score"] for x in categories.values()) == r["static_score"]["subtotal"] == 92
inputs = r["dynamic_score"]["inputs"]
assert len(inputs) == r["meta"]["n_inputs"] == 11
for item in inputs:
    assert item["executed"] is True and item["execution_note"]
    assert 3 <= len(item["assertions"]) <= 5
    assert item["basic"] + item["specialized"] == item["total"]
    assert item["assertions_passed"] == sum(x["result"] == "PASS" for x in item["assertions"])
    assert item["assertions_total"] == len(item["assertions"])
assert sum(x["assertions_passed"] for x in inputs) == 51
assert sum(x["assertions_total"] for x in inputs) == 51
assert round(sum(x["total"] for x in inputs) / len(inputs), 1) == r["dynamic_score"]["execution_avg"] == 91.7
assert r["final"] == {"static_weighted": 36.8, "dynamic_weighted": 55.0, "score": 92, "max": 100, "grade": "Production Ready", "grade_symbol": "⭐", "deployable": True, "veto_override": False}
assert 2 <= len(r["key_strengths"]) <= 5
assert [x["priority"] for x in r["recommendations"]] == ["P2", "P2"]
print("REPORT_SCHEMA_AND_ARITHMETIC=PASS")
