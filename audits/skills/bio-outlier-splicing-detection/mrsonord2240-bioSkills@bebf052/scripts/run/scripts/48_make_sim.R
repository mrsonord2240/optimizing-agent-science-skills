# NEW input: counts from OUTRIDER's own simulator (makeExampleOutriderDataSet, 2000 genes, freq 1e-3, seed 42) written as counts.tsv + truth
suppressPackageStartupMessages(library(OUTRIDER))
a <- commandArgs(TRUE); m <- as.integer(a[1]); out <- a[2]
set.seed(42)
ods0 <- makeExampleOutriderDataSet(n = 2000, m = m, freq = 1e-3)
tr <- assay(ods0, "trueOutliers"); tk <- which(tr != 0, arr.ind = TRUE)
dir.create(out, showWarnings = FALSE, recursive = TRUE)
write.table(counts(ods0), file.path(out, "counts.tsv"), sep = "\t", quote = FALSE)
write.table(data.frame(gene = rownames(tr)[tk[, 1]], sample = colnames(tr)[tk[, 2]], fold = NA_real_), file.path(out, "outrider_truth.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
cat("m =", m, "; injected outliers:", nrow(tk), "\n")
