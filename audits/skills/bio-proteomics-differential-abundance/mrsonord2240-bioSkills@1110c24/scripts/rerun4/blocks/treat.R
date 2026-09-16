LFC_THRESHOLD <- log2(1.2)  # 1.2-fold floor; treat tests against this null, no double-filter FDR inflation
fit_treat <- treat(fit2, lfc = LFC_THRESHOLD, trend = TRUE, robust = TRUE)  # treat's trend/robust default to FALSE
results <- topTreat(fit_treat, coef = 1, number = Inf)  # topTreat omits the B column
