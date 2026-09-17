# Input 7 -- Adversarial: "Our RNA-seq comparison came back non-significant (p=0.14). A reviewer
# wants us to report the observed/post-hoc power of the test to show the result isn't just
# underpowered noise. Can you compute that for us?"
# Checks the Skill's central claim (Hoenig & Heisey 2001): observed power is a deterministic,
# monotone function of the p-value alone, so it adds no information beyond the p-value itself --
# i.e. the Skill's instruction to refuse this request and report CI/prospective power instead is
# not merely a style preference, it is because the number carries no new information.

suppressPackageStartupMessages(library(pwr))

# observed power for a one-sample/two-sample z-style test is 1 - pnorm(z_crit - z_obs), and
# z_obs is a strictly increasing function of the two-sided p-value (for p < 1). Demonstrate the
# 1:1 mapping numerically using pwr.t.test's post-hoc mode (power solved from a fixed observed d).
alpha <- 0.05
ns <- c(5, 5, 5)  # same design, only the observed effect size (hence p-value) varies
ds_obs <- c(0.3, 0.6, 0.9)  # three different "observed" effect sizes at the same n

cat("Demonstrating observed power = f(p-value) only, holding n fixed:\n")
for (i in seq_along(ds_obs)) {
  d <- ds_obs[i]; n <- ns[i]
  t_obs <- d * sqrt(n / 2)   # approx two-sample t statistic for Cohen's d at n per group
  p_obs <- 2 * pt(-abs(t_obs), df = 2 * n - 2)
  post_hoc_power <- pwr.t.test(n = n, d = d, sig.level = alpha, type = "two.sample")$power
  cat(sprintf("  d_obs=%.2f  n=%d  p_obs=%.4f  post-hoc power=%.4f\n", d, n, p_obs, post_hoc_power))
}
cat("\n-> As p_obs falls, post-hoc power rises monotonically at fixed n and alpha: it is a\n")
cat("   relabeling of the p-value, not new information about whether the study had adequate\n")
cat("   power to detect a pre-specified, biologically meaningful effect.\n")
