library(ashr)

ok <- !is.na(fit2$coefficients[, 1]) & !is.na(fit2$s2.post)  # ash() returns PosteriorMean 0 / prior lfsr for NA rows
se <- sqrt(fit2$s2.post[ok]) * fit2$stdev.unscaled[ok, 1]
shrunk <- ash(fit2$coefficients[ok, 1], se, mixcompdist = 'normal')
shrunken_fc <- shrunk$result$PosteriorMean  # report alongside raw logFC, not as a replacement for GSEA
lfsr <- shrunk$result$lfsr
