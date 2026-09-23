# Independent matched-LD positive control for the corrected coloc.susie CLI.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1) stop("usage: input12_make_fresh_matched_locus.R <outdir>")
outdir <- args[[1]]
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)

set.seed(2026092212)
n <- 2200L
m <- 140L
causal <- 42L
snp <- sprintf("rs%d", seq_len(m))
pos <- seq.int(46000000L, by = 900L, length.out = m)
R0 <- .63^abs(outer(seq_len(m), seq_len(m), "-"))
g <- scale(matrix(rnorm(n * m), n, m) %*% chol(R0))
sumstats <- function(y) do.call(rbind, lapply(seq_len(m), function(j) {
  summary(lm(y ~ g[, j]))$coefficients[2, 1:2]
}))
y_gwas <- .38 * g[, causal] + rnorm(n)
y_eqtl <- .51 * g[, causal] + rnorm(n)
gwas_fit <- sumstats(y_gwas)
eqtl_fit <- sumstats(y_eqtl)
ld <- cor(g)
rownames(ld) <- snp
colnames(ld) <- snp
gwas <- data.frame(SNP = snp, CHR = 1L, POS = pos, BETA = gwas_fit[, 1], SE = gwas_fit[, 2])
eqtl <- data.frame(SNP = snp, CHR = 1L, POS = pos, BETA = eqtl_fit[, 1], SE = eqtl_fit[, 2])
lambda_gwas <- susieR::estimate_s_rss(gwas$BETA / gwas$SE, ld, n = n)
lambda_eqtl <- susieR::estimate_s_rss(eqtl$BETA / eqtl$SE, ld, n = n)
stopifnot(lambda_gwas <= .05, lambda_eqtl <= .05)
write.table(gwas, file.path(outdir, "gwas.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
write.table(eqtl, file.path(outdir, "eqtl.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
write.table(cbind(SNP = snp, ld), file.path(outdir, "ld.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
cat(sprintf("FRESH_MATCHED_PLANTED_SHARED=rs%d\n", causal))
cat(sprintf("FRESH_MATCHED_LAMBDAS=%.6f,%.6f\n", lambda_gwas, lambda_eqtl))
