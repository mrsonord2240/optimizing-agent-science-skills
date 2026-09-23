import subprocess
from pathlib import Path

python = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\Scripts\python.exe"
source = r"F:\OpenScience\wt\chemoinformatics-virtual-screening\chemoinformatics\virtual-screening\scripts\dock_single.py"
data = Path(r"F:\OpenScience\audits\bio-virtual-screening\data\fresh1")
vina = r"F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\tools\vina\vina.exe"
base = [python, source, str(data / "receptor.pdbqt"), str(data / "lig.pdbqt"),
        "--center", "15.2", "53.3", "16.9", "--size", "20", "20", "20",
        "--seed", "42", "--vina-exe", vina]
a = subprocess.run(base + ["--out", str(data / "determinism_a.pdbqt")], capture_output=True, text=True, check=True)
b = subprocess.run(base + ["--out", str(data / "determinism_b.pdbqt")], capture_output=True, text=True, check=True)
assert a.stdout == b.stdout, (a.stdout, b.stdout)
print("DETERMINISM=PASS " + a.stdout.strip())
