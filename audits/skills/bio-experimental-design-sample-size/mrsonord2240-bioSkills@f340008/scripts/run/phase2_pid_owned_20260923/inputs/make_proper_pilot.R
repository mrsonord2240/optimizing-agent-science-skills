set.seed(20260923)
ngenes <- 240L
nsamples <- 8L
base_mu <- exp(rnorm(ngenes, log(150), 0.55))
disp <- 0.20
condition <- rep(c("A", "B"), each = nsamples / 2)
mat <- sapply(seq_len(nsamples), function(j) {
  fc <- ifelse(condition[j] == "B", c(rep(1.5, 24L), rep(1, ngenes - 24L)), 1)
  rnbinom(ngenes, mu = base_mu * fc, size = 1 / disp)
})
colnames(mat) <- paste0(condition, "_", ave(condition, condition, FUN = seq_along))
rownames(mat) <- sprintf("Gene%03d", seq_len(ngenes))
out <- commandArgs(trailingOnly = TRUE)[1]
write.csv(mat, out, quote = FALSE)
stopifnot(file.exists(out), nrow(read.csv(out, row.names = 1, check.names = FALSE)) == ngenes)
cat(sprintf("OK synthetic PROPER pilot: %d genes x %d samples written\n", ngenes, nsamples))
