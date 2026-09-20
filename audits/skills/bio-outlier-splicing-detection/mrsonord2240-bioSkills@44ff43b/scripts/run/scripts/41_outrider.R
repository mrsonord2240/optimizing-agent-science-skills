# The Skill's SKILL.md OUTRIDER block on the synthetic count matrix; scored against planted truth.
# Usage: Rscript 41_outrider.R <data_dir> <n_samples> [ncpu]
suppressPackageStartupMessages({library(OUTRIDER); library(BiocParallel)})
a <- commandArgs(TRUE); d <- a[1]; n <- as.integer(a[2]); ncpu <- if (length(a) >= 3) as.integer(a[3]) else 8
cat("OUTRIDER", as.character(packageVersion("OUTRIDER")), "n =", n, "\n")
countTable <- read.table(file.path(d, "counts.tsv"), header = TRUE, row.names = 1)
truth <- read.delim(file.path(d, "outrider_truth.tsv"), stringsAsFactors = FALSE)
if (n < ncol(countTable)) {          # keep all planted-outlier samples that fit; drop others first
  keep <- unique(c(truth$sample, colnames(countTable))); keep <- keep[seq_len(n)]; countTable <- countTable[, keep]
  truth <- truth[truth$sample %in% keep, ]
}
cat("counts:", dim(countTable), "; planted outliers present:", nrow(truth), "\n")
# ---- verbatim from SKILL.md ----
ods <- OutriderDataSet(countData = countTable)
ods <- filterExpression(ods, minCounts = TRUE, filterGenes = TRUE)
q_best <- estimateBestQ(ods)
cat("estimateBestQ returned class:", class(q_best), " value:", if (is.numeric(q_best)) q_best else "<object>", "\n")
ods <- OUTRIDER(ods, q = q_best, BPPARAM = if (.Platform$OS.type == "windows") SerialParam() else MulticoreParam(ncpu))
res <- results(ods, padjCutoff = 0.05, zScoreCutoff = 0)
# --------------------------------
cat("result columns:", paste(colnames(res), collapse = ", "), "\n"); cat("total calls padj<0.05:", nrow(res), "\n")
key <- paste(res$sampleID, res$geneID); tk <- paste(truth$sample, truth$gene)
for (i in seq_len(nrow(truth))) { r <- res[key == tk[i], ]; cat(sprintf("  %s %s x%.2f: %s\n", truth$sample[i], truth$gene[i], truth$fold[i],
   if (nrow(r)) sprintf("DETECTED padj=%.1e z=%.2f", r$padjust[1], r$zScore[1]) else "not detected")) }
fp <- res[!(key %in% tk), ]
cat(sprintf("detected %d/%d planted; non-planted calls: %d (of %d gene-sample tests => rate %.2e)\n", sum(tk %in% key), nrow(truth), nrow(fp), nrow(ods) * ncol(ods), nrow(fp) / (nrow(ods) * ncol(ods))))
cat("Skill's quality-threshold row 'OUTRIDER zScore abs >= 2 (conservative)': calls with |z|<2 at padj<0.05 :", sum(abs(res$zScore) < 2), "\n")
