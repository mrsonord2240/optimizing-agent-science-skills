"""Run the saved WSL capability probe and persist its exact exit and output."""
import subprocess
from pathlib import Path

ROOT = Path(r"F:\OpenScience\audits\bio-single-cell-cell-annotation\reaudit-optimized-scientific-skills@2dee47f-20260925")
script = "/mnt/openscience/audits/bio-single-cell-cell-annotation/reaudit-optimized-scientific-skills@2dee47f-20260925/run/input2_wsl_probe.sh"
command = ["wsl.exe", "-d", "science", "--", "bash", "-lc", script]
result = subprocess.run(command, text=True, encoding="utf-8", errors="replace", capture_output=True)
log = "\n".join([
    "COMMAND: " + subprocess.list2cmdline(command),
    f"EXIT_CODE: {result.returncode}",
    "STDOUT:\n" + result.stdout,
    "STDERR:\n" + result.stderr,
])
(ROOT / "run" / "input2_wsl_probe.log").write_text(log, encoding="utf-8")
print(log)
raise SystemExit(result.returncode)
