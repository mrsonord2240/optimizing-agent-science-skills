"""Install an isolated WSL R env, execute SingleR there, and preserve exact logs/exits."""
import subprocess
from pathlib import Path

ROOT = Path(r"F:\OpenScience\audits\bio-single-cell-cell-annotation\reaudit-optimized-scientific-skills@2dee47f-20260925")
RUN = ROOT / "run"
base = "/mnt/openscience/audits/bio-single-cell-cell-annotation/reaudit-optimized-scientific-skills@2dee47f-20260925/run"
commands = [
    ("input2_wsl_install.log", ["wsl.exe", "-d", "science", "--", "bash", "-lc", f"{base}/install_input2_wsl.sh"]),
    ("input2_wsl.log", ["wsl.exe", "-d", "science", "--", "bash", "-lc", f"micromamba run -n cellann-reaudit-2dee47f Rscript {base}/input2_wsl.R"]),
]
for log_name, command in commands:
    result = subprocess.run(command, text=True, encoding="utf-8", errors="replace", capture_output=True)
    log = "\n".join(["COMMAND: " + subprocess.list2cmdline(command), f"EXIT_CODE: {result.returncode}",
                      "STDOUT:\n" + result.stdout, "STDERR:\n" + result.stderr])
    (RUN / log_name).write_text(log, encoding="utf-8")
    print(f"{log_name}: exit={result.returncode}")
    if result.returncode != 0:
        raise SystemExit(result.returncode)
