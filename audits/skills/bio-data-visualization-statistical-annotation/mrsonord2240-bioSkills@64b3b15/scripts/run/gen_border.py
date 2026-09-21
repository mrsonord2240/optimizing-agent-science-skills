# SYNTHETIC: search seeds for a 3-group set where raw p is <0.05 for 3 pairs (some) but Holm/Bonferroni push at least one over 0.05.
import numpy as np, pandas as pd
from scipy import stats
D = r"F:\OpenScience\audits\bio-data-visualization-statistical-annotation\data"
for seed in range(1, 5000):
    rng = np.random.default_rng(seed)
    a = rng.lognormal(0.0, 0.6, 10); b = rng.lognormal(0.55, 0.6, 13); c = rng.lognormal(1.0, 0.6, 8)
    p = [stats.mannwhitneyu(a,b).pvalue, stats.mannwhitneyu(a,c).pvalue, stats.mannwhitneyu(b,c).pvalue]
    if p[0] < 0.045 and p[0] > 0.02 and p[1] < 0.004 and 0.02 < p[2] < 0.045:
        pd.DataFrame({"group": ["G1"]*10 + ["G2"]*13 + ["G3"]*8, "value": np.concatenate([a,b,c])}).to_csv(D + r"\border.csv", index=False)
        print("seed", seed, p); break
