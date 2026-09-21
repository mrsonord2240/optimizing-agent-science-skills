# Independent ground truth: scipy + statsmodels-free manual Holm/Bonferroni/BH
import pandas as pd, numpy as np, itertools, json
from scipy import stats
D = r"F:\OpenScience\audits\bio-data-visualization-statistical-annotation\data"
def adj(p, m):
    p = np.array(p); n = len(p); o = np.argsort(p)
    if m == "holm":
        r = np.maximum.accumulate((n - np.arange(n)) * p[o]); r = np.minimum(r, 1)
    elif m == "bonferroni":
        r = np.minimum(p[o] * n, 1)
    elif m == "BH":
        r = np.minimum.accumulate((n / np.arange(n, 0, -1)) * p[o][::-1] * 0 + (p[o] * n / (np.arange(n) + 1))[::-1])[::-1]; r = np.minimum(r, 1)
    out = np.empty(n); out[o] = r; return out
df = pd.read_csv(D + r"\three_group.csv")
pairs = [("Control","Treatment"),("Control","Vehicle"),("Treatment","Vehicle")]
res = {}
for test in ["wilcox", "welch"]:
    raw = []
    for a, b in pairs:
        x = df[df.group == a].value; y = df[df.group == b].value
        raw.append(stats.mannwhitneyu(x, y, alternative="two-sided", method="auto").pvalue if test == "wilcox" else stats.ttest_ind(x, y, equal_var=False).pvalue)
    res[test] = {"raw": raw, "holm": list(adj(raw, "holm")), "bonf": list(adj(raw, "bonferroni")), "BH": list(adj(raw, "BH"))}
print("3-group"); print(json.dumps(res, indent=1))
print("KW", stats.kruskal(*[df[df.group == g].value for g in ["Control","Treatment","Vehicle"]]))
four = pd.read_csv(D + r"\four_group.csv")
print(four.groupby("group").value.agg(["count","mean"]))
raw = []; pr = list(itertools.combinations(["A","B","C","D"], 2))
for a, b in pr:
    raw.append(stats.mannwhitneyu(four[four.group==a].value, four[four.group==b].value, alternative="two-sided").pvalue)
print("4-group wilcox raw", dict(zip(pr, np.round(raw, 5)))); print("holm", np.round(adj(raw,"holm"),5)); print("bonf", np.round(adj(raw,"bonferroni"),5))
pd_ = pd.read_csv(D + r"\paired.csv")
pre = pd_[pd_.time=="Pre"].value.values; post = pd_[pd_.time=="Post"].value.values
print("paired: wilcoxon", stats.wilcoxon(pre, post).pvalue, "paired t", stats.ttest_rel(pre, post).pvalue, "unpaired MWU", stats.mannwhitneyu(pre, post).pvalue, "unpaired welch", stats.ttest_ind(pre, post, equal_var=False).pvalue)
n = pd.read_csv(D + r"\nested.csv")
print("nested cells MWU", stats.mannwhitneyu(n[n.group=="Ctl"].value, n[n.group=="Trt"].value).pvalue)
pp = n.groupby(["group","subject_id"]).value.mean().reset_index()
print("per-patient means", pp.to_string()); print("per-patient welch", stats.ttest_ind(pp[pp.group=="Ctl"].value, pp[pp.group=="Trt"].value, equal_var=False).pvalue)
b = pd.read_csv(D + r"\bigN.csv")
print("bigN MWU", stats.mannwhitneyu(b[b.group=="X"].value, b[b.group=="Y"].value).pvalue, "d", (b[b.group=="Y"].value.mean()-b[b.group=="X"].value.mean())/b.value.std())
