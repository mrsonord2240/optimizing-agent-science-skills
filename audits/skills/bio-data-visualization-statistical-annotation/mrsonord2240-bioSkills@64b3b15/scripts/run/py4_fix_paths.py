# Verify the two fix paths for statannotations: correction_format='replace' and set_pvalues() with independently computed Holm p. SYNTHETIC data.
import warnings, numpy as np, pandas as pd, seaborn as sns, matplotlib.pyplot as plt
from scipy import stats
from statannotations.Annotator import Annotator
warnings.filterwarnings("ignore")
D = "F:/OpenScience/audits/bio-data-visualization-statistical-annotation"
df = pd.read_csv(f"{D}/data/three_group.csv"); order = ["Control", "Treatment", "Vehicle"]
pairs = [("Control","Treatment"),("Control","Vehicle"),("Treatment","Vehicle")]
raw = [stats.mannwhitneyu(df[df.group==a].value, df[df.group==b].value).pvalue for a, b in pairs]
n = len(raw); o = np.argsort(raw); r = np.minimum(1, np.maximum.accumulate((n - np.arange(n)) * np.array(raw)[o])); holm = np.empty(n); holm[o] = r
print("raw", np.round(raw, 5), "holm", np.round(holm, 5))
for label, cfg in [("replace", dict(test="Mann-Whitney", comparisons_correction="holm", text_format="star", correction_format="replace"))]:
    fig, ax = plt.subplots(); sns.boxplot(x="group", y="value", data=df, order=order, ax=ax)
    an = Annotator(ax, pairs, data=df, x="group", y="value", order=order); an.configure(**cfg); an.apply_and_annotate(); print(label, [t.get_text() for t in ax.texts]); plt.close(fig)
fig, ax = plt.subplots(); sns.boxplot(x="group", y="value", data=df, order=order, ax=ax)
an = Annotator(ax, pairs, data=df, x="group", y="value", order=order); an.configure(text_format="star", loc="inside")
an.set_pvalues(list(holm)); an.annotate(); print("set_pvalues(holm)", [t.get_text() for t in ax.texts]); plt.close(fig)
