# Input 5 (stress/triangulation): after TWAS flags GENE1 (planted true signal, rs637471,
# GWAS Z=6.5, S-PrediXcan/FUSION both verified above), the Skill's own triangulation guidance
# says a TWAS hit alone is not causal evidence and should be triangulated with cis-eQTL MR
# and colocalization. This checks the coloc.abf step of that documented pipeline with a
# realistic planted-shared-causal-variant scenario at the SORT1-style locus pattern the
# Skill's usage-guide references.
suppressMessages(library(coloc))

set.seed(20260919)
n_snp <- 50
maf <- runif(n_snp, 0.05, 0.5)
# Shared causal SNP at index 10 for both GWAS and eQTL (colocalization = TRUE scenario).
causal_idx <- 10
beta_gwas <- rnorm(n_snp, 0, 0.02); beta_gwas[causal_idx] <- 0.15
beta_eqtl <- rnorm(n_snp, 0, 0.05); beta_eqtl[causal_idx] <- 0.40
se_gwas <- rep(0.02, n_snp)
se_eqtl <- rep(0.05, n_snp)

dataset1 <- list(beta = beta_gwas, varbeta = se_gwas^2, N = 100000, type = "quant", MAF = maf, snp = paste0("rs", 1:n_snp))
dataset2 <- list(beta = beta_eqtl, varbeta = se_eqtl^2, N = 500, type = "quant", MAF = maf, snp = paste0("rs", 1:n_snp))

res <- coloc.abf(dataset1 = dataset1, dataset2 = dataset2)
print(res$summary)
cat("\nTop SNP by PP4 (H4 = shared causal variant):\n")
print(head(res$results[order(-res$results$SNP.PP.H4), c("snp","SNP.PP.H4")], 3))
