"""Preserve the interrupted WSL environment state without resuming or deleting it."""
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"F:\OpenScience\audits\bio-single-cell-cell-annotation\reaudit-optimized-scientific-skills@2dee47f-20260925")
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
RUN = ROOT / "run"
ENV_NAME = "cellann-reaudit-2dee47f"
ENV_PATH = "/home/sci/micromamba/envs/cellann-reaudit-2dee47f"

export_cmd = ["wsl.exe", "-d", "science", "--", "bash", "-lc", f"micromamba env export -n {ENV_NAME}"]
export = subprocess.run(export_cmd, text=True, encoding="utf-8", errors="replace", capture_output=True)
(RUN / "input2_wsl_partial_environment.yaml").write_text(export.stdout, encoding="utf-8")

state_cmd = [
    "wsl.exe", "-d", "science", "--", "bash", "-lc",
    f"du -sb {ENV_PATH}; pgrep -af 'micromamba create.*{ENV_NAME}' || true; "
    f"micromamba list -n {ENV_NAME} | head -n 25",
]
state = subprocess.run(state_cmd, text=True, encoding="utf-8", errors="replace", capture_output=True)
log = "\n".join([
    f"RECORDED_UTC: {datetime.now(timezone.utc).isoformat()}",
    f"ENV_NAME: {ENV_NAME}",
    f"ENV_PATH: {ENV_PATH}",
    "INSTALL_RUNNER_EXIT: 1 (interrupted with Ctrl+C after observed size exceeded the 1 GB limit)",
    "WSL_SINGLER_EXECUTED: false",
    "EXPORT_COMMAND: " + subprocess.list2cmdline(export_cmd),
    f"EXPORT_EXIT_CODE: {export.returncode}",
    "EXPORT_STDERR:\n" + export.stderr,
    "STATE_COMMAND: " + subprocess.list2cmdline(state_cmd),
    f"STATE_EXIT_CODE: {state.returncode}",
    "STATE_STDOUT:\n" + state.stdout,
    "STATE_STDERR:\n" + state.stderr,
])
(RUN / "input2_wsl_install_interrupted.log").write_text(log, encoding="utf-8")
print(log)
if export.returncode != 0 or state.returncode != 0:
    raise SystemExit(1)
