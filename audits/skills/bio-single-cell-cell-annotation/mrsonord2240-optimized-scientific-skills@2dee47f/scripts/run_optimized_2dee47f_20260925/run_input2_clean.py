"""Execute and log the clean sparse-matrix SingleR route with exact process exits."""
import os
import subprocess
from pathlib import Path

ROOT = Path(r"F:\OpenScience\audits\bio-single-cell-cell-annotation\reaudit-optimized-scientific-skills@2dee47f-20260925")
RUN = ROOT / "run"
PYTHON = r"F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\Scripts\python.exe"
commands = [
    [PYTHON, str(RUN / "input2_clean_prepare.py")],
    [r"C:\Program Files\Git\bin\bash.exe", "F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/tools/rs.sh", str(RUN / "input2_clean.R").replace("\\", "/")],
]
chunks = []
last_exit = 0
for command in commands:
    result = subprocess.run(command, cwd=ROOT, text=True, encoding="utf-8", errors="replace", capture_output=True,
                            env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    chunks.extend(["COMMAND: " + subprocess.list2cmdline(command), f"EXIT_CODE: {result.returncode}",
                   "STDOUT:\n" + result.stdout, "STDERR:\n" + result.stderr])
    last_exit = result.returncode
    if result.returncode != 0:
        break
(RUN / "input2_clean.log").write_text("\n".join(chunks), encoding="utf-8")
print("\n".join(chunks))
raise SystemExit(last_exit)
