#!/usr/bin/env python3
"""Run ten consecutive advertised wrapper calls for the structural stability gate."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

RUN = Path(__file__).resolve().parent
EVIDENCE = RUN / "evidence"
WORK = RUN / "work" / "stability"
TOOLING = Path("/mnt/openscience/audit-envs/bio-cfdna-preprocessing")
PYTHON = TOOLING / "conda-env" / "bin" / "python"
SCRIPT = Path("/mnt/openscience/wt/opt10-cfdna/skills/bio-cfdna-preprocessing/scripts/preprocess_cfdna.py")
RAW = TOOLING / "data" / "synthetic-umi" / "raw.unmapped.bam"
REFERENCE = TOOLING / "data" / "synthetic-umi" / "reference.fa"
ENV = os.environ.copy()
ENV["PATH"] = str(TOOLING / "conda-env" / "bin") + os.pathsep + ENV.get("PATH", "")
ENV["PYTHONDONTWRITEBYTECODE"] = "1"


def main() -> None:
    WORK.mkdir(parents=True, exist_ok=False)
    calls = []
    for index in range(1, 11):
        duplex = index % 2 == 0
        output = WORK / f"call-{index:02d}" / "final.bam"
        output.parent.mkdir()
        argv = [
            str(PYTHON), str(TOOLING / "call_candidate.py"),
            "--script", str(SCRIPT), "--input", str(RAW),
            "--output", str(output), "--reference", str(REFERENCE),
            "--threads", "2",
        ]
        if duplex:
            argv.append("--duplex")
        completed = subprocess.run(argv, env=ENV, text=True, capture_output=True, check=False, timeout=60)
        stdout = EVIDENCE / f"stability-{index:02d}.stdout.txt"
        stderr = EVIDENCE / f"stability-{index:02d}.stderr.txt"
        stdout.write_text(completed.stdout, encoding="utf-8")
        stderr.write_text(completed.stderr, encoding="utf-8")
        calls.append({
            "index": index,
            "duplex": duplex,
            "returncode": completed.returncode,
            "output_exists": output.exists(),
            "stdout": stdout.name,
            "stderr": stderr.name,
        })
    failures = sum(call["returncode"] != 0 or not call["output_exists"] for call in calls)
    summary = {
        "calls": calls,
        "successes": len(calls) - failures,
        "failures": failures,
        "failure_rate": failures / len(calls),
    }
    path = EVIDENCE / "stability-summary.json"
    path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
