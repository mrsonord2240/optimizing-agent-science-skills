"""Re-audit 5 (volcano-and-ma-plots): scripts/ma_plot.py on the real shrunken airway table; rasterised vs vector size; sanbomics statements.
Usage: PYTHONPATH=<py-extra/sanbomics> py.sh r5_ma_python.py <skilldir> <csvdir> <outdir>"""
import importlib.util
import os
import sys
from pathlib import Path
skill, csvdir, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
out.mkdir(parents=True, exist_ok=True)
os.chdir(out)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
ok = True


def chk(label, cond):
    global ok
    ok &= bool(cond)
    print(f"[{'PASS' if cond else 'FAIL'}] {label}")


res = pd.read_csv(csvdir / "airway_shrunk_apeglm.csv")
print("rows", len(res), "non-NA padj", int(res.padj.notna().sum()), "padj<0.05", int((res.padj < .05).sum()))
spec = importlib.util.spec_from_file_location("ma_plot_mod", skill / "scripts" / "ma_plot.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
ax = mod.ma_plot(res)
fig = ax.figure
nsig = int(((res.padj < .05) & res.padj.notna()).sum())
cols = [c for c in ax.collections]
n_drawn = [len(c.get_offsets()) for c in cols]
print("points per collection", n_drawn)
chk("every row with baseMean>0 is drawn (grey + orange == rows)", sum(n_drawn) == int((res.baseMean > 0).sum()))
chk(f"orange (significant) count == padj<0.05 ({nsig})", n_drawn[1] == nsig)
fig.savefig("ma_py.pdf")
fig.savefig("ma_py.png", dpi=150)
# raster vs vector, on the 17,994 points with padj (the claim's subset) at the function's default figure size
sub = res[res.padj.notna()]


def size(ras):
    f, a = plt.subplots(figsize=(6, 5))
    sig = sub.padj < .05
    a.scatter(np.log10(sub.loc[~sig, 'baseMean']), sub.loc[~sig, 'log2FoldChange'], c='#999999', s=4, alpha=.4, rasterized=ras)
    a.scatter(np.log10(sub.loc[sig, 'baseMean']), sub.loc[sig, 'log2FoldChange'], c='#D55E00', s=6, alpha=.7, rasterized=ras)
    p = f"ma_{'ras' if ras else 'vec'}.pdf"
    f.savefig(p)
    plt.close(f)
    return os.path.getsize(p)


v, r = size(False), size(True)
print(f"MA scatter on {len(sub)} points: vector {v / 1e3:.0f} KB, rasterized {r / 1e3:.0f} KB  (claim 444 KB / 23 KB)")
print("(claim text says 17,994 points; 23/444 KB were measured on all 29,391 rows at 3.5x3 in; r5b below repeats that)")
# --- sanbomics statements
import sanbomics.plots as sp
chk("sanbomics.plots.volcano exists", hasattr(sp, "volcano"))
try:
    import sanbomics.tools as st
    print("sanbomics.tools.volcano:", hasattr(st, "volcano"))
except Exception as e:
    print("sanbomics.tools import:", type(e).__name__, str(e)[:80])
import inspect
sig_ = inspect.signature(sp.volcano)
print("signature:", sig_)
chk("pvalue='padj' is the default and a 'symbol' column is a parameter", sig_.parameters['pvalue'].default == 'padj' and 'symbol' in sig_.parameters)
d = res.dropna(subset=['padj']).rename(columns={'gene': 'symbol'})
plt.close('all')
sp.volcano(d, symbol='symbol')
fg = plt.gcf()
a2 = fg.axes[0]
import collections
cnt = collections.Counter(tuple(np.round(fc[:3], 3)) for c in a2.collections for fc in c.get_facecolors())
print("per-point facecolours (rgb: points):", dict(cnt), " collections:", [(len(c.get_offsets())) for c in a2.collections])
n_up = int(((d.padj < .05) & (d.log2FoldChange > .75)).sum()); n_dn = int(((d.padj < .05) & (d.log2FoldChange < -.75)).sum())
print("with sanbomics defaults (padj<0.05, |LFC|>0.75): Up", n_up, "Down", n_dn)
dim, blk = (0.412, 0.412, 0.412), (0.0, 0.0, 0.0)
nde = cnt.get(dim, 0) + cnt.get(blk, 0)
chk(f"sanbomics draws all {n_up + n_dn} DE points (Up {n_up} + Down {n_dn}) in one dark-grey class (+ black 'picked'), not Up/Down colours (SKILL.md)", nde == n_up + n_dn and len(cnt) == 3)
print("legend texts:", [t.get_text() for ax_ in fg.axes for t in (ax_.get_legend().get_texts() if ax_.get_legend() else [])])
fg.savefig("sanbomics_volcano.png", dpi=120)
print("RESULT", "PASS" if ok else "FAIL")

# repeat the MA size measurement the way ma_plot() really draws: all rows with baseMean>0, 3.5 x 3 in
def size_all(ras):
    f, a = plt.subplots(figsize=(3.5, 3))
    mod.ma_plot(res[res.baseMean > 0], 0.05, a)
    if not ras:
        for c in a.collections:
            c.set_rasterized(False)
    p = f"ma_all_{'ras' if ras else 'vec'}.pdf"
    f.savefig(p)
    plt.close(f)
    return os.path.getsize(p)


va, ra = size_all(False), size_all(True)
print(f"ma_plot() as shipped on all {int((res.baseMean > 0).sum())} rows, 3.5x3 in: vector {va / 1e3:.0f} KB, rasterized {ra / 1e3:.0f} KB")
print("points ma_plot() draws:", sum(n_drawn), "of which padj NA (drawn grey):", int(res.padj.isna().sum()))
