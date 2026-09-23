import importlib.util
import subprocess
from pathlib import Path

source = Path(r"F:\OpenScience\wt\chemoinformatics-virtual-screening\chemoinformatics\virtual-screening\scripts\dock_single.py")
spec = importlib.util.spec_from_file_location("fresh_dock_single", source)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
out = Path(r"F:\OpenScience\audits\bio-virtual-screening\data\filter_mock.pdbqt")

class Result:
    returncode = 0
    stdout = ""
    stderr = ""

old_run = subprocess.run

def fake_run(cmd, capture_output, text):
    out.write_text("REMARK VINA RESULT: -7.0 0 0\nREMARK VINA RESULT: 68.0 0 0\n")
    return Result()

subprocess.run = fake_run
try:
    values = module.dock_single(
        "receptor.pdbqt", "ligand.pdbqt", (0, 0, 0), (1, 1, 1),
        out_pdbqt=str(out), vina_exe="intentionally-missing-vina",
    )
finally:
    subprocess.run = old_run

assert values == [[-7.0, 0.0, 0.0]], values
print("POSITIVE_ENERGY_FILTER=PASS")
