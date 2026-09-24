# Synthetic two-sample MR summary statistics with planted truth.
# usage: r.sh 01_simulate.R <scenario: A|B> <outdir>
#  A: true causal beta = 0.30, 30% of instruments pleiotropic (directional, mean alpha 0.02)
#  B: true causal beta = 0.00 (NULL), same 30% directional pleiotropy -> IVW false positive expected
args <- commandArgs(TRUE); scen <- args[1]; outdir <- args[2]
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)
set.seed(if (scen == "A") 2026 else 2027)
beta_true <- if (scen == "A") 0.30 else 0.00
n_inst <- 100; n_null <- 300; n_bad <- 30
Nx <- 200000; Ny <- 100000
comp <- c(A="T", C="G", G="C", T="A")
pairs <- list(c("A","G"), c("A","C"), c("T","G"), c("C","T"))
mk <- function(n) {
  p <- pairs[sample(length(pairs), n, TRUE)]
  data.frame(a1 = sapply(p, `[`, 1), a2 = sapply(p, `[`, 2), stringsAsFactors = FALSE)
}
n <- n_inst + n_null
snp <- paste0("rs", 100000 + seq_len(n))
al <- mk(n)
maf <- runif(n, 0.1, 0.5)
gamma <- c(pmax(abs(rnorm(n_inst, 0.05, 0.02)), 0.02), rep(0, n_null))   # oriented positive
bad <- c(rep(TRUE, n_bad), rep(FALSE, n_inst - n_bad), rep(FALSE, n_null))
bad <- c(sample(bad[1:n_inst]), rep(FALSE, n_null))
alpha <- ifelse(bad, rnorm(n, 0.02, 0.005), 0)      # directional pleiotropy, independent of gamma (InSIDE)
se_x <- 1 / sqrt(Nx * 2 * maf * (1 - maf)); se_y <- 1 / sqrt(Ny * 2 * maf * (1 - maf))
bx <- rnorm(n, gamma, se_x)
by <- rnorm(n, gamma * beta_true + alpha, se_y)
# random allele orientation in the exposure file
flip <- sample(c(TRUE, FALSE), n, TRUE)
ex <- data.frame(SNP = snp, A1 = ifelse(flip, al$a2, al$a1), A2 = ifelse(flip, al$a1, al$a2),
                 EAF = ifelse(flip, 1 - maf, maf), BETA = ifelse(flip, -bx, bx), SE = se_x, N = Nx)
ex$P <- 2 * pnorm(-abs(ex$BETA / ex$SE))
# outcome file: 15% of SNPs reported with alleles in the opposite order (needs harmonising)
sw <- sample(c(TRUE, FALSE), n, TRUE, prob = c(0.15, 0.85))
oy <- data.frame(SNP = snp, A1 = ex$A1, A2 = ex$A2, EAF = ifelse(flip, 1 - maf, maf),
                 BETA = ifelse(flip, -by, by), SE = se_y, N = Ny)
oy[sw, c("A1", "A2")] <- oy[sw, c("A2", "A1")]
oy$BETA[sw] <- -oy$BETA[sw]; oy$EAF[sw] <- 1 - oy$EAF[sw]
oy$P <- 2 * pnorm(-abs(oy$BETA / oy$SE))
write.table(ex, file.path(outdir, "exposure_gwas.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)
write.table(oy, file.path(outdir, "outcome_gwas.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)
truth <- data.frame(SNP = snp, is_instrument = seq_len(n) <= n_inst, planted_invalid = bad, alpha = alpha)
write.table(truth, file.path(outdir, "truth_snps.tsv"), sep = "\t", row.names = FALSE, quote = FALSE)
writeLines(sprintf("scenario=%s\nbeta_true=%s\nn_instruments=%d\nn_planted_invalid=%d\nmean_alpha_over_instruments=%.4f\nnull_snps=%d",
   scen, beta_true, n_inst, sum(bad), mean(alpha[1:n_inst]), n_null), file.path(outdir, "truth.txt"))
cat(readLines(file.path(outdir, "truth.txt")), sep = "\n")
cat("exposure sig (p<5e-8):", sum(ex$P < 5e-8), " strand/order swapped in outcome:", sum(sw), "\n")
