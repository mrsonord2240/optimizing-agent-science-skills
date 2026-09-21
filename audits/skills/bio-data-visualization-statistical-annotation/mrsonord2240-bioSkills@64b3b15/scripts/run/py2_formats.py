# statannotations: test names x correction x text_format, compared with independent scipy + manual adjustment. SYNTHETIC data.
import warnings, itertools, numpy as np, pandas as pd, seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from statannotations.Annotator import Annotator
warnings.filterwarnings("ignore")
D = "F:/OpenScience/audits/bio-data-visualization-statistical-annotation"
def holm(p):
    p = np.array(p); n = len(p); o = np.argsort(p); r = np.minimum(1, np.maximum.accumulate((n - np.arange(n)) * p[o])); out = np.empty(n); out[o] = r; return out
def bh(p):
    p = np.array(p); n = len(p); o = np.argsort(p); r = np.minimum(1, np.minimum.accumulate((p[o] * n / np.arange(1, n + 1))[::-1])[::-1]); out = np.empty(n); out[o] = r; return out
def stars(p): return "ns" if p > 0.05 else "*" if p > 0.01 else "**" if p > 1e-3 else "***" if p > 1e-4 else "****"
def annotate(df, pairs, order, **cfg):
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.boxplot(x="group", y="value", data=df, order=order, ax=ax)
    an = Annotator(ax, pairs, data=df, x="group", y="value", order=order)
    an.configure(**cfg); an.apply_and_annotate()
    txt = [t.get_text() for t in ax.texts]
    return fig, ax, an, txt

df = pd.read_csv(f"{D}/data/border.csv"); order = ["G1", "G2", "G3"]
pairs = [("G1","G2"),("G1","G3"),("G2","G3")]
raw = [stats.mannwhitneyu(df[df.group==a].value, df[df.group==b].value, alternative="two-sided").pvalue for a, b in pairs]
print("truth raw", np.round(raw, 5), "holm", np.round(holm(raw), 5), "bonf", np.round(np.minimum(1, np.array(raw)*3), 5), "BH", np.round(bh(raw), 5))
print("truth stars raw", [stars(x) for x in raw], "holm", [stars(x) for x in holm(raw)], "bonf", [stars(min(1, x*3)) for x in raw], "BH", [stars(x) for x in bh(raw)])
for corr in [None, "holm", "bonferroni", "BH"]:
    for fmt in ["star", "simple", "full"]:
        fig, ax, an, txt = annotate(df, pairs, order, test="Mann-Whitney", comparisons_correction=corr, text_format=fmt)
        pv = [(round(a.data.pvalue, 5), a.data.stat_value if False else None) for a in an.annotations]
        print(f"corr={corr} fmt={fmt}: texts={txt} | Annotation.data.pvalue={[p[0] for p in pv]}")
        plt.close(fig)

# test names
print("\n--- t-test_ind vs Welch vs scipy")
a = df[df.group=="G1"].value; b = df[df.group=="G2"].value
for name in ["t-test_ind", "t-test_welch", "Mann-Whitney"]:
    fig, ax, an, txt = annotate(df, [("G1","G2")], order, test=name, text_format="full", comparisons_correction=None)
    print(name, txt, "| scipy student", stats.ttest_ind(a, b).pvalue, "welch", stats.ttest_ind(a, b, equal_var=False).pvalue, "mwu", stats.mannwhitneyu(a, b).pvalue); plt.close(fig)

# one-sided
fig, ax, an, txt = annotate(df, [("G1","G2")], order, test="Mann-Whitney", text_format="full", comparisons_correction=None, test_short_name=None)
plt.close(fig)

# paired
pdf = pd.read_csv(f"{D}/data/paired.csv"); po = ["Pre", "Post"]
pre = pdf[pdf.time=="Pre"].value.values; post = pdf[pdf.time=="Post"].value.values
print("\n--- paired truth: wilcoxon", stats.wilcoxon(pre, post).pvalue, "ttest_rel", stats.ttest_rel(pre, post).pvalue, "unpaired mwu", stats.mannwhitneyu(pre, post).pvalue)
for name in ["Wilcoxon", "t-test_paired", "Mann-Whitney", "t-test_ind"]:
    fig, ax, an, txt = annotate(pdf.rename(columns={"time": "group"}), [("Pre","Post")], po, test=name, text_format="full", comparisons_correction=None)
    print(name, txt); plt.close(fig)
# paired with rows sorted differently (shuffled) -> pairing lost silently?
sh = pdf.sample(frac=1, random_state=1).rename(columns={"time": "group"})
fig, ax, an, txt = annotate(sh, [("Pre","Post")], po, test="Wilcoxon", text_format="full", comparisons_correction=None)
print("Wilcoxon on SHUFFLED rows (pairing by row order, no id):", txt); plt.close(fig)

# Kruskal / 4 groups pairwise count and adjustment
fd = pd.read_csv(f"{D}/data/four_group.csv"); fo = ["A","B","C","D"]
pr = list(itertools.combinations(fo, 2))
rawf = [stats.mannwhitneyu(fd[fd.group==a].value, fd[fd.group==b].value).pvalue for a, b in pr]
print("\n4-group raw", np.round(rawf, 5), "holm stars", [stars(x) for x in holm(rawf)], "bonf stars", [stars(min(1,x*6)) for x in rawf])
fig, ax, an, txt = annotate(fd, pr, fo, test="Mann-Whitney", comparisons_correction="bonferroni", text_format="star"); print("bonferroni star", txt); plt.close(fig)
fig, ax, an, txt = annotate(fd, pr, fo, test="Mann-Whitney", comparisons_correction="holm", text_format="star"); print("holm star", txt); plt.close(fig)
# only a SUBSET of pairs: count corrected = number of pairs passed
sub = [("A","C"),("B","C")]
fig, ax, an, txt = annotate(fd, sub, fo, test="Mann-Whitney", comparisons_correction="bonferroni", text_format="full"); print("bonferroni subset(2) full", txt, "| p*2 truth", [round(min(1, rawf[pr.index(s)]*2),5) for s in sub], "p*6", [round(min(1, rawf[pr.index(s)]*6),5) for s in sub]); plt.close(fig)
# Kruskal
fig, ax, an, txt = annotate(fd, [("A","C")], fo, test="Kruskal", text_format="full", comparisons_correction=None); print("Kruskal (2 groups)", txt, "truth", stats.kruskal(fd[fd.group=='A'].value, fd[fd.group=='C'].value).pvalue); plt.close(fig)
