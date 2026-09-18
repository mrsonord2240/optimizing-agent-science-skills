# Input 7 (Adversarial, NEW angle) — regression of pre-fix Input 6's core numeric claim,
# plus a genuinely new stress case: does the Bonferroni-adjustment formula generalize to
# a SMALL targeted panel (m=50), not just the m=5000 discovery-wide case the fix log
# quotes? A reviewer might reasonably push back: "your alpha-adjustment formula must be
# wrong for small panels, since m=50 barely needs correction."
suppressPackageStartupMessages(library(pwr))

cat("=== Part A: regression of the fix log's headline numbers (m=5000, d=1.2) ===\n")
unadj <- pwr.t.test(d = 1.2, sig.level = 0.05, power = 0.80)
adj_5000 <- pwr.t.test(d = 1.2, sig.level = 0.05 / 5000, power = 0.80)
cat(sprintf("Unadjusted (per-protein alpha=0.05): n=%.2f/group\n", unadj$n))
cat(sprintf("Bonferroni-adjusted (m=5000): n=%.2f/group\n", adj_5000$n))
cat("Fix log claims: 11.94 unadjusted, 43.26 Bonferroni-adjusted -- ",
    if (abs(unadj$n - 11.94) < 0.05 && abs(adj_5000$n - 43.26) < 0.05) "MATCHES" else "DOES NOT MATCH", "\n")

cat("\n=== Part B: NEW - does the same formula make sense for a targeted m=50 panel? ===\n")
adj_50 <- pwr.t.test(d = 1.2, sig.level = 0.05 / 50, power = 0.80)
cat(sprintf("Bonferroni-adjusted (m=50): n=%.2f/group\n", adj_50$n))

cat("\n=== Part C: does the Bonferroni n actually deliver 80%% BH power under simulation, at both panel sizes? ===\n")
simulate_bh_power <- function(m, n_per_group, d_true = 1.2, p_changed = 0.10, mnar_frac = 0.20, nsim = 30) {
  changed <- seq_len(round(m * p_changed))
  powers <- numeric(nsim)
  for (s in seq_len(nsim)) {
    pvals <- numeric(m)
    for (g in seq_len(m)) {
      true_d <- if (g %in% changed) d_true else 0
      x <- rnorm(n_per_group, mean = true_d, sd = 1)
      y <- rnorm(n_per_group, mean = 0, sd = 1)
      # MNAR-style dropout: bias low-abundance draws to missing, drop mnar_frac at random per group
      keep_x <- rbinom(n_per_group, 1, 1 - mnar_frac) == 1
      keep_y <- rbinom(n_per_group, 1, 1 - mnar_frac) == 1
      if (sum(keep_x) < 2 || sum(keep_y) < 2) { pvals[g] <- NA; next }
      pvals[g] <- t.test(x[keep_x], y[keep_y])$p.value
    }
    padj <- p.adjust(pvals, method = "BH")
    powers[s] <- mean(padj[changed] < 0.05, na.rm = TRUE)
  }
  mean(powers, na.rm = TRUE)
}
set.seed(20260918)
p_5000 <- simulate_bh_power(5000, round(adj_5000$n))
cat(sprintf("m=5000, Bonferroni n=%d/group -> simulated BH marginal power = %.3f\n", round(adj_5000$n), p_5000))
set.seed(20260918)
p_50 <- simulate_bh_power(50, round(adj_50$n))
cat(sprintf("m=50, Bonferroni n=%d/group -> simulated BH marginal power = %.3f\n", round(adj_50$n), p_50))

cat("\n=== Part D: what does the unadjusted n actually deliver under the same multiplicity? ===\n")
set.seed(20260918)
p_unadj_5000 <- simulate_bh_power(5000, round(unadj$n))
cat(sprintf("m=5000, UNADJUSTED n=%d/group -> simulated BH marginal power = %.3f (SKILL.md's warned-against case)\n",
            round(unadj$n), p_unadj_5000))
