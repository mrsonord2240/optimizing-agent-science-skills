"""Fixer evidence: py_compile changed Python files without writing into the provider tree."""

from pathlib import Path
import py_compile

root = Path(r"F:\OpenScience\wt\backlog-statistical-annotation\skills\bio-data-visualization-statistical-annotation")
out = Path(r"F:\OpenScience\audits\bio-data-visualization-statistical-annotation\run\fixer-pyc")
out.mkdir(exist_ok=True)
files = [
    root / "scripts" / "annotate_pairwise.py",
    root / "scripts" / "annotate_paired.py",
    root / "tests" / "regression.py",
]
for file in files:
    py_compile.compile(str(file), cfile=str(out / f"{file.stem}.pyc"), doraise=True)
    print("PY_COMPILE PASS", file.name)

import matplotlib
import pandas
import scipy
import seaborn
import statannotations
import statsmodels

for module in (matplotlib, pandas, scipy, seaborn, statannotations, statsmodels):
    print(module.__name__, getattr(module, "__version__", "unknown"))
