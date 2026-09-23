"""Validate core reporting-contract invariants for this corrective re-audit.

Usage: python validate_corrective_report.py <report-json>
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

report = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
assert set(report) == {"meta", "veto_gates", "static_score", "dynamic_score", "final", "key_strengths", "recommendations"}
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert report["meta"]["source"].startswith("mrsonord2240/bioSkills@6b48002e06f0dfd1ae3bb1e19a75ff9522da6ebe:")
categories = report["static_score"]["categories"]
assert len(categories) == 8
assert sum(item["score"] for item in categories.values()) == report["static_score"]["subtotal"]
inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == report["meta"]["n_inputs"] == 7
for item in inputs:
    assert item["executed"] is True and item["execution_note"]
    assert 3 <= len(item["assertions"]) <= 5
    assert item["assertions_passed"] == sum(a["result"] == "PASS" for a in item["assertions"])
    assert item["assertions_total"] == len(item["assertions"])
    assert item["basic"] + item["specialized"] == item["total"]
assert report["dynamic_score"]["assertion_pass_rate"] == {"passed": 28, "total": 28}
assert 2 <= len(report["key_strengths"]) <= 5
assert report["final"] == {"static_weighted": 36.4, "dynamic_weighted": 56.0, "score": 92.4, "max": 100, "grade": "Production Ready", "grade_symbol": "⭐", "deployable": True, "veto_override": False}
assert [r["priority"] for r in report["recommendations"]] == ["P2"]
print("REPORT_CONTRACT_PASS")
