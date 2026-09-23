# Fresh Phase 2 input 10 assertions for scripts/commonfactor_gwas_qsnp.R output.
out <- read.delim("input10_helper_output.tsv", check.names = FALSE)
required <- c("SNP", "Pval_Estimate", "Q_pval", "Q_pval_ML", "factor_only_dwls", "factor_only")
stopifnot(nrow(out) == 20L, all(required %in% names(out)), length(unique(out$SNP)) == 20L)
stopifnot(all(is.finite(out$Q_pval)), all(is.finite(out$Q_pval_ML)))
stopifnot(is.logical(out$factor_only_dwls), is.logical(out$factor_only))
cat(sprintf("INPUT10 helper output parsed: rows=%d required_columns=PASS unique_snps=PASS finite_q=PASS factor_only=%d\\n", nrow(out), sum(out$factor_only)))
