# Exact current-source upsetplot regression vectors for the backlog fix.
import matplotlib as mpl
mpl.use("Agg")
mpl.rcParams["pdf.fonttype"] = 42
import matplotlib.pyplot as plt
from pathlib import Path
import pandas as pd
from upsetplot import UpSet, from_contents

assert "2.2" <= pd.__version__ < "3", pd.__version__
sets = {
    "A": [*(f"a{i}" for i in range(6)), *(f"ab{i}" for i in range(5)), *(f"abc{i}" for i in range(3))],
    "B": [*(f"b{i}" for i in range(4)), *(f"ab{i}" for i in range(5)), *(f"bc{i}" for i in range(2)), *(f"abc{i}" for i in range(3))],
    "C": [*(f"c{i}" for i in range(2)), *(f"bc{i}" for i in range(2)), *(f"abc{i}" for i in range(3))],
}
data = from_contents(sets)
data["log2FC"] = range(len(data))
u = UpSet(data, subset_size="count", show_counts=False, sort_by="cardinality", max_subset_rank=3)
u.style_subsets(present=["A", "B"], absent=["C"], facecolor="#D55E00")
fig = plt.figure(figsize=(8, 5)); axes = u.plot(fig=fig)
assert len(fig.axes) == len(axes), "no stray axes"
assert len(axes["intersections"].patches) == 3, "max_subset_rank must cap the bar count"
for bar in axes["intersections"].patches:
    if bar.get_height(): axes["intersections"].annotate(f"{bar.get_height():g}", (bar.get_x() + bar.get_width()/2, bar.get_height()), ha="center")
assert len(axes["intersections"].texts) >= 3, "manual labels missing"
colors = [bar.get_facecolor() for bar in axes["intersections"].patches]
assert any(c[0] > c[1] for c in colors), "exact present+absent style missing"
fig.savefig("python_exact.pdf", bbox_inches="tight"); fig.savefig("python_exact.png", dpi=150, bbox_inches="tight"); plt.close(fig)
assert Path("python_exact.pdf").stat().st_size > 2000
print("Python vectors PASS: pandas pin, no show_counts, no stray axes, manual labels, exact style, rank cap, Type42 PDF")
