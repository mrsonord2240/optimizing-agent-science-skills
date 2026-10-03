"""Minimal probe: does a stock matplotlib 3.11.2 PDF save with default pdf.fonttype=3 work? Isolates the Type 3 failure seen in m3_recipes.py."""
import sys, tempfile, matplotlib as mpl, matplotlib.pyplot as plt, numpy as np
print(mpl.__version__, "default pdf.fonttype", mpl.rcParams['pdf.fonttype'])
def tryit(label, fn):
    try:
        fn(); print("ok  ", label)
    except Exception as e:
        print("FAIL", label, "->", type(e).__name__, e)
d = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp()
import os; os.makedirs(d, exist_ok=True)
fig, ax = plt.subplots(); ax.plot([-1, 0, 1], [-1, 0, 1])
tryit("default Type 3, negative ticks (U+2212)", lambda: fig.savefig(d + "/a.pdf"))
mpl.rcParams['axes.unicode_minus'] = False
fig, ax = plt.subplots(); ax.plot([-1, 0, 1], [-1, 0, 1])
tryit("default Type 3, ascii minus", lambda: fig.savefig(d + "/b.pdf"))
mpl.rcParams['axes.unicode_minus'] = True
fig, ax = plt.subplots(); ax.plot([1, 2, 3], [1, 2, 3])
tryit("default Type 3, positive ticks only", lambda: fig.savefig(d + "/c.pdf"))
mpl.rcParams['pdf.fonttype'] = 42
fig, ax = plt.subplots(); ax.plot([-1, 0, 1], [-1, 0, 1])
tryit("Type 42, negative ticks", lambda: fig.savefig(d + "/d.pdf"))
