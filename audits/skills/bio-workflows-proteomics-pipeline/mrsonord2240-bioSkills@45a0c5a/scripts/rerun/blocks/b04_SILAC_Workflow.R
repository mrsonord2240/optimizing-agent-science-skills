library(limma)

# SILAC ratios from MaxQuant (quote/comment.char as in the MSstats block above)
silac <- read.delim('proteinGroups.txt', quote = '', comment.char = '')
ratio_cols <- grep('Ratio.H.L.normalized', colnames(silac), value = TRUE)

# Log2 transform ratios. MaxQuant leaves NaN (and 0 for an absent channel) wherever it could not
# form a ratio, so log2 produces NaN/-Inf; coerce every non-finite cell to NA before testing.
silac_log2 <- log2(as.matrix(silac[, ratio_cols]))
silac_log2[!is.finite(silac_log2)] <- NA
rownames(silac_log2) <- silac$Majority.protein.IDs   # without this the result table has no identity

# Keep proteins with >= 2 finite ratios. apply(t.test) over the raw matrix STOPS the whole script
# with "not enough 'x' observations" on the first protein quantified in one replicate only.
keep <- rowSums(!is.na(silac_log2)) >= 2
cat('proteins tested:', sum(keep), 'of', nrow(silac_log2), '\n')

# One-sample moderated test against log2 ratio 0 (no change): an intercept-only limma fit borrows
# variance across proteins, which an unmoderated per-protein t-test at n = 3 cannot. Report the
# BH-adjusted p-value -- a raw p-value per protein controls nothing across thousands of tests.
fit <- eBayes(lmFit(silac_log2[keep, , drop = FALSE]), trend = TRUE, robust = TRUE)
results <- topTable(fit, coef = 1, number = Inf, adjust.method = 'BH')
# Proteins dropped by `keep` are an on/off presence table, not a fold change (quantification).
