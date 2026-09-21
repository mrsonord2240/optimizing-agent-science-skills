# Input 2: every Python block of SKILL.md (ptitprince RainCloud, seaborn boxenplot) + the seaborn functions named in the header, on the SAME synthetic data as input 1.
import warnings, io, sys, traceback
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns, ptitprince as pt
print("seaborn", sns.__version__, "matplotlib", matplotlib.__version__, "ptitprince", getattr(pt, "__version__", "?"), "pandas", pd.__version__)
df = pd.read_csv(r"F:\OpenScience\audits\bio-data-visualization-distribution-plots\run\data\i1_synthetic_2group.csv")
df["group"] = pd.Categorical(df["group"], ["Control", "Treated"])
med = df.groupby("group", observed=True)["value"].median()
n = df.groupby("group", observed=True)["value"].size()
print("truth: n", dict(n), "median", {k: round(v, 3) for k, v in med.items()})
res = []
def rec(name, ok, note=""):
    res.append((name, ok)); print(("[PASS] " if ok else "[FAIL] ") + name, note)
OUT = r"F:\OpenScience\audits\bio-data-visualization-distribution-plots\run\out"

def run(name, fn):
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        try:
            fig = fn(); fig.savefig(OUT + "\\" + name + ".png", dpi=110, bbox_inches="tight"); plt.close(fig)
            print(f"-- {name}: ran; warnings: {sorted(set(str(x.category.__name__)+': '+str(x.message)[:110] for x in w))}")
            return True
        except Exception as e:
            print(f"-- {name}: ERROR {type(e).__name__}: {str(e)[:300]}"); plt.close("all"); return False

# ---- SKILL block, verbatim: ptitprince RainCloud with x='group', y='value', orient='h'
def raincloud_verbatim():
    fig, ax = plt.subplots(figsize=(5, 3.5))
    pt.RainCloud(x='group', y='value', data=df,
                 palette=['#0072B2', '#D55E00'],
                 bw='scott', cut=0,                          # bandwidth + trim
                 width_viol=0.6, orient='h', ax=ax)
    return fig
ok_verbatim = run("i2_raincloud_verbatim", raincloud_verbatim)

# ---- what a correct horizontal call looks like: x=value, y=group
def raincloud_swapped():
    fig, ax = plt.subplots(figsize=(5, 3.5))
    pt.RainCloud(x='group', y='value', data=df, palette=['#0072B2', '#D55E00'], bw='scott', cut=0, width_viol=0.6, orient='h', ax=ax)
    return fig
def raincloud_correct_h():
    fig, ax = plt.subplots(figsize=(5, 3.5))
    pt.RainCloud(x='value', y='group', data=df, palette=['#0072B2', '#D55E00'], bw='scott', cut=0, width_viol=0.6, orient='h', ax=ax)
    return fig
run("i2_raincloud_xvalue_ygroup", raincloud_correct_h)
def raincloud_vertical():
    fig, ax = plt.subplots(figsize=(4, 4))
    pt.RainCloud(x='group', y='value', data=df, palette=['#0072B2', '#D55E00'], bw='scott', cut=0, width_viol=0.6, orient='v', ax=ax)
    return fig
run("i2_raincloud_vertical", raincloud_vertical)

# ---- SKILL block verbatim: boxenplot with palette (no hue)
def boxen():
    fig, ax = plt.subplots(figsize=(4, 3.5))
    sns.boxenplot(x='group', y='value', data=df, palette=['#0072B2', '#D55E00'], ax=ax)
    return fig
run("i2_boxen", boxen)

# ---- header functions: box / violin / swarm / strip
def std_panel():
    fig, axs = plt.subplots(1, 4, figsize=(14, 3.5))
    sns.boxplot(x='group', y='value', hue='group', data=df, palette=['#0072B2', '#D55E00'], ax=axs[0], legend=False)
    sns.violinplot(x='group', y='value', hue='group', data=df, palette=['#0072B2', '#D55E00'], bw_method='scott', cut=0, ax=axs[1], legend=False)
    sns.swarmplot(x='group', y='value', data=df, hue='group', palette=['#0072B2', '#D55E00'], ax=axs[2], legend=False)
    sns.stripplot(x='group', y='value', data=df, hue='group', palette=['#0072B2', '#D55E00'], ax=axs[3], legend=False)
    for a, t in zip(axs, ["box", "violin", "swarm", "strip"]): a.set_title(t)
    return fig
run("i2_standard4", std_panel)

# ---- assertions on drawn content of the RainCloud (build once more, inspect artists)
def inspect(orient, x, y):
    fig, ax = plt.subplots(figsize=(5, 3.5))
    pt.RainCloud(x=x, y=y, data=df, palette=['#0072B2', '#D55E00'], bw='scott', cut=0, width_viol=0.6, orient=orient, ax=ax)
    fig.canvas.draw()
    return fig, ax
for label, (o, x, y) in {"verbatim x=group,y=value,orient=h": ("h", "group", "value"), "x=value,y=group,orient=h": ("h", "value", "group"), "x=group,y=value,orient=v": ("v", "group", "value")}.items():
    try:
        fig, ax = inspect(o, x, y)
        ptsn = [len(c.get_offsets()) for c in ax.collections if hasattr(c, "get_offsets") and len(c.get_offsets()) > 0]
        # median lines: boxplot median Line2D have 2 pts
        lines = [l for l in ax.lines if len(l.get_xdata()) == 2 and len(l.get_ydata()) == 2]
        meds_x = sorted({round(float(l.get_xdata()[0]), 3) for l in lines if l.get_xdata()[0] == l.get_xdata()[1] and o == "h"})
        meds_y = sorted({round(float(l.get_ydata()[0]), 3) for l in lines if l.get_ydata()[0] == l.get_ydata()[1] and o == "v"})
        print(f"   [{label}] scatter collections sizes {ptsn}; xlabel={ax.get_xlabel()!r} ylabel={ax.get_ylabel()!r}; xticks={[t.get_text() for t in ax.get_xticklabels()][:4]} yticks={[t.get_text() for t in ax.get_yticklabels()][:4]}; box-median candidates x={meds_x[:6]} y={meds_y[:6]}")
        plt.close(fig)
    except Exception as e:
        print(f"   [{label}] inspect ERROR {type(e).__name__}: {str(e)[:200]}"); plt.close("all")
print("SUMMARY", sum(o for _, o in res), "/", len(res), "explicit asserts")
