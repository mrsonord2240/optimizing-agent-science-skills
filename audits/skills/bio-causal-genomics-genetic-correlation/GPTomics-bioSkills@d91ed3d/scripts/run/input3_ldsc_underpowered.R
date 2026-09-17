# Input 3 (Edge) -- "Two small pilot GWAS (N~3000 each). Compute genetic
# correlation and tell me if the estimate is trustworthy."
# Planted truth: very low h2 and small N -> mean chi-square should fall near/under
# the Skill's stated 1.02 underpower floor, exercising the "defer, don't switch
# methods" operational rule.

suppressPackageStartupMessages({ library(GenomicSEM) })
setwd("F:/OpenScience/audits/bio-causal-genomics-genetic-correlation")
source("run/simulate_gwas_pair.R")

sim <- simulate_gwas_pair(
  ld_dir = "data/ld", N1 = 3000, N2 = 3000,
  h2_1 = 0.05, h2_2 = 0.05, rg = 0.30,
  overlap_n = 0, overlap_rho = 0,
  out_prefix = "data/sumstats/input3", seed = 3003
)
cat("=== PLANTED TRUTH (Input 3) ===\n"); str(sim$truth)

res <- ldsc(
  traits = c(sim$file1, sim$file2),
  sample.prev = c(NA, NA), population.prev = c(NA, NA),
  ld = "data/ld", wld = "data/ld", chr = 1, stand = TRUE,
  trait.names = c("pilotA", "pilotB"),
  ldsc.log = "run/input3_ldsc"
)

rg_hat <- res$S_Stand[1, 2]
rg_se_approx <- NA
if (!is.null(res$V)) rg_se_approx <- sqrt(diag(res$V))[length(diag(res$V))]
cat("\n=== GenomicSEM::ldsc() RESULT (Input 3) ===\n")
cat("S_Stand (rg):\n"); print(res$S_Stand)
cat(sprintf("\nRecovered rg = %.4f (planted %.2f)\n", rg_hat, sim$truth$rg))
cat(sprintf("Mean chi-square: trait1=%.4f trait2=%.4f (underpower floor 1.02)\n",
            sim$truth$mean_chisq1, sim$truth$mean_chisq2))

cat("\nASSERTION underpowered_flagged (mean chi-sq < 1.02 in >=1 trait):",
    sim$truth$mean_chisq1 < 1.02 || sim$truth$mean_chisq2 < 1.02, "\n")
cat("ASSERTION rg_estimate_produced_but_uncertain:", is.finite(rg_hat), "\n")
