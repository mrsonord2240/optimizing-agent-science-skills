library(DEqMS)

# fit2 is the limma fit through eBayes (above), after the valid-value filter
stopifnot(all(fit2$df.residual > 0))  # NA-sigma rows make spectraCounteBayes recycle loess predictions onto the wrong proteins
fit2$count <- psm_count_per_protein[rownames(fit2$coefficients)]  # PSM for TMT, peptide for LFQ; min across batches
fit3 <- spectraCounteBayes(fit2)

results <- outputResult(fit3, coef_col = 1)
# adds sca.t, sca.P.Value, sca.adj.pval (the count-adjusted statistics; use these, not the limma columns)
