"""Reproducible fix-pass checks for bio-machine-learning-model-validation.

Run from any directory with the audit Python environment:
  <python> fix_pass_validation.py <worktree>

This verifies each former P2 finding as a source-level requirement, compiles the
skill's executable example, and executes it in the installed sklearn API.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def require(text: str, needle: str, finding: str) -> None:
    if needle not in text:
        raise AssertionError(f"{finding}: missing {needle!r}")
    print(f"PASS {finding}")


def main(worktree: Path) -> None:
    skill_dir = worktree / "machine-learning" / "model-validation"
    skill = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    guide = (skill_dir / "usage-guide.md").read_text(encoding="utf-8")

    # Former P2: taxonomy ordering looked like a severity ordering.
    require(skill, "Indicative impact (not a ranking)", "P2 taxonomy distinguishes impact from ordering")
    require(skill, "Can manufacture near-perfect CV from pure noise", "P2 taxonomy identifies selection severity")
    require(skill, "A single global scaler may move little", "P2 taxonomy qualifies preprocessing magnitude")

    # Former P2: nested-versus-flat magnitude was unconditional.
    require(skill, "Its optimism is not a fixed size", "P2 nested-CV gap is conditional")
    require(skill, "number of configurations searched", "P2 nested-CV report fields")

    # Former P2: oversampling regime was unconditional in both entry points.
    require(skill, "under severe imbalance", "P2 SMOTE prevalence regime")
    require(skill, 'do not promise "no AUC gain"', "P2 SMOTE avoids unconditional AUC claim")
    require(skill, "original prevalence", "P2 SMOTE deployment-prevalence evaluation")
    require(guide, "especially under severe imbalance", "P2 guide matches SMOTE qualification")

    # Former P2: reporting request had no deliverable shape.
    require(skill, "Minimum validation-report skeleton", "P2 report skeleton exists")
    for field in ("calibration intercept, slope", "net benefit at pre-specified", "subgroup performance", "code/data version identifiers"):
        require(skill, field, f"P2 report skeleton includes {field}")
    require(guide, "auditable TRIPOD+AI-oriented report", "P2 guide exposes report deliverable")

    example = skill_dir / "examples" / "nested_cv_biomarker.py"
    subprocess.run([sys.executable, "-m", "py_compile", str(example)], check=True)
    print("PASS bundled example byte-compiles")
    completed = subprocess.run(
        [sys.executable, str(example)], check=True, text=True, capture_output=True, timeout=300
    )
    for headline in ("Nested-safe AUC:", "Leaky (selection-before-CV) AUC:", "Mean predicted risk", "Calibrated Brier:"):
        require(completed.stdout, headline, f"bundled example emits {headline}")
    print("PASS bundled example executes end-to-end")
    print(completed.stdout, end="")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} <worktree>")
    main(Path(sys.argv[1]).resolve())
