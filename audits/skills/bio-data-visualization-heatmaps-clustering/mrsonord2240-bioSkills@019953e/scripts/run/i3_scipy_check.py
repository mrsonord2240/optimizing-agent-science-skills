"""Skill claim: seaborn method='ward' (scipy) is equivalent to R ward.D2. Compare merge heights on the same data (written by i3_edge_claims.R)."""
import numpy as np, pandas as pd, subprocess, json
from scipy.cluster import hierarchy as sch
x = pd.read_csv("i3_x.csv", index_col=0).values
L = sch.linkage(x, method="ward", metric="euclidean")
np.savetxt("i3_scipy_heights.txt", L[:, 2])
print("scipy top merge height:", round(L[-1, 2], 3), " (R ward.D2 top height was 67.4)")
