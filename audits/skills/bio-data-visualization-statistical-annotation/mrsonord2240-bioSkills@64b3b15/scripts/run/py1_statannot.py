# SKILL.md statannotations block verbatim (pairs + Annotator) on SYNTHETIC data; assert texts vs scipy/manual
import warnings, itertools, numpy as np, pandas as pd, seaborn as sns, matplotlib
import matplotlib.pyplot as plt
from scipy import stats
from statannotations.Annotator import Annotator
import statannotations, scipy
print("statannotations", statannotations.__version__ if hasattr(statannotations, "__version__") else "?", "seaborn", sns.__version__, "scipy", scipy.__version__)
D = "F:/OpenScience/audits/bio-data-visualization-statistical-annotation"
def holm(p):
    p = np.array(p); n = len(p); o = np.argsort(p); r = np.minimum(1, np.maximum.accumulate((n - np.arange(n)) * p[o])); out = np.empty(n); out[o] = r; return out
def bh(p):
    p = np.array(p); n = len(p); o = np.argsort(p); r = np.minimum(1, np.minimum.accumulate((p[o] * n / np.arange(1, n + 1))[::-1])[::-1]); out = np.empty(n); out[o] = r; return out
def stars(p):
    return "ns" if p > 0.05 else "*" if p > 0.01 else "**" if p > 1e-3 else "***" if p > 1e-4 else "****"

def run(dset, pairs, corr, fmt, test="Mann-Whitney", tag="", order=None, extra=None):
    df = pd.read_csv(f"{D}/data/{dset}.csv")
    fig, ax = plt.subplots(figsize=(6, 5))
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        ax = sns.boxplot(x="group", y="value", data=df, ax=ax, order=order)
        an = Annotator(ax, pairs, data=df, x="group", y="value", order=order)
        kw = dict(test=test, comparisons_correction=corr, text_format=fmt, line_height=0.02, text_offset=0.5)
        if extra: kw.update(extra)
        an.configure(**kw)
        an.apply_and_annotate()
    texts = [t.get_text() for t in ax.texts]
    fig.savefig(f"{D}/figs/py_{dset}_{tag or corr}_{fmt}.png", dpi=100); plt.close(fig)
    raw_res = [a.data.pvalue for a in an.annotations] if hasattr(an.annotations[0], "data") else None
    print(f"[{dset} corr={corr} fmt={fmt} test={test}] texts={texts}  warnings={[str(x.message)[:90] for x in w]}")
    return an, texts, df

# --- SKILL.md block: 3 groups, Mann-Whitney + holm + star (both datasets)
pairs = [("Control","Treatment"),("Control","Vehicle"),("Treatment","Vehicle")]
an, t, df = run("three_group", pairs, "holm", "star", tag="skill")
groups = ["Control","Treatment","Vehicle"]
def truth(df, pairs, method="asymptotic"):
    return [stats.mannwhitneyu(df[df.group==a].value, df[df.group==b].value, alternative="two-sided", method=method).pvalue for a, b in pairs]
for method in ["asymptotic", "exact"]:
    raw = truth(df, pairs, method); print(" scipy", method, "raw", np.round(raw, 5), "holm", np.round(holm(raw), 5), "stars(holm)", [stars(x) for x in holm(raw)])
for a in an.annotations:
    print("  annotation", a.structs[0]["group"] if False else "", a.text if hasattr(a, "text") else "")

bp = ["G1","G2","G3"]; pairsB = [("G1","G2"),("G1","G3"),("G2","G3")]
an, t, dfb = run("border", pairsB, "holm", "star")
raw = truth(dfb, pairsB); print(" scipy raw", np.round(raw, 5), "holm", np.round(holm(raw), 5), [stars(x) for x in holm(raw)], "raw stars", [stars(x) for x in raw])
# bracket connectivity: look at annotation objects
for a in an.annotations:
    print("  ", [ (s["label"], s.get("group")) for s in a.structs] if hasattr(a, "structs") else vars(a).keys())
