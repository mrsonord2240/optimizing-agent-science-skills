# Independent adversarial eQTL/LD fixture for the corrected two-trait guard.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1) stop("usage: input11_make_fresh_eqtl_mismatch.R <outdir>")
outdir <- args[[1]]
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)

set.seed(2026092211)
n <- 1400L
m <- 120L
causal <- 37L
snp <- sprintf("rs%d", seq_len(m))
pos <- seq.int(42000000L, by = 1000L, length.out = m)
R0 <- .68^abs(outer(seq_len(m), seq_len(m), "-"))
g_gwas <- scale(matrix(rnorm(n * m), n, m) %*% chol(R0))
y_gwas <- .42 * g_gwas[, causal] + rnorm(n)
sumstats <- function(y, g) do.call(rbind, lapply(seq_len(ncol(g)), function(j) {
  summary(lm(y ~ g[, j]))$coefficients[2, 1:2]
}))
gwas_fit <- sumstats(y_gwas, g_gwas)

# eQTL statistics deliberately come from a separate near-identity-LD panel.
g_eqtl_bad <- scale(matrix(rnorm(n * m), n, m))
y_eqtl_bad <- .55 * g_eqtl_bad[, causal] + rnorm(n)
eqtl_fit <- sumstats(y_eqtl_bad, g_eqtl_bad)
ld <- cor(g_gwas)
rownames(ld) <- snp
colnames(ld) <- snp
gwas <- data.frame(SNP = snp, CHR = 1L, POS = pos, BETA = gwas_fit[, 1], SE = gwas_fit[, 2])
eqtl <- data.frame(SNP = snp, CHR = 1L, POS = pos, BETA = eqtl_fit[, 1], SE = eqtl_fit[, 2])
lambda_bad <- susieR::estimate_s_rss(eqtl$BETA / eqtl$SE, ld, n = n)
stopifnot(lambda_bad > .05)
write.table(gwas, file.path(outdir, "gwas.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
write.table(eqtl, file.path(outdir, "eqtl.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
write.table(cbind(SNP = snp, ld), file.path(outdir, "ld.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
cat(sprintf("FRESH_EQTL_LAMBDA_WITH_WRONG_LD=%.6f\n", lambda_bad))
