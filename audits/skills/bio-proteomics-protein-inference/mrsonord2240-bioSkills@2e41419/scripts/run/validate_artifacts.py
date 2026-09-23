"""Validate Phase-2 audit artifact consistency without modifying the audited Skill."""
from __future__ import annotations

import json
from pathlib import Path

RUN = Path(__file__).resolve().parent
AUDIT = RUN.parent
report_path = AUDIT / "eval_report_bio-proteomics-protein-inference_result.json"
viewer_path = AUDIT / "eval_viewer_bio-proteomics-protein-inference.md"
report = json.loads(report_path.read_text(encoding="utf-8"))

meta = report["meta"]
assert meta["source"] == "mrsonord2240/bioSkills@2e41419be0f5d52378d18ce545c162a611006a93:proteomics/protein-inference"
assert meta["auditor_independent"] is False
assert meta["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == meta["n_inputs"] == 9
assert all(row["executed"] is True for row in inputs)
assert all(3 <= len(row["assertions"]) <= 5 for row in inputs)
assert all(row["basic"] + row["specialized"] == row["total"] for row in inputs)
assert sum(row["assertions_passed"] for row in inputs) == 36
assert sum(row["assertions_total"] for row in inputs) == 36
assert round(sum(row["total"] for row in inputs) / len(inputs), 1) == report["dynamic_score"]["execution_avg"]
assert sum(item["score"] for item in report["static_score"]["categories"].values()) == report["static_score"]["subtotal"] == 93
assert report["final"]["score"] == 95 and report["final"]["deployable"] is True
assert viewer_path.exists() and "Production Ready" in viewer_path.read_text(encoding="utf-8")
for filename in ("run_prior_python.log", "run_prior_percolator.log", "run_prior_philosopher_guard.log", "run_new_epifany_and_prefix.log", "run_new_example.log"):
    assert (RUN / "outputs" / filename).exists(), filename
print("artifact validation PASS: 9 executed inputs, 36/36 assertions, exact final-pass metadata, score 95")
