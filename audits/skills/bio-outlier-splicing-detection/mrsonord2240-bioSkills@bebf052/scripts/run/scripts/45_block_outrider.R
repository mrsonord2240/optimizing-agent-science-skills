# Run the SKILL.md OUTRIDER block VERBATIM (blocks/02_r.R) from a dir holding counts.tsv, then score vs planted truth.
# usage: Rscript 45_block_outrider.R <dir with counts.tsv + outrider_truth.tsv> <blockfile>
a <- commandArgs(TRUE); setwd(a[1]); blockf <- a[2]
suppressPackageStartupMessages({library(OUTRIDER); library(BiocParallel)})
cat("OUTRIDER", as.character(packageVersion("OUTRIDER")), "\n")
source(blockf, echo = FALSE)
truth <- read.delim("outrider_truth.tsv", stringsAsFactors = FALSE)
cat("q_best =", q_best, "; ods dims", dim(ods), "; total calls:", nrow(res), "\n")
key <- paste(res$sampleID, res$geneID); tk <- paste(truth$sample, truth$gene)
hit <- tk %in% key
for (i in seq_len(nrow(truth))) cat(sprintf("  %s %s x%.2f: %s\n", truth$sample[i], truth$gene[i], truth$fold[i], if (hit[i]) "DETECTED" else "not detected"))
cat(sprintf("RESULT detected %d/%d planted; false calls (not planted) %d\n", sum(hit), nrow(truth), sum(!(key %in% tk))))
stopifnot(is.numeric(q_best), q_best > 1)
