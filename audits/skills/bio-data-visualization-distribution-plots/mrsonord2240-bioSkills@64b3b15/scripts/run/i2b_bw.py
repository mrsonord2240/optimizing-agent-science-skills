# Input 2b: how much bimodality does the SKILL's Python raincloud bandwidth (bw='scott') keep vs Sheather-Jones? SYNTHETIC input-1 data.
import numpy as np, pandas as pd
from scipy.stats import gaussian_kde
df = pd.read_csv(r"F:\OpenScience\audits\bio-data-visualization-distribution-plots\run\data\i1_synthetic_2group.csv")
x = df.loc[df.group == "Treated", "value"].to_numpy(); n = len(x)
grid = np.linspace(x.min() - 1, x.max() + 1, 1000)
def trough_ratio(bw_abs):
    # gaussian_kde with covariance factor = bw_abs / std
    k = gaussian_kde(x, bw_method=bw_abs / x.std(ddof=1)); y = k(grid)
    lo, hi = grid < 4.9, grid >= 4.9
    return y[(grid > 3.5) & (grid < 6.5)].min() / min(y[lo].max(), y[hi].max()), y.max()
scott_bw = n ** (-1 / 5) * x.std(ddof=1)       # what seaborn/scipy 'scott' uses
sj_bw = 0.363                                   # bw.SJ from R on the same data (run/out/i1_gg4.log)
for name, bw in [("scott (ptitprince bw='scott')", scott_bw), ("Sheather-Jones (R bw.SJ, 0.363)", sj_bw)]:
    r, ymax = trough_ratio(bw); print(f"{name}: bw={bw:.3f}  valley/lower-peak density ratio = {r:.3f}")
print("raw data: points between 4 and 6 in Treated:", int(((x > 4) & (x < 6)).sum()), "of", n)
