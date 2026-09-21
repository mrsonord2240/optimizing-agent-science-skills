"""INPUT 6b: SKILL.md names scanpy.pl.heatmap() as the single-cell option (no code given). SYNTHETIC counts: 3 cell types x 8 marker genes planted."""
import numpy as np, pandas as pd, scanpy as sc, anndata as ad, matplotlib
matplotlib.use("Agg")
rng = np.random.default_rng(4)
n, g = 300, 60
ct = np.repeat(["T", "B", "Mono"], 100)
X = rng.poisson(1.0, (n, g)).astype(float)
for k, c in enumerate(["T", "B", "Mono"]):
    X[np.ix_(ct == c, range(k*8, k*8+8))] += rng.poisson(6, (100, 8))
a = ad.AnnData(X, obs=pd.DataFrame({"celltype": pd.Categorical(ct, categories=["T","B","Mono"])}, index=[f"c{i}" for i in range(n)]),
               var=pd.DataFrame(index=[f"gene{i}" for i in range(g)]))
sc.pp.normalize_total(a, target_sum=1e4); sc.pp.log1p(a)
markers = [f"gene{i}" for i in range(24)]
ax = sc.pl.heatmap(a, markers, groupby="celltype", cmap="RdBu_r", standard_scale="var", swap_axes=True, show=False, save="_i6b.png")
import os, glob
f = glob.glob("figures/heatmap_i6b.png")
print("figure:", f, os.path.getsize(f[0]) if f else None)
# assert: mean expression of planted markers highest in their own type
m = pd.DataFrame(a[:, markers].X, columns=markers).groupby(ct).mean()
print("argmax cell type per gene block correct:", all(m.iloc[:, k*8:k*8+8].mean().idxmax() if False else m.iloc[:, k*8:k*8+8].mean(axis=1).idxmax() == c for k, c in enumerate(["T","B","Mono"])))
