"""INPUT 2 (Variant A): seaborn.clustermap block from SKILL.md, verbatim, on SYNTHETIC log-expression data with planted modules.
Ground truth: 3 gene modules x 2 sample groups (up/down patterns) + noise; raw values centred ~8 (log2 expression scale)."""
import numpy as np, pandas as pd, seaborn as sns, matplotlib
matplotlib.use("Agg")
from scipy.cluster import hierarchy as sch
rng = np.random.default_rng(3)
ng, ns = 90, 18
cond = np.array(["Control"] * 9 + ["Treatment"] * 9)
batch = np.array(["A", "B", "C"] * 6)
base = rng.normal(8, 1.5, size=(ng, 1))                     # per-gene baseline level (gene amplitude differs)
X = base + rng.normal(0, 0.4, size=(ng, ns))
X[:30, cond == "Treatment"] += 2.0                          # module 1 up
X[30:60, cond == "Treatment"] -= 2.0                        # module 2 down
truth = np.array(["up"] * 30 + ["down"] * 30 + ["flat"] * 30)
df = pd.DataFrame(X, index=[f"G{i}" for i in range(ng)], columns=[f"S{i}" for i in range(ns)])
metadata = pd.DataFrame({"condition": cond, "batch": batch}, index=df.columns)

# ------------------------ verbatim from SKILL.md ------------------------
# Robust symmetric bounds (1-99% quantile)
vmax = np.quantile(np.abs(df.values[~np.isnan(df.values)]), 0.99)

# col_colors / row_colors for categorical annotations
condition_colors = metadata['condition'].map({'Control': '#56B4E9', 'Treatment': '#D55E00'})
batch_colors = metadata['batch'].map({'A': '#009E73', 'B': '#0072B2', 'C': '#CC79A7'})
col_colors = pd.DataFrame({'Condition': condition_colors, 'Batch': batch_colors})

g = sns.clustermap(df,
                   cmap='RdBu_r', center=0, vmin=-vmax, vmax=vmax,
                   row_cluster=True, col_cluster=True,
                   method='ward',                      # seaborn uses scipy ward, equivalent to R ward.D2
                   metric='euclidean',
                   z_score=0,                          # 0 = rows, 1 = columns
                   col_colors=col_colors,
                   dendrogram_ratio=0.15,
                   cbar_pos=(0.02, 0.8, 0.03, 0.15),
                   figsize=(10, 12),
                   rasterized=True)                    # rasterize the cell layer
# ------------------------------------------------------------------------
g.savefig("i2_clustermap_verbatim.png", dpi=90)
print("vmax computed on RAW df:", round(vmax, 3))
Z = g.data2d.values                                     # what is actually plotted
print("plotted data range:", round(Z.min(), 2), round(Z.max(), 2), "| fraction of cells with |z| > 0.5*vmax:", round((np.abs(Z) > 0.5 * vmax).mean(), 3))
# assertions on what was plotted
ri, ci = g.dendrogram_row.reordered_ind, g.dendrogram_col.reordered_ind
zref = (df.sub(df.mean(axis=1), axis=0)).div(df.std(axis=1), axis=0)         # ddof=1 like pandas (seaborn uses DataFrame ops)
print("plotted == row z-score of input (rows reordered):", np.allclose(Z, zref.values[np.ix_(ri, ci)], atol=1e-9))
print("plotted rows have mean 0, sd 1:", np.allclose(Z.mean(axis=1), 0, atol=1e-9), np.allclose(Z.std(axis=1, ddof=1), 1, atol=1e-9))
# independent scipy ward on the z-scored matrix
L = sch.linkage(zref.values, method="ward", metric="euclidean")
lv = sch.leaves_list(L)
print("row leaf SET structure equals independent scipy ward (cophenetic identical):",
      np.allclose(sch.cophenet(L), sch.cophenet(g.dendrogram_row.linkage)))
# planted recovery: cut into 3
cl = sch.fcluster(g.dendrogram_row.linkage, 3, "maxclust")
print(pd.crosstab(cl, truth))
# columns: do Control and Treatment separate?
ccl = sch.fcluster(g.dendrogram_col.linkage, 2, "maxclust")
print(pd.crosstab(ccl, cond))
# col_colors follow the reordered columns
colcols = g.ax_col_colors.collections[0].get_array() if g.ax_col_colors.collections else None
order_cond = cond[ci]
print("drawn column order conditions:", "".join("C" if c == "Control" else "T" for c in order_cond))
# labels of drawn columns
print("xticklabels == df.columns[ci]:", [t.get_text() for t in g.ax_heatmap.get_xticklabels()] == list(df.columns[ci]))
print("z_score + standard_scale both:", end=" ")
try:
    sns.clustermap(df, z_score=0, standard_scale=0); print("no error")
except Exception as e:
    print(type(e).__name__, e)
