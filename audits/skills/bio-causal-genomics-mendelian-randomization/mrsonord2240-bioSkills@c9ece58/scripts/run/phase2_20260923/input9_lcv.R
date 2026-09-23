# Input 9 (NEW -- LCV clone now available, was absent pre-fix). This Skill's own Decision
# Tree lists LCV in the sensitivity battery for "Polygenic exposure with potential CHP" and
# its Statistical Model Taxonomy names LCV's gcp parameter explicitly, but ships no inline
# LCV code (points to LHC-MR/LCV only for "genome-wide resolution"). Tests whether following
# that documented workflow (RunLCV on genome-wide z-scores) actually produces the gcp
# statistic this Skill's own tables describe, using a planted partial-causation scenario.
setwd("F:/OpenScience/audit-envs/mendelian-randomization-analyst/tools/src/LCV/R")
source("RunLCV.R")

set.seed(5)
m <- 3000
ell <- runif(m, 1, 60)          # per-SNP LD score, genome-wide-style
true_gcp <- 0.6                  # planted: trait 1 mostly causal for trait 2 (partial)
z1 <- rnorm(m, 0, sqrt(ell))
# Mix of a causal path (z1 -> z2) and independent genetic-correlation-only noise so gcp
# lands short of 1 (full causation) but clearly above 0 (pure correlation).
z2 <- true_gcp * 0.5 * z1 + rnorm(m, 0, sqrt(ell))

t0 <- Sys.time()
res_lcv <- RunLCV(ell, z1, z2, no.blocks = 20)
cat("RunLCV wall time (s):", round(as.numeric(Sys.time() - t0, units = "secs"), 1), "\n")

cat("\nFields returned by RunLCV():\n")
print(names(res_lcv))

cat("\ngcp.pm (posterior mean gcp):", round(res_lcv$gcp.pm, 4), "\n")
cat("gcp.pse (posterior SE):", round(res_lcv$gcp.pse, 4), "\n")
cat("p-value gcp=0 (two-tailed):", signif(res_lcv$pval.gcpzero.2tailed, 3), "\n")
cat("rho.est (genetic correlation):", round(res_lcv$rho.est, 4), "\n")

cat("\nPlanted scenario: partial causal contribution from trait1->trait2 (not pure genetic\n")
cat("correlation, not full determinism). gcp.pm magnitude should land strictly between 0 and 1.\n")
