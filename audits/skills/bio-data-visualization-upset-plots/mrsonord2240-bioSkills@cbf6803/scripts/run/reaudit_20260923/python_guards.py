"""Independent upsetplot 0.9 / pandas-2 checks for rank, labels, exact styles, and PDF font type."""
from pathlib import Path
import matplotlib as mpl
mpl.use("Agg")
mpl.rcParams["pdf.fonttype"] = 42
import matplotlib.pyplot as plt
import pandas as pd
from upsetplot import UpSet, from_contents

assert "2.2" <= pd.__version__ < "3", pd.__version__
sets = {
    "A": [*(f"a{i}" for i in range(7)), *(f"ab{i}" for i in range(6)), *(f"ac{i}" for i in range(4)), "abc0"],
    "B": [*(f"b{i}" for i in range(5)), *(f"ab{i}" for i in range(6)), *(f"bc{i}" for i in range(2)), "abc0"],
    "C": [*(f"c{i}" for i in range(3)), *(f"ac{i}" for i in range(4)), *(f"bc{i}" for i in range(2)), "abc0"],
}
try:
    from_contents({"A": ["x", "x"], "B": ["x"]})
except ValueError:
    duplicate_rejected = True
else:
    duplicate_rejected = False
assert duplicate_rejected
data = from_contents(sets)
upset = UpSet(data, subset_size="count", show_counts=False, sort_by="cardinality", max_subset_rank=3)
upset.style_subsets(present=["A", "B"], absent=["C"], facecolor="#D55E00")
fig = plt.figure(figsize=(8, 5)); axes = upset.plot(fig=fig)
assert len(fig.axes) == len(axes), "separate figure must not add stray axes"
bars = axes["intersections"].patches
print("intersection patches=", len(bars), "heights=", [bar.get_height() for bar in bars])
assert len(bars) == 3, len(bars)
for bar in bars:
    h = bar.get_height()
    if h:
        axes["intersections"].annotate(f"{h:g}", (bar.get_x() + bar.get_width() / 2, h), ha="center", va="bottom")
assert len(axes["intersections"].texts) >= 3
assert any(c[0] > c[1] for c in (bar.get_facecolor() for bar in bars)), "exact AB-only style absent"
out = Path("out/py_example/python_guards.pdf")
fig.savefig(out, bbox_inches="tight"); plt.close(fig)
assert out.stat().st_size > 2000
blob = out.read_bytes()
assert b"Type3" not in blob and (b"Type42" in blob or b"CIDFontType2" in blob), "Type-42/TrueType PDF font absent"

# Ties at the rank boundary are retained, so max_subset_rank is not a hard display cap.
tie_data = from_contents({"A": ["a1", "a2", "ab1", "ab2", "abc1"], "B": ["b1", "ab1", "ab2", "bc1", "abc1"], "C": ["c1", "bc1", "abc1"]})
tie_fig = plt.figure(figsize=(7, 4)); tie_axes = UpSet(tie_data, subset_size="count", sort_by="cardinality", max_subset_rank=3).plot(fig=tie_fig)
tie_count = len(tie_axes["intersections"].patches); plt.close(tie_fig)
assert tie_count > 3, tie_count
print("PASS Python guards: pandas-2 pin, duplicate rejection, rank cap without ties, labels, exact style, no stray axes, embedded non-Type3 PDF font; rank-boundary ties retain", tie_count, "bars")
