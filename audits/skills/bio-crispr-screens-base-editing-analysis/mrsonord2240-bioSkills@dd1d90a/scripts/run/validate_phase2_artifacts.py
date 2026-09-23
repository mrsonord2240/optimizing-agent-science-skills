"""Validate Phase 2 report arithmetic and required final-pass provenance."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

RUN = Path(__file__).resolve().parent
AUDIT = RUN.parent
report = json.loads((AUDIT / "eval_report_bio-crispr-screens-base-editing-analysis_result.json").read_text(encoding="utf-8"))
assert report["meta"]["auditor_independent"] is False
assert report["meta"]["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md"
assert report["meta"]["source"] == "mrsonord2240/bioSkills@dd1d90a9ae607f068d5ffda2e761e869f07decce:crispr-screens/base-editing-analysis"
inputs = report["dynamic_score"]["inputs"]
assert len(inputs) == report["meta"]["n_inputs"] == 7
assert all(item["executed"] is True for item in inputs)
assert all(3 <= len(item["assertions"]) <= 5 for item in inputs)
assert all(item["basic"] + item["specialized"] == item["total"] for item in inputs)
assert sum(item["assertions_passed"] for item in inputs) == 27
assert sum(item["assertions_total"] for item in inputs) == 28
avg = round(sum(item["total"] for item in inputs) / len(inputs), 1)
assert avg == report["dynamic_score"]["execution_avg"] == 93.7
static = sum(item["score"] for item in report["static_score"]["categories"].values())
assert static == report["static_score"]["subtotal"] == 89
assert report["final"]["static_weighted"] == round(static * 0.4, 1) == 35.6
assert report["final"]["dynamic_weighted"] == round(avg * 0.6, 1) == 56.2
assert report["final"]["score"] == round(35.6 + 56.2) == 92
assert report["final"]["grade"] == "Production Ready" and report["final"]["deployable"] is True
assert report["final"]["veto_override"] is False
assert (AUDIT / "eval_viewer_bio-crispr-screens-base-editing-analysis.md").exists()
assert (Path(r"F:\OpenScience\audits\_pre-fix-2026-09-22\bio-crispr-screens-base-editing-analysis") / "eval_report_bio-crispr-screens-base-editing-analysis_result.json").exists()
worktree = Path(r"F:\OpenScience\wt\crispr-screens-base-editing-analysis")
git = lambda *args: subprocess.check_output(["git", "-C", str(worktree), *args], text=True).strip()
assert git("rev-parse", "HEAD") == "dd1d90a9ae607f068d5ffda2e761e869f07decce"
assert git("branch", "--show-current") == "fix/crispr-screens-base-editing-analysis"
assert git("status", "--porcelain") == ""
print("PHASE2_REPORT_VALIDATION_PASS")
