# Input 2 (Variant A): "Small case-control cohort: fit a SKAT null model on covariates and report burden, SKAT
# and SKAT-O p-values per gene with Beta(1,25) MAF weighting." SYNTHETIC data (data/make_rv_data.py).
# SKILL.md block verbatim inside the loop; only data loading is added.
suppressMessages(library(SKAT))
cat("SKAT", as.character(packageVersion("SKAT")), "\n")
covar_df <- read.delim("../../data/covar_skat.tsv")
covar_df$phenotype <- covar_df$Y
cat("n =", nrow(covar_df), " cases =", sum(covar_df$phenotype), "\n")

# Null model on covariates only (out_type='D' binary, 'C' continuous). Refit once, reuse per gene.
obj <- SKAT_Null_Model(phenotype ~ age + sex + PC1 + PC2, out_type = 'D', data = covar_df)

genes <- sprintf("G%02d", 1:30)
res <- data.frame()
for (g in genes) {
  Z <- as.matrix(read.delim(sprintf("../../data/gene_%s.tsv", g), check.names = FALSE))
  skato <- SKAT(Z, obj, method = 'SKATO', weights.beta = c(1, 25))
  burden <- SKAT(Z, obj, r.corr = 1, weights.beta = c(1, 25))
  skat <- SKAT(Z, obj, weights.beta = c(1, 25))
  p <- c(skato = skato$p.value, burden = burden$p.value, skat = skat$p.value)
  res <- rbind(res, data.frame(gene = g, n_var = ncol(Z), skato = p[["skato"]], burden = p[["burden"]], skat = p[["skat"]]))
}
res$min_p <- pmin(res$skato, res$burden, res$skat)
print(format(res[order(res$min_p), ], digits = 3), row.names = FALSE)
cat("\nBonferroni over 30 genes x 3 tests: 0.05/90 =", signif(0.05 / 90, 3), "\n")
cat("null genes with any p < 0.05:", sum(res$min_p[!res$gene %in% c("G01", "G11", "G21")] < 0.05), "of 27\n")
write.table(res, "skat_results.tsv", sep = "\t", quote = FALSE, row.names = FALSE)
