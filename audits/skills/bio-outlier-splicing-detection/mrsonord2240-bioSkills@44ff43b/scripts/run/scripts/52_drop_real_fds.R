# REAL data: DROP-demo FRASER fit (10 real chr21 RNA-seq BAMs + 2 external count samples). Pull results with the Skill's cutoffs.
suppressPackageStartupMessages({library(FRASER)})
d <- "drop_demo/Output/processed_results/aberrant_splicing/datasets/savedObjects"
fds <- loadFraserDataSet(dir = "drop_demo/Output/processed_results/aberrant_splicing/datasets", name = "fraser--v29")
cat("FRASER", as.character(packageVersion("FRASER")), "| samples:", ncol(fds), "| junctions:", nrow(fds), "| fitMetrics:", paste(fitMetrics(fds), collapse=","), "| bestQ(jaccard):", tryCatch(bestQ(fds, "jaccard"), error=function(e) NA), "\n")
res <- results(fds, psiType = "jaccard", padjCutoff = 0.05, deltaPsiCutoff = 0.1)
cat("Skill cutoffs (padj<0.05, |dPsi|>=0.1): ", length(res), "junction-sample calls in", length(unique(res$sampleID)), "of", ncol(fds), "samples\n")
print(table(res$sampleID))
r <- as.data.frame(res)[, c("seqnames","start","end","sampleID","hgncSymbol","padjust","deltaPsi","counts","totalCounts")]
print(head(r[order(r$padjust), ], 8))
cat("columns from results():", paste(colnames(as.data.frame(res)), collapse=","), "\n")
