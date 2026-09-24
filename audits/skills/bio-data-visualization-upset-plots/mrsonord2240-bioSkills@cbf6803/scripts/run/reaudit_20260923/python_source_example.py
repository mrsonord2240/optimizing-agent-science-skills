"""Run the exact committed pandas-2/upsetplot example and assert its outputs."""
from pathlib import Path
import os
import runpy

src = Path(r"F:/OpenScience/wt/data-visualization-upset-plots/data-visualization/upset-plots/examples/upset_python.py")
out = Path(r"F:/OpenScience/audits/bio-data-visualization-upset-plots/run/reaudit_20260923/out/py_example")
assert src.exists() and out.exists()
os.chdir(out)
runpy.run_path(str(src), run_name="__main__")
required = [
    "upset_basic.png", "upset_basic.pdf", "upset_customized.png", "upset_customized.pdf",
    "upset_with_boxplot.png", "upset_with_boxplot.pdf",
]
for name in required:
    assert (out / name).stat().st_size > 2000, name
assert not list(out.glob("Rplots.pdf"))
print("PASS exact Python example: six nonempty named outputs, no stray R artifact")
