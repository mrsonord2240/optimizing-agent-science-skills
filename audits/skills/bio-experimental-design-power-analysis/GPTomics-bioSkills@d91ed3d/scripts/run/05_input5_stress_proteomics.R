# Input 5 -- Scope boundary / decision-tree row: "We're running DIA proteomics on about 4000
# proteins, expect roughly 20% missingness, and want to detect a 1.3-fold (log2 ~0.38) change at
# 80% power. How many biological replicates?"
# Exercises the SKILL.md "Algorithmic Taxonomy" row: pwr::pwr.t.test per protein after a
# variance-stabilizing transform (Gaussian, continuous log-abundance).

suppressPackageStartupMessages(library(pwr))

cat("=== pwr.t.test at several plausible effect sizes (Cohen's d), alpha=0.05 uncorrected ===\n")
for (d in c(0.5, 0.8, 1.0, 1.2)) {
  r <- pwr.t.test(d = d, sig.level = 0.05, power = 0.80, type = "two.sample")
  cat(sprintf("d=%.1f  ->  n=%.2f per group (ceil %d)\n", d, r$n, ceiling(r$n)))
}

cat("\n=== Same, but with Bonferroni correction for 4000 proteins tested (0.05/4000) ===\n")
for (d in c(0.5, 0.8, 1.0, 1.2)) {
  r <- pwr.t.test(d = d, sig.level = 0.05/4000, power = 0.80, type = "two.sample")
  cat(sprintf("d=%.1f  ->  n=%.2f per group (ceil %d)\n", d, r$n, ceiling(r$n)))
}

cat("\n=== Checking against SKILL.md's own decision-tree row: 'pwr::pwr.t.test per protein with missingness caveat' ===\n")
