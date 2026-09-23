"""Validate the Phase 2 report's required audit contract and arithmetic."""
from __future__ import annotations

import json
from pathlib import Path

root = Path(r"F:\OpenScience\audits\bio-metabolomics-targeted-analysis")
report = json.loads((root / "eval_report_bio-metabolomics-targeted-analysis_result.json").read_text(encoding="utf-8"))

assert report["meta"]["source"] == "mrsonord2240/bioSkills@a23f43a7558a4ed755dea34196feaebc5affcfc1:metabolomics/targeted-analysis"
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert report["final"]["deployable"] is True and report["final"]["veto_override"] is False
assert report["veto_gates"]["skill_veto"]["gate"] == "PASS"
assert report["veto_gates"]["research_veto"]["gate"] == "PASS"

categories = report["static_score"]["categories"]
assert len(categories) == 8
assert sum(row["score"] for row in categories.values()) == report["static_score"]["subtotal"]

inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == report["meta"]["n_inputs"] == 7
passed = 0
total = 0
for entry in inputs:
    assert entry["executed"] is True
    assert entry["execution_note"].strip()
    assert entry["basic"] + entry["specialized"] == entry["total"]
    assert 3 <= len(entry["assertions"]) <= 5
    pass_count = sum(a["result"] == "PASS" for a in entry["assertions"])
    assert pass_count == entry["assertions_passed"]
    assert len(entry["assertions"]) == entry["assertions_total"]
    passed += pass_count
    total += len(entry["assertions"])
assert (passed, total) == (28, 28)
assert report["dynamic_score"]["assertion_pass_rate"] == {"passed": passed, "total": total}
avg = round(sum(entry["total"] for entry in inputs) / len(inputs), 1)
assert avg == report["dynamic_score"]["execution_avg"] == 94.0
assert report["final"]["static_weighted"] == round(report["static_score"]["subtotal"] * 0.4, 1)
assert report["final"]["dynamic_weighted"] == round(avg * 0.6, 1)
assert report["final"]["score"] == round(report["final"]["static_weighted"] + report["final"]["dynamic_weighted"])
assert all("priority" in recommendation for recommendation in report["recommendations"])
print("REPORT_SCHEMA_AND_ARITHMETIC_OK")
