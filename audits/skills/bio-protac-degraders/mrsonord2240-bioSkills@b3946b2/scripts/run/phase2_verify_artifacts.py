"""Validate final-pass report consistency without touching the source worktree."""

from __future__ import annotations

import json
from pathlib import Path


AUDIT = Path(__file__).resolve().parents[1]
REPORT = AUDIT / "eval_report_bio-protac-degraders_result.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    meta = report["meta"]
    require(meta["source"] == "mrsonord2240/bioSkills@b3946b260ddf8aebed7ad920e494fd43b06d147f:chemoinformatics/protac-degraders", "wrong source")
    require(meta["auditor_independent"] is False, "final-pass exception missing")
    require(meta["note"] == "final pass: fixed and audited under one brief, see CHECKPOINT.md", "wrong final-pass note")
    inputs = report["dynamic_score"]["inputs"]
    require(len(inputs) == meta["n_inputs"] == 11, "input count mismatch")
    require(all("executed" in row and "execution_note" in row for row in inputs), "execution fields missing")
    passed = sum(sum(item["result"] == "PASS" for item in row["assertions"]) for row in inputs)
    total = sum(len(row["assertions"]) for row in inputs)
    require((passed, total) == (44, 44), "assertion counts mismatch")
    average = round(sum(row["total"] for row in inputs) / len(inputs), 1)
    require(average == report["dynamic_score"]["execution_avg"] == 95.1, "dynamic average mismatch")
    require(sum(item["score"] for item in report["static_score"]["categories"].values()) == 94, "static sum mismatch")
    require(report["final"]["score"] == 95 and report["final"]["deployable"] is True, "final result mismatch")
    require((AUDIT / "eval_viewer_bio-protac-degraders.md").is_file(), "viewer missing")
    print("ARTIFACT PASS: 11 inputs; 44/44 assertions; static=94; dynamic=95.1; final=95")


if __name__ == "__main__":
    main()
