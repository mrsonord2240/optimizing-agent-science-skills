suppressPackageStartupMessages(library(OUTRIDER))
d <- commandArgs(TRUE)[1]
cnt <- read.table(file.path(d, "counts.tsv"), header = TRUE, row.names = 1); truth <- read.delim(file.path(d, "outrider_truth.tsv"))
for (i in 1:nrow(truth)) cat(truth$gene[i], truth$sample[i], "count", cnt[truth$gene[i], truth$sample[i]], " row median", median(unlist(cnt[truth$gene[i], ])), " row max", max(unlist(cnt[truth$gene[i], ])), "\n")
ods <- OutriderDataSet(countData = cnt); ods <- filterExpression(ods, minCounts = TRUE, filterGenes = TRUE)
ods <- OUTRIDER(ods, q = 8, BPPARAM = SerialParam())
r <- results(ods, padjCutoff = 1, zScoreCutoff = 0, all = TRUE)
k <- paste(r$sampleID, r$geneID); for (i in 1:nrow(truth)) { x <- r[k == paste(truth$sample[i], truth$gene[i]), ]; cat(truth$gene[i], "z", round(x$zScore, 2), "p", signif(x$pValue, 3), "padj", signif(x$padjust, 3), "\n") }
cat("min padj overall:", min(r$padjust), " n p<1e-4:", sum(r$pValue < 1e-4), "\n")
