# Input 3 (Edge): "In G11 we expect both gain- and loss-of-function missense variants, and in G21 only the
# truncating variants should matter. Burden or SKAT? And which mask?" SYNTHETIC data.
suppressMessages(library(SKAT))
covar_df <- read.delim("../../data/covar_skat.tsv"); covar_df$phenotype <- covar_df$Y
obj <- SKAT_Null_Model(phenotype ~ age + sex + PC1 + PC2, out_type = 'D', data = covar_df)
run3 <- function(Z) {
  c(burden = SKAT(Z, obj, r.corr = 1, weights.beta = c(1, 25))$p.value,
    skat = SKAT(Z, obj, weights.beta = c(1, 25))$p.value,
    skato = SKAT(Z, obj, method = 'SKATO', weights.beta = c(1, 25))$p.value)
}
masked <- function(g, keep) {
  Z <- as.matrix(read.delim(sprintf("../../data/gene_%s.tsv", g), check.names = FALSE))
  anno <- sub(".*\\|", "", colnames(Z))
  Z[, anno %in% keep, drop = FALSE]
}
for (g in c("G11", "G21", "G01")) {
  for (m in list(c("LoF"), c("LoF", "missense"), c("LoF", "missense", "synonymous"))) {
    Z <- masked(g, m)
    p <- run3(Z)
    cat(sprintf("%s mask=%-26s nvar=%2d burden=%.2e skat=%.2e skato=%.2e\n", g, paste(m, collapse = "+"), ncol(Z), p[1], p[2], p[3]))
  }
}
# per-variant direction in G11 missense (marginal log-OR sign from carrier case fraction)
Z <- masked("G11", "missense")
y <- covar_df$phenotype
cat("\nG11 missense carriers: case fraction per variant (overall", round(mean(y), 3), ")\n")
print(round(apply(Z, 2, function(z) if (sum(z > 0) > 0) mean(y[z > 0]) else NA), 3))
