# Count-vs-abundance handling on REAL chrX 2v2: Skill path (importIsoformExpression defaults: counts derived from TMM-normalised abundance = scaledTPM)
# vs tximport raw NumReads vs importIsoformExpression(calculateCountsFromAbundance=FALSE).
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R")
suppressPackageStartupMessages({ library(IsoformSwitchAnalyzeR); library(tximport) })
sm <- c("ERR188383", "ERR188428", "ERR188454", "ERR204916"); design <- data.frame(sampleID = sm, condition = c("GBR", "GBR", "YRI", "YRI"))
run <- function(cnt, ab, label) {
  sl <- suppressWarnings(importRdata(cnt, ab, design, "annotation.gtf", "transcripts.fa", showProgress = FALSE, quiet = TRUE))
  sl <- preFilter(sl, geneExpressionCutoff = 1, isoformExpressionCutoff = 0, removeSingleIsoformGenes = TRUE, quiet = TRUE)
  sl <- isoformSwitchTestDEXSeq(sl, reduceToSwitchingGenes = FALSE, alpha = 0.05, dIFcutoff = 0.1, quiet = TRUE)
  f <- sl$isoformFeatures; f <- f[!is.na(f$isoform_switch_q_value), ]
  cat(sprintf("%-58s genes tested %3d | isoforms q<0.05: %3d | q<0.05 & |dIF|>0.1: %3d | genes: %2d | lib sizes(sum counts) %s\n", label, length(unique(f$gene_id)), sum(f$isoform_switch_q_value < 0.05), sum(f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1),
      length(unique(f$gene_id[f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1])), paste(round(colSums(cnt[, -1])), collapse = "/")))
  invisible(sl) }
sq <- suppressMessages(importIsoformExpression(parentDir = "real_salmon/", addIsofomIdAsColumn = TRUE, showProgress = FALSE, quiet = TRUE))
run(sq$counts, sq$abundance, "Skill path: importIsoformExpression defaults (scaledTPM)")
sq2 <- suppressMessages(importIsoformExpression(parentDir = "real_salmon/", addIsofomIdAsColumn = TRUE, calculateCountsFromAbundance = FALSE, showProgress = FALSE, quiet = TRUE))
run(sq2$counts, sq2$abundance, "importIsoformExpression(calculateCountsFromAbundance=FALSE)")
sq3 <- suppressMessages(importIsoformExpression(parentDir = "real_salmon/", addIsofomIdAsColumn = TRUE, interLibNormTxPM = FALSE, showProgress = FALSE, quiet = TRUE))
run(sq3$counts, sq3$abundance, "importIsoformExpression(interLibNormTxPM=FALSE)")
txi <- tximport(setNames(file.path("real_salmon", sm, "quant.sf"), sm), type = "salmon", txOut = TRUE, countsFromAbundance = "no")
run(data.frame(isoform_id = rownames(txi$counts), txi$counts, check.names = FALSE), data.frame(isoform_id = rownames(txi$abundance), txi$abundance, check.names = FALSE), "tximport raw NumReads + raw TPM (Input 3 path)")
cat("corr(ISAR counts, raw NumReads) per sample:", paste(round(sapply(sm, function(s) cor(sq$counts[[s]], txi$counts[match(sq$counts$isoform_id, rownames(txi$counts)), s])), 4), collapse = " "), "\n")
# gene-level agreement of the two counts routes (ISAR-specific reduction is not used)
