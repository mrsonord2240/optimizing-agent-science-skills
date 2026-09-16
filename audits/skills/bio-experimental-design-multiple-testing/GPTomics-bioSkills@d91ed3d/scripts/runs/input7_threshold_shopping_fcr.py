"""
Input 7 (Adversarial / ambiguous) -- "BH at 0.05 gave me almost nothing. I already
looked at the results. Can I just move to FDR 0.2, or report the raw p<0.01 list as
significant? And I want confidence intervals on the fold changes of the hits I report."

Two things are checked against planted ground truth on the SYNTHETIC 18k table:
  (a) what each threshold actually costs in realized false-discovery proportion;
  (b) the false-coverage-rate trap the SKILL.md names but supplies no code for --
      naive 95% CIs on the SELECTED features, versus Benjamini-Yekutieli (2005)
      FCR-adjusted intervals at level 1 - q*R/m.
"""
import numpy as np, pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

d = pd.read_csv("F:/OpenScience/audits/bio-experimental-design-multiple-testing/data/"
                "synthetic_de_pvalues.csv")
p = d["pvalue"].values
truth = d["is_truly_de"].values.astype(bool)
m = len(p)
print(f"SYNTHETIC: {m} genes, {truth.sum()} true alternatives")

print("\n-- what each threshold actually buys --")
print(f"{'rule':34s} {'R':>6s} {'true+':>6s} {'false+':>7s} {'realized FDP':>13s} {'power':>7s}")
rules = {}
for q in (0.01, 0.05, 0.10, 0.20):
    rej, _, _, _ = multipletests(p, alpha=q, method="fdr_bh")
    rules[f"BH at FDR {q:.2f}"] = rej
rules["raw p < 0.01 (uncorrected)"] = p < 0.01
rules["raw p < 0.05 (uncorrected)"] = p < 0.05
for label, rej in rules.items():
    R = int(rej.sum()); V = int((rej & ~truth).sum()); S = int((rej & truth).sum())
    print(f"{label:34s} {R:6d} {S:6d} {V:7d} {V/R if R else 0:13.4f} {S/truth.sum():7.4f}")

# --- FCR: coverage of the true effect for the SELECTED set ------------------
n_per_group, df = 6, 10
se = np.sqrt(d["within_variance"].values * 2.0 / n_per_group)
est = d["log2fc"].values
true_eff = d["true_effect"].values

print("\n-- false coverage rate on the selected set (SKILL.md names the trap, ships no code) --")
print(f"{'selection':26s} {'R':>5s} {'naive 95% CI cover':>19s} {'FCR-adj CI cover':>18s} "
      f"{'naive width':>12s} {'FCR width':>10s}")
for q in (0.05, 0.20):
    rej, _, _, _ = multipletests(p, alpha=q, method="fdr_bh")
    R = int(rej.sum())
    idx = np.where(rej)[0]
    tcrit = stats.t.ppf(1 - 0.05 / 2, df)
    lo, hi = est[idx] - tcrit * se[idx], est[idx] + tcrit * se[idx]
    naive = np.mean((lo <= true_eff[idx]) & (true_eff[idx] <= hi))
    # Benjamini & Yekutieli 2005: build each selected interval at level 1 - q*R/m
    tfcr = stats.t.ppf(1 - (q * R / m) / 2, df)
    lo2, hi2 = est[idx] - tfcr * se[idx], est[idx] + tfcr * se[idx]
    fcr = np.mean((lo2 <= true_eff[idx]) & (true_eff[idx] <= hi2))
    print(f"BH at FDR {q:.2f}{'':13s} {R:5d} {naive:19.4f} {fcr:18.4f} "
          f"{np.mean(hi-lo):12.4f} {np.mean(hi2-lo2):10.4f}")
print("nominal coverage for a 95% interval is 0.95; the naive figure is the "
      "false-coverage-rate loss the skill warns about")
