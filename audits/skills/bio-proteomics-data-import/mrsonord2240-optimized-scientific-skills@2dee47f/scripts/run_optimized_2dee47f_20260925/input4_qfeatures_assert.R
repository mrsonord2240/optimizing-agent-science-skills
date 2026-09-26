# Independent checks around the exact bundled QFeatures workflow.
suppressPackageStartupMessages(library(QFeatures))

args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 1L) stop('Usage: Rscript input4_qfeatures_assert.R proteinGroups.txt', call. = FALSE)
pg <- read.delim(args[[1]], quote = '', check.names = FALSE)
lfq <- grep('^LFQ intensity ', names(pg), value = TRUE)
stopifnot(length(lfq) > 0)
qf <- readQFeatures(pg, quantCols = lfq, name = 'proteinGroups')
rd <- rowData(qf[[1]])
colnames(rd) <- make.names(colnames(rd))
rowData(qf[[1]]) <- rd
qf <- filterFeatures(qf, ~ !(Reverse %in% '+') & !(Potential.contaminant %in% '+') & !(Only.identified.by.site %in% '+'))
qf <- zeroIsNA(qf, 1)
qf <- logTransform(qf, i = 1, name = 'log2LFQ')
mat <- assay(qf[['log2LFQ']])
all_missing <- sum(rowSums(!is.na(mat)) == 0L)
stopifnot(nrow(mat) == 1500L, ncol(mat) == 8L, !any(is.infinite(mat)), all_missing == 55L)
cat(sprintf('Independent QFeatures assertions: rows=%d samples=%d all-missing=%d -Inf=%s\n', nrow(mat), ncol(mat), all_missing, any(is.infinite(mat))))
