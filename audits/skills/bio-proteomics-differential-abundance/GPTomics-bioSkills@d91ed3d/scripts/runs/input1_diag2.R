source('F:/OpenScience/audits/bio-proteomics-differential-abundance/runs/common.R')
# Which rows trigger "prior.weights contain NA values" in eBayes(trend=TRUE)?
suppressPackageStartupMessages(library(limma))
sample_info <- read.csv(file.path(DATA, 'sample_annotation.csv'), stringsAsFactors = TRUE)
pg <- read_pg(); pm <- lfq_log2(pg, as.character(sample_info$sample))
design <- model.matrix(~0 + condition + batch, data = sample_info)
colnames(design)[1:2] <- levels(factor(sample_info$condition))
fit2 <- suppressWarnings(contrasts.fit(lmFit(pm, design), makeContrasts(Treatment - Control, levels = design)))
bad <- is.na(fit2$coefficients[, 1]); df <- fit2$df.residual
tst <- function(keep, lab) cat(sprintf('%-55s n=%4d : %s\n', lab, sum(keep),
  tryCatch({ eBayes(fit2[keep, ], trend = TRUE, robust = TRUE); 'OK' }, error = function(e) conditionMessage(e))))
tst(rep(TRUE, length(bad)), 'all rows')
tst(!(bad & df == 0), 'drop NA-contrast rows with df=0')
tst(!(bad & df > 0), 'drop NA-contrast rows with df>0')
tst(!bad, 'drop all NA-contrast rows')
tst(df > 0, 'drop df=0 rows (sigma NA)')
tst(!is.na(fit2$sigma), 'drop NA-sigma rows')
cat('NA-contrast rows by df:\n'); print(table(df[bad]))
cat('Amean NA among NA-contrast rows:', sum(is.na(fit2$Amean[bad])), '\n')
# one-sample check: is it the NA-contrast rows with df>0 whose sigma is non-NA but coefficient NA?
x <- which(bad & df > 0)[1]; print(pm[x, ]); cat('sigma', fit2$sigma[x], 'df', df[x], '\n')
allna <- rowSums(!is.na(pm)) == 0
cat('\nRows with NO LFQ value in any of the 8 runs:', sum(allna), '\n')
tst(!allna, 'drop only all-NA rows')
