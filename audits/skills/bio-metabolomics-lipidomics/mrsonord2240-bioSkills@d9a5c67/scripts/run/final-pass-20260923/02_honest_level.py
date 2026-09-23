import os
import runpy
import sys

sys.dont_write_bytecode = True
source = r"F:\OpenScience\wt\metabolomics-lipidomics\metabolomics\lipidomics\scripts\honest_level.py"
honest_names = runpy.run_path(source)["honest_names"]

cases = {
    "PC 16:0/18:1": "PC 16:0_18:1",
    "PC 34:1": "PC 34:1",
    "TG 52:3": "TG 52:3",
    "PC O-34:1": "PC O-34:1",
    "PC P-34:1": "PC P-34:1",
}
for name, expected in cases.items():
    level, honest, summed = honest_names(name)
    print(f"{name}\tclaimed={level.name}\thonest={honest}\tsum={summed}")
    assert honest == expected, (name, honest, expected)
print(f"PASS honest-level cases={len(cases)}")
