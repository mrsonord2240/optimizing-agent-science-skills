# SILAC ratios from MaxQuant
silac <- read.delim('proteinGroups.txt')
ratio_cols <- grep('Ratio.H.L.normalized', colnames(silac), value = TRUE)

# Log2 transform ratios
silac_log2 <- log2(silac[, ratio_cols])

# One-sample t-test against 0 (no change)
results <- apply(silac_log2, 1, function(x) t.test(x, mu = 0)$p.value)
