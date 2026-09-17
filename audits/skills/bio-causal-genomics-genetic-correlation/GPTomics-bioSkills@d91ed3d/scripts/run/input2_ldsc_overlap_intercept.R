# Input 2 (Variant A / MR-validity stress test) -- "These two GWAS are both drawn
# from UK Biobank (~40k shared participants). Compute genetic correlation and tell
# me whether the sample overlap biases rg." Also doubles as the |rg|>0.3 CHP-aware
# MR-sensitivity trigger check (SKILL.md 'Relationship to MR Causal Inference').
#
# Planted truth: h2_1=0.25, h2_2=0.25, rg=0.35, substantial sample overlap
# (Ns=40000 of N1=N2=50000, phenotypic correlation among overlap 0.5). Directly
# tests the Skill's central claim: "cross-trait LDSC intercept absorbs sample
# overlap WITHOUT biasing the rg estimate."

suppressPackageStartupMessages({ library(GenomicSEM) })
setwd("F:/OpenScience/audits/bio-causal-genomics-genetic-correlation")
source("run/simulate_gwas_pair.R")

sim <- simulate_gwas_pair(
  ld_dir = "data/ld", N1 = 50000, N2 = 50000,
  h2_1 = 0.25, h2_2 = 0.25, rg = 0.35,
  overlap_n = 40000, overlap_rho = 0.5,
  out_prefix = "data/sumstats/input2", seed = 2002
)
cat("=== PLANTED TRUTH (Input 2) ===\n"); str(sim$truth)

res <- ldsc(
  traits = c(sim$file1, sim$file2),
  sample.prev = c(NA, NA), population.prev = c(NA, NA),
  ld = "data/ld", wld = "data/ld", chr = 1, stand = TRUE,
  trait.names = c("traitX", "traitY"),
  ldsc.log = "run/input2_ldsc"
)

rg_hat <- res$S_Stand[1, 2]
intercept_xy <- res$I[1, 2]
cat("\n=== GenomicSEM::ldsc() RESULT (Input 2) ===\n")
cat("S_Stand (rg):\n"); print(res$S_Stand)
cat("I (intercepts; off-diagonal = cross-trait intercept, overlap proxy):\n"); print(res$I)
cat(sprintf("\nRecovered rg = %.4f (planted %.2f)\n", rg_hat, sim$truth$rg))
cat(sprintf("Recovered cross-trait intercept = %.4f (planted/expected ~%.4f from overlap)\n",
            intercept_xy, sim$truth$expected_intercept))

cat("\nASSERTION rg_within_tolerance_despite_overlap:",
    abs(rg_hat - sim$truth$rg) < 0.20, "\n")
cat("ASSERTION intercept_materially_nonzero:", abs(intercept_xy) > 0.05, "\n")
cat("ASSERTION MR_CHP_trigger (|rg|>0.3):", abs(rg_hat) > 0.3, "\n")
