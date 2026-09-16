"""
Input 5 (Stress / multi-part) -- "Can I gain power by dropping the bottom half of
genes before testing? I was going to filter on per-gene variance, keeping the most
variable genes. And can I use that same variance as the IHW covariate?"

The SKILL.md section "Independent Filtering -- Power for Free, If the Filter Is
Independent" says the filter statistic must be independent of the test statistic
under the null, that overall mean count qualifies, and that "a pre-test on variance
or a preliminary t-test is NOT independent and biases the FDR".

This script tests that claim against planted ground truth, first on the stored
SYNTHETIC homoscedastic table and then over 300 fresh replicates.
"""
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

DATA = ("F:/OpenScience/audits/bio-experimental-design-multiple-testing/data/"
        "synthetic_de_homovar.csv")
ALPHA = 0.05


def bh_scores(p, truth, label, n_alt_total):
    rej, _, _, _ = multipletests(p, alpha=ALPHA, method="fdr_bh")
    R = int(rej.sum()); V = int((rej & ~truth).sum()); S = int((rej & truth).sum())
    print(f"{label:38s} kept={len(p):6d}  R={R:5d}  true+={S:5d}  false+={V:4d}  "
          f"FDP={V/R if R else 0:.4f}  power={S/n_alt_total:.4f}")
    return (V / R if R else 0.0), S / n_alt_total


d = pd.read_csv(DATA)
p, truth = d["pvalue"].values, d["is_truly_de"].values.astype(bool)
n_alt = int(truth.sum())
print(f"SYNTHETIC homoscedastic table: {len(p)} genes, {n_alt} true alternatives "
      f"(pi0={1-truth.mean():.4f}), sigma identical for every gene")

print("\n-- stored table, single draw --")
bh_scores(p, truth, "no filter", n_alt)
for frac in (0.5,):
    k = d["overall_variance"].rank(pct=True) > (1 - frac)
    bh_scores(p[k.values], truth[k.values], f"filter: top {frac:.0%} overall VARIANCE", n_alt)
    k2 = d["mean_expression"].rank(pct=True) > (1 - frac)
    bh_scores(p[k2.values], truth[k2.values], f"filter: top {frac:.0%} overall MEAN", n_alt)

# --- 300 fresh replicates --------------------------------------------------
RNG = np.random.default_rng(987654)
M, N_ALT, NPG, REPS = 6000, 500, 6, 300
df = 2 * NPG - 2
acc = {k: {"fdp": [], "pow": []} for k in
       ("none", "variance50", "mean50", "pretest")}
for _ in range(REPS):
    tr = np.zeros(M, dtype=bool); tr[:N_ALT] = True
    eff = np.where(tr, RNG.uniform(0.9, 2.4, M) * RNG.choice([-1., 1.], M), 0.0)
    mu = np.clip(RNG.normal(6, 2, M), 1, 14)
    a = RNG.normal(mu[:, None], 1.0, (M, NPG))
    b = RNG.normal((mu + eff)[:, None], 1.0, (M, NPG))
    sp2 = (a.var(1, ddof=1) + b.var(1, ddof=1)) / 2
    t = (b.mean(1) - a.mean(1)) / np.sqrt(sp2 * 2 / NPG)
    pv = 2 * stats.t.sf(np.abs(t), df)
    allx = np.hstack([a, b])
    ov, om = allx.var(1, ddof=1), allx.mean(1)
    # a deliberately illegitimate filter: a preliminary t-test on the same data
    pre = pv < 0.5
    masks = {"none": np.ones(M, bool),
             "variance50": ov >= np.median(ov),
             "mean50": om >= np.median(om),
             "pretest": pre}
    for key, mk in masks.items():
        rej, _, _, _ = multipletests(pv[mk], alpha=ALPHA, method="fdr_bh")
        R = rej.sum(); V = (rej & ~tr[mk]).sum(); S = (rej & tr[mk]).sum()
        acc[key]["fdp"].append(V / R if R else 0.0)
        acc[key]["pow"].append(S / N_ALT)

print(f"\n-- {REPS} fresh SYNTHETIC replicates (m={M}, {N_ALT} alternatives, "
      f"BH at alpha={ALPHA}) --")
print(f"{'filter':28s} {'mean FDP':>9s} {'sd FDP':>8s} {'P(FDP>a)':>9s} {'mean power':>11s}")
for key in ("none", "variance50", "mean50", "pretest"):
    f = np.array(acc[key]["fdp"])
    print(f"{key:28s} {f.mean():9.4f} {f.std():8.4f} {(f > ALPHA).mean():9.3f} "
          f"{np.mean(acc[key]['pow']):11.4f}")
