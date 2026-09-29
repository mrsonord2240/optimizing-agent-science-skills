#!/usr/bin/env python3
"""Run and persist the candidate's shipped live regression suite."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import time


RUN_ROOT = Path("/mnt/openscience/audits/bio-cfdna-preprocessing/reaudit-opt10-20260928")
CANDIDATE = Path("/mnt/openscience/wt/opt10-cfdna/skills/bio-cfdna-preprocessing")
FIXTURE = Path("/mnt/openscience/audit-envs/bio-cfdna-preprocessing/data/synthetic-umi")


def main() -> int:
    command = [sys.executable, "-m", "unittest", "discover", "-s", str(CANDIDATE / "tests"), "-v"]
    env = {**os.environ, "CFDNA_FIXTURE_ROOT": str(FIXTURE), "PYTHONDONTWRITEBYTECODE": "1"}
    started = time.perf_counter()
    completed = subprocess.run(command, capture_output=True, text=True, env=env)
    elapsed = round(time.perf_counter() - started, 3)
    evidence = RUN_ROOT / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    (evidence / "shipped-suite.stdout.txt").write_text(completed.stdout, encoding="utf-8")
    (evidence / "shipped-suite.stderr.txt").write_text(completed.stderr, encoding="utf-8")
    summary = {
        "argv": command,
        "elapsed_seconds": elapsed,
        "returncode": completed.returncode,
        "fixture": str(FIXTURE),
        "stdout": "evidence/shipped-suite.stdout.txt",
        "stderr": "evidence/shipped-suite.stderr.txt",
        "candidate_tests": ["validation", "argv-only", "simplex", "duplex", "literal metacharacter paths", "QC flags/bounds/empty", "ten consecutive complete calls"],
    }
    (evidence / "shipped-suite-summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
