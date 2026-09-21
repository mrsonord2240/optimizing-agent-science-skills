# INPUT 7E (NEW): real chrX 2v2, the three possible 2v2 label splits. Split 1 = GBR v YRI (the biology); splits 2 and 3 mix populations (no population signal),
# so calls there are individual-level differences / dispersion under-estimation at n=2. Both count routes, ISAR DEXSeq wrapper (Skill settings).
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
sm <- c("ERR188383", "ERR188428", "ERR188454", "ERR204916"); wd <- "w7c"
splits <- list(true_GBR_v_YRI = c("A", "A", "B", "B"), mixed1 = c("A", "B", "A", "B"), mixed2 = c("A", "B", "B", "A"))
a <- suppressMessages(importIsoformExpression(file.path(wd, "salmon_quant"), addIsofomIdAsColumn = TRUE, calculateCountsFromAbundance = FALSE, showProgress = FALSE, quiet = TRUE))
d <- suppressMessages(importIsoformExpression(file.path(wd, "salmon_quant"), addIsofomIdAsColumn = TRUE, calculateCountsFromAbundance = TRUE, showProgress = FALSE, quiet = TRUE))
res <- list()
for (sp in names(splits)) for (rt in c("raw", "default")) {
  imp <- if (rt == "raw") a else d; des <- data.frame(sampleID = sm, condition = splits[[sp]])
  sl <- suppressWarnings(importRdata(imp$counts, imp$abundance, des, file.path(wd, "annotation.gtf"), file.path(wd, "transcripts.fa"), showProgress = FALSE, quiet = TRUE))
  sl <- preFilter(sl, geneExpressionCutoff = 1, isoformExpressionCutoff = 0, IFcutoff = 0.01, removeSingleIsoformGenes = TRUE, keepIsoformInAllConditions = TRUE, quiet = TRUE)
  sl <- isoformSwitchTestDEXSeq(sl, reduceToSwitchingGenes = FALSE, alpha = 0.05, dIFcutoff = 0.1, quiet = TRUE)
  f <- sl$isoformFeatures; s <- f[!is.na(f$isoform_switch_q_value) & f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1, ]
  res[[paste(sp, rt)]] <- unique(s$gene_id)
  cat(sprintf("%-16s %-8s %3d isoforms / %2d genes | min isoform q %.3g\n", sp, rt, nrow(s), length(unique(s$gene_id)), min(f$isoform_switch_q_value, na.rm = TRUE))) }
tr <- res[["true_GBR_v_YRI raw"]]
cat("raw-route genes of the true split also called in a mixed split:", paste(sapply(c("mixed1", "mixed2"), function(m) sprintf("%s %d/%d", m, length(intersect(tr, res[[paste(m, "raw")]])), length(tr))), collapse = "; "), "\n")
cat("DONE 71\n")
