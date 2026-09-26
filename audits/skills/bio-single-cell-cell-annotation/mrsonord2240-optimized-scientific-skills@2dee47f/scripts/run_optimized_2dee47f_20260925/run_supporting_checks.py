"""Run the two focused supporting checks and retain stdout/stderr with exact exits."""
import os
import subprocess
from pathlib import Path

ROOT = Path(r"F:\OpenScience\audits\bio-single-cell-cell-annotation\reaudit-optimized-scientific-skills@2dee47f-20260925")
RUN = ROOT / "run"
PYTHON = r"F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\Scripts\python.exe"
for stem in ("verify_seed_repeat", "validate_required_inputs"):
    command = [PYTHON, str(RUN / f"{stem}.py")]
    result = subprocess.run(command, cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True,
                            env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    log = "\n".join(["COMMAND: " + subprocess.list2cmdline(command), f"EXIT_CODE: {result.returncode}",
                      "STDOUT:\n" + result.stdout, "STDERR:\n" + result.stderr])
    (RUN / f"{stem}.log").write_text(log, encoding="utf-8")
    print(f"{stem}: exit={result.returncode}")
    if result.returncode != 0:
        raise SystemExit(result.returncode)
