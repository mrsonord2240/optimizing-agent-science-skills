"""Validate the final-pass report's mandatory audit-contract fields and arithmetic."""
from __future__ import annotations

import json
from pathlib import Path

root = Path(r"F:\OpenScience\audits\bio-causal-genomics-proteome-mr-drug-target")
report = root / "eval_report_bio-causal-genomics-proteome-mr-drug-target_result.json"
payload = json.loads(report.read_text(encoding="utf-8"))
meta = payload["meta"]
assert meta["source"] == "mrsonord2240/bioSkills@b1df50d420e9a6bb2cd43f46adf2a0d94ff37288:causal-genomics/proteome-mr-drug-target"
assert meta["auditor_independent"] is False
assert meta["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
inputs = payload["dynamic_score"]["inputs"]
assert len(inputs) == meta["n_inputs"] == 11
assert all(row["executed"] is True and row["execution_note"] for row in inputs)
assert all(row["basic"] + row["specialized"] == row["total"] for row in inputs)
assert sum(row["assertions_passed"] for row in inputs) == 48
assert sum(row["assertions_total"] for row in inputs) == 49
assert round(sum(row["total"] for row in inputs) / len(inputs), 1) == 93.9
assert sum(item["score"] for item in payload["static_score"]["categories"].values()) == 92
final = payload["final"]
assert final == {"static_weighted": 36.8, "dynamic_weighted": 56.3, "score": 93, "max": 100,
                 "grade": "Production Ready", "grade_symbol": "⭐", "deployable": True, "veto_override": False}
assert payload["veto_gates"]["skill_veto"]["gate"] == "PASS"
assert payload["veto_gates"]["research_veto"]["gate"] == "PASS"
print("PASS: report schema fields, execution coverage, source ref, metadata, and arithmetic validated.")
