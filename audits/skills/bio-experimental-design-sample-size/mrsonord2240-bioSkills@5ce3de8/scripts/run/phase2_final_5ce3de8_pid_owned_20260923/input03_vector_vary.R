suppressPackageStartupMessages({library(DESeq2); library(ssizeRNA)})
set.seed(20260923)
ngenes <- 240L
condition <- factor(rep(c("control", "treated"), each = 4))
base_mu <- rgamma(ngenes, shape = 5, rate = 0.04)
counts_mat <- sapply(seq_along(condition), function(i) {
  de <- seq_len(ngenes) <= 24L & condition[i] == "treated"
  rnbinom(ngenes, mu = base_mu * ifelse(de, 1.5, 1), size = 1 / 0.10)
})
rownames(counts_mat) <- paste0("g", seq_len(ngenes))
colnames(counts_mat) <- paste0("s", seq_len(ncol(counts_mat)))
dds <- DESeqDataSetFromMatrix(round(counts_mat), data.frame(condition), ~ condition)
dds <- DESeq(dds, quiet = TRUE)
mu_vec <- rowMeans(counts(dds, normalized = TRUE))
disp_vec <- dispersions(dds)
keep <- is.finite(mu_vec) & mu_vec > 0 & is.finite(disp_vec) & disp_vec > 0
mu_vec <- mu_vec[keep]
disp_vec <- disp_vec[keep]
res <- ssizeRNA_vary(nGenes = length(mu_vec), pi0 = 0.95, mu = mu_vec, disp = disp_vec,
                     fc = 1.5, fdr = 0.05, power = 0.80, maxN = 200)
n <- res$ssize[, "ssize"]
stopifnot(length(n) == 1L, is.finite(n), n >= 2, n <= 200)
cat(sprintf("OK DESeq2-pilot vector n=%d achieved_power=%.3f genes=%d\n", n, res$ssize[, "power"], length(mu_vec)))
