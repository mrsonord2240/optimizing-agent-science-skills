"""
SYNTHETIC data generator for the audit of bio-experimental-design-multiple-testing.

Everything produced here is SYNTHETIC. No real samples, no real genes, no real
GWAS study. Gene identifiers are of the form SYNGENE00001 to make that obvious.

The point of the design is PLANTED GROUND TRUTH: for every feature we know
whether the null is true, so realized FDR and power of any correction procedure
can be measured exactly rather than argued about.

Design
------
m      = 18000 "genes", n = 6 vs 6 samples, log2-expression scale.
mu_g   ~ Normal(6, 2), clipped to [1, 14]      -> the "mean expression" covariate
sigma_g= exp(1.1 - 0.16 * mu_g + N(0, 0.25))   -> mean-variance trend: low-expression
                                                  genes are noisier, so POWER rises
                                                  with mean expression. That is what
                                                  makes mean expression an INFORMATIVE
                                                  but null-independent IHW covariate.
1500 true alternatives (pi0 = 0.9167), effect size drawn independently of mu_g.
Test   = pooled two-sample t-test -> exactly uniform p-values under the null.

Also emitted:
  * overall (group-blind) per-gene variance -- the NON-independent filter statistic
    from Bourgon 2010, because it absorbs the between-group difference.
  * a small 40-term "GO enrichment" table that is entirely null, for the edge case.

Outputs (all CSV, all SYNTHETIC):
  synthetic_de_pvalues.csv
  synthetic_go_all_null.csv
"""
import numpy as np
import pandas as pd

RNG = np.random.default_rng(20260916)
M = 18000
N_ALT = 1500
N_PER_GROUP = 6

mu = np.clip(RNG.normal(6.0, 2.0, M), 1.0, 14.0)
sigma = np.exp(1.1 - 0.16 * mu + RNG.normal(0.0, 0.25, M))

truth = np.zeros(M, dtype=int)
alt_idx = RNG.choice(M, N_ALT, replace=False)
truth[alt_idx] = 1

# Effect size in absolute log2 units, drawn INDEPENDENTLY of mu.
# Power therefore varies with mu only through sigma -> informative covariate.
effect = np.zeros(M)
effect[alt_idx] = RNG.uniform(0.9, 2.4, N_ALT) * RNG.choice([-1.0, 1.0], N_ALT)

grp_a = RNG.normal(mu[:, None], sigma[:, None], size=(M, N_PER_GROUP))
grp_b = RNG.normal((mu + effect)[:, None], sigma[:, None], size=(M, N_PER_GROUP))

ma, mb = grp_a.mean(1), grp_b.mean(1)
va, vb = grp_a.var(1, ddof=1), grp_b.var(1, ddof=1)
sp2 = (va + vb) / 2.0                      # pooled within-group variance
se = np.sqrt(sp2 * (2.0 / N_PER_GROUP))
tstat = (mb - ma) / se
df = 2 * N_PER_GROUP - 2

from scipy import stats
pval = 2 * stats.t.sf(np.abs(tstat), df)

allsamp = np.hstack([grp_a, grp_b])
overall_var = allsamp.var(1, ddof=1)       # group-blind variance: NOT null-independent
observed_mean = allsamp.mean(1)            # group-blind mean: IS null-independent

de = pd.DataFrame({
    "gene_id": [f"SYNGENE{i+1:05d}" for i in range(M)],
    "pvalue": pval,
    "tstat": tstat,
    "log2fc": mb - ma,
    "mean_expression": observed_mean,       # the legitimate IHW covariate / filter
    "overall_variance": overall_var,        # the illegitimate filter (Bourgon 2010)
    "within_variance": sp2,
    "true_mu": mu,
    "true_sigma": sigma,
    "true_effect": effect,
    "is_truly_de": truth,                   # PLANTED GROUND TRUTH
})
de.to_csv("F:/OpenScience/audits/bio-experimental-design-multiple-testing/data/"
          "synthetic_de_pvalues.csv", index=False)

# --- homogeneous-variance companion set ------------------------------------
# Identical design but every gene shares sigma = 1. With the across-gene spread
# in sigma removed, the group-blind ("overall") variance is dominated by the
# between-group difference, which is exactly the regime in which filtering on
# variance stops being null-independent (Bourgon 2010). Used to test the
# skill's independent-filtering claim under conditions where the claim bites.
M2 = 12000
N_ALT2 = 1000
truth2 = np.zeros(M2, dtype=int)
alt2 = RNG.choice(M2, N_ALT2, replace=False)
truth2[alt2] = 1
effect2 = np.zeros(M2)
effect2[alt2] = RNG.uniform(0.9, 2.4, N_ALT2) * RNG.choice([-1.0, 1.0], N_ALT2)
mu2 = np.clip(RNG.normal(6.0, 2.0, M2), 1.0, 14.0)
a2 = RNG.normal(mu2[:, None], 1.0, size=(M2, N_PER_GROUP))
b2 = RNG.normal((mu2 + effect2)[:, None], 1.0, size=(M2, N_PER_GROUP))
sp2b = (a2.var(1, ddof=1) + b2.var(1, ddof=1)) / 2.0
t2 = (b2.mean(1) - a2.mean(1)) / np.sqrt(sp2b * (2.0 / N_PER_GROUP))
p2 = 2 * stats.t.sf(np.abs(t2), df)
all2 = np.hstack([a2, b2])
pd.DataFrame({
    "gene_id": [f"SYNHOM{i+1:05d}" for i in range(M2)],
    "pvalue": p2,
    "mean_expression": all2.mean(1),
    "overall_variance": all2.var(1, ddof=1),
    "within_variance": sp2b,
    "is_truly_de": truth2,
}).to_csv("F:/OpenScience/audits/bio-experimental-design-multiple-testing/data/"
          "synthetic_de_homovar.csv", index=False)
print("SYNTHETIC homoscedastic set: %d genes, %d alternatives" % (M2, N_ALT2))

# --- small, entirely-null enrichment table for the edge case ---------------
go = pd.DataFrame({
    "term_id": [f"SYNGO:{i+1:07d}" for i in range(40)],
    "term_name": [f"synthetic biological process {i+1}" for i in range(40)],
    "pvalue": RNG.uniform(0, 1, 40),        # ALL NULL by construction
    "n_genes_in_term": RNG.integers(15, 300, 40),
    "is_truly_enriched": 0,
})
go.to_csv("F:/OpenScience/audits/bio-experimental-design-multiple-testing/data/"
          "synthetic_go_all_null.csv", index=False)

print("SYNTHETIC DE table:", de.shape,
      "| true alternatives:", int(truth.sum()),
      "| pi0(true) = %.4f" % (1 - truth.mean()))
print("raw p < 0.05:", int((pval < 0.05).sum()),
      "| null p<0.05 (expect ~%.0f):" % (0.05 * (M - N_ALT)),
      int(((pval < 0.05) & (truth == 0)).sum()))
print("corr(mean_expression, pvalue | null) = %.4f" %
      np.corrcoef(observed_mean[truth == 0], pval[truth == 0])[0, 1])
print("corr(overall_variance, pvalue | null) = %.4f" %
      np.corrcoef(overall_var[truth == 0], pval[truth == 0])[0, 1])
print("SYNTHETIC all-null GO table:", go.shape)
