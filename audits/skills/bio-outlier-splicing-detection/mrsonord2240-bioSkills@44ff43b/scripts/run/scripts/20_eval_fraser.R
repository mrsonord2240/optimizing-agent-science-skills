# Evaluate FRASER results against the PLANTED truth (synthetic cohort). Usage: Rscript 20_eval_fraser.R <workdir> <name> <synth_dir> [delta] [padj]
# Loads the fds that the Skill's workflow saved, pulls results for ALL samples, scores them against planted_truth.tsv.
suppressPackageStartupMessages({library(FRASER); library(GenomicRanges)})
args <- commandArgs(TRUE); wd <- args[1]; nm <- args[2]; synth <- args[3]
delta <- if (length(args) >= 4) as.numeric(args[4]) else 0.1
padj  <- if (length(args) >= 5) as.numeric(args[5]) else 0.05
fds <- loadFraserDataSet(dir = wd, name = nm)
cat("FRASER", as.character(packageVersion("FRASER")), " samples:", ncol(fds), " current type:", currentType(fds), "\n")
cat("fitMetrics:", paste(fitMetrics(fds), collapse=","), "\n")
cat("junctions total:", nrow(fds), " passed filter:", sum(mcols(fds, type="j")[["passed"]]), "\n")
res <- results(fds, psiType = "jaccard", padjCutoff = padj, deltaPsiCutoff = delta)
cat("result columns:", paste(colnames(mcols(res)), collapse=", "), "\n")
cat("total significant junction-sample calls:", length(res), "\n")
truth <- read.delim(file.path(synth, "planted_truth.tsv"), stringsAsFactors = FALSE)
genes <- read.delim(file.path(synth, "genes.tsv"), stringsAsFactors = FALSE)
gr_genes <- GRanges(genes$chrom, IRanges(genes$start, genes$end), gene = genes$gene)
# S05 was renamed to PATIENT_001 by the Skill's example layout
sid <- as.character(res$sampleID); sid[sid == "PATIENT_001"] <- "S05"
res$sample <- sid
hit_gene <- rep(NA_character_, length(res))
ov <- findOverlaps(res, gr_genes); hit_gene[queryHits(ov)] <- gr_genes$gene[subjectHits(ov)]
res$gene <- hit_gene
cat("\n== per-planted-splicing-event detection (padj<", padj, ", |dPsi|>=", delta, ") ==\n", sep = "")
for (i in seq_len(nrow(truth))) {
  t <- truth[i, ]
  h <- res[res$sample == t$sample & !is.na(res$gene) & res$gene == t$gene]
  cat(sprintf("%-4s %-4s %-17s : %s", t$sample, t$gene, t$type, if (length(h)) sprintf("DETECTED n=%d min_padj=%.2e max|dPsi|=%.2f", length(h), min(h$padjust), max(abs(h$deltaPsi))) else "not detected"), "\n")
}
cat("\n== calls per sample (all) ==\n")
tab <- table(res$sample); print(tab[order(-tab)])
planted_pairs <- paste(truth$sample, truth$gene)
is_planted <- paste(res$sample, res$gene) %in% planted_pairs
fp <- res[!is_planted & res$sample != "S29"]
cat("\nnon-planted calls excluding tissue-mismatch S29:", length(fp), " in ", length(unique(fp$sample)), " samples, ", length(unique(paste(fp$sample, fp$gene))), " sample-gene pairs\n", sep = "")
cat("S29 (tissue-mismatch) calls:", sum(res$sample == "S29"), " distinct genes:", length(unique(res$gene[res$sample == "S29"])), "\n")
tested <- sum(mcols(fds, type="j")[["passed"]]) * ncol(fds)
cat("tested junction-sample pairs (passed filter x samples):", tested, "; per-pair FP rate for non-planted calls:", signif(length(fp) / tested, 3), "\n")
cat("non-planted genes hit by a non-S29 call:", length(unique(fp$gene)), " of ", nrow(genes), " genes\n")
write.table(as.data.frame(res), file.path(wd, "all_results_annotated.tsv"), sep = "\t", quote = FALSE, row.names = FALSE)
print(head(as.data.frame(fp)[, c("sample", "gene", "start", "end", "padjust", "deltaPsi", "counts", "totalCounts")], 15))
