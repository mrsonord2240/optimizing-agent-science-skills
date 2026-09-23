# Fresh Phase 2 input 10: construct a fully synthetic 3-trait covstruc and
# SNP table for the extracted commonfactorGWAS helper. No real-person data.
source("synth_lib.R")
traits <- c("MDD", "ANX", "PTSD")
loadings <- c(0.75, 0.65, 0.70)
covstruc <- list(
  V = build_V(3, diag_var = 1e-4),
  S = name_S(build_one_factor_S(loadings, c(0.10, 0.06, 0.05)), traits),
  I = build_I(3)
)
set.seed(20260923)
n_factor <- 5L; n_het <- 5L; n_null <- 10L; n <- n_factor + n_het + n_null
beta <- matrix(0, n, 3)
for (i in seq_len(n_factor)) beta[i, ] <- 0.05 * loadings
for (i in (n_factor + 1):(n_factor + n_het)) beta[i, ] <- c(0.15, 0, 0)
beta[(n_factor + n_het + 1):n, ] <- matrix(rnorm(n_null * 3, 0, 0.002), n_null, 3)
snps <- data.frame(
  SNP = paste0("phase2_rs", seq_len(n)), A1 = "A", A2 = "G",
  MAF = seq(0.06, 0.44, length.out = n),
  beta.MDD = beta[, 1], se.MDD = 0.01,
  beta.ANX = beta[, 2], se.ANX = 0.01,
  beta.PTSD = beta[, 3], se.PTSD = 0.01
)
saveRDS(covstruc, "input10_covstruc.rds")
write.csv(snps, "input10_snps.csv", row.names = FALSE)
cat(sprintf("INPUT10 fixture: %d SNPs; %d factor; %d heterogeneous; %d null\\n", n, n_factor, n_het, n_null))
