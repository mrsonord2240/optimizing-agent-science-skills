# Input 1 (Canonical) -- "Compute genetic correlation between trait A and trait B
# using cross-trait LDSC with the EUR reference panel. Report rg, SE, p-value, and
# the gcov intercept."
#
# Executes the Skill's documented "GenomicSEM ldsc()" alternative to CLI ldsc.py
# (ldsc.py itself was not installed in this environment at audit time -- see
# eval_viewer for the note). Planted truth: h2_1=0.30, h2_2=0.25, rg=0.45, NO
# sample overlap. Synthetic single-chromosome LD reference (data/ld), synthetic
# sumstats (data/sumstats) -- not real GWAS.

suppressPackageStartupMessages({ library(GenomicSEM) })
setwd("F:/OpenScience/audits/bio-causal-genomics-genetic-correlation")
source("run/simulate_gwas_pair.R")

sim <- simulate_gwas_pair(
  ld_dir = "data/ld", N1 = 80000, N2 = 60000,
  h2_1 = 0.30, h2_2 = 0.25, rg = 0.45,
  overlap_n = 0, overlap_rho = 0,
  out_prefix = "data/sumstats/input1", seed = 1001
)
cat("=== PLANTED TRUTH (Input 1) ===\n"); str(sim$truth)

res <- ldsc(
  traits = c(sim$file1, sim$file2),
  sample.prev = c(NA, NA), population.prev = c(NA, NA),
  ld = "data/ld", wld = "data/ld", chr = 1, stand = TRUE,
  trait.names = c("traitA", "traitB"),
  ldsc.log = "run/input1_ldsc"
)

cat("\n=== GenomicSEM::ldsc() RESULT (Input 1) ===\n")
cat("Genetic covariance matrix S:\n"); print(res$S)
cat("Standardized (rg) matrix S_Stand:\n"); print(res$S_Stand)
cat("Intercept matrix I:\n"); print(res$I)

rg_hat <- res$S_Stand[1, 2]
h2_1_hat <- res$S[1, 1]; h2_2_hat <- res$S[2, 2]
cat(sprintf("\nRecovered rg = %.4f (planted %.2f)\n", rg_hat, sim$truth$rg))
cat(sprintf("Recovered h2_1 = %.4f (planted %.2f), h2_2 = %.4f (planted %.2f)\n",
            h2_1_hat, sim$truth$h2_1, h2_2_hat, sim$truth$h2_2))
cat(sprintf("Mean chi-square: trait1=%.3f trait2=%.3f (underpower floor is 1.02)\n",
            sim$truth$mean_chisq1, sim$truth$mean_chisq2))

cat("\nASSERTION rg_within_tolerance:",
    abs(rg_hat - sim$truth$rg) < 0.20, "\n")
cat("ASSERTION h2_positive_both:", h2_1_hat > 0 && h2_2_hat > 0, "\n")
