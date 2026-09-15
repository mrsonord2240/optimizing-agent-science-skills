.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Reference comparison for INPUT 4: limma trend+robust on the same 12v12 matrix, same median normalization and
# same >=2-per-group filter as the Skill's Python path (does moderation still matter at n=12?).
suppressPackageStartupMessages(library(limma))
D <- 'F:/OpenScience/audits/bio-proteomics-differential-abundance/data'
x <- as.matrix(read.csv(file.path(D, 'plasma_12v12.csv'), row.names = 1)); x <- log2(x)
x <- sweep(x, 2, apply(x, 2, median, na.rm = TRUE)) + median(apply(x, 2, median, na.rm = TRUE))
tru <- read.csv(file.path(D, 'plasma_truth.csv'), row.names = 1, na.strings = '')
g <- factor(ifelse(grepl('^case', colnames(x)), 'case', 'ctrl'), levels = c('ctrl', 'case'))
keep <- rowSums(!is.na(x[, g == 'case'])) >= 2 & rowSums(!is.na(x[, g == 'ctrl'])) >= 2
d <- model.matrix(~g); f <- eBayes(lmFit(x[keep, ], d), trend = TRUE, robust = TRUE)
tt <- topTable(f, coef = 2, number = Inf); s <- rownames(tt)[tt$adj.P.Val < 0.05]
cat(sprintf('limma trend+robust, n=12/group: tested %d, called %d, null %d (%.1f%%), TP %d/70; df.prior %.1f\n', sum(keep), length(s),
            sum(tru[s, 'class'] == 'null'), 100 * mean(tru[s, 'class'] == 'null'), sum(tru[s, 'class'] %in% c('up', 'down')), median(f$df.prior)))
