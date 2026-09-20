# why does the shipped example's isoformSwitchTestDEXSeq(reduceToSwitchingGenes = TRUE) stop on real chrX 2v2?
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
source("../skill/examples/isoform_switch_analysis.R", echo = FALSE)
design <- data.frame(sampleID = c("ERR188383", "ERR188428", "ERR188454", "ERR204916"), condition = c("GBR", "GBR", "YRI", "YRI"))
sl <- suppressWarnings(import_salmon_data("real_salmon/", design))
sl <- preFilter(sl, geneExpressionCutoff = 1, isoformExpressionCutoff = 0, removeSingleIsoformGenes = TRUE, quiet = TRUE)
tryit <- function(label, ...) { r <- tryCatch({ x <- isoformSwitchTestDEXSeq(sl, quiet = TRUE, ...); f <- x$isoformFeatures; paste("ok:", length(unique(f$gene_id)), "genes kept;", sum(f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1, na.rm = TRUE), "sig isoforms") }, error = function(e) paste("ERROR:", conditionMessage(e))); cat(sprintf("%-75s %s\n", label, r)) }
tryit("reduceToSwitchingGenes=TRUE (example call; defaults otherwise)", reduceToSwitchingGenes = TRUE)
tryit("reduceToSwitchingGenes=TRUE, reduceFurtherToGenesWithConsequencePotential=FALSE", reduceToSwitchingGenes = TRUE, reduceFurtherToGenesWithConsequencePotential = FALSE)
tryit("reduceToSwitchingGenes=FALSE", reduceToSwitchingGenes = FALSE)
tryit("reduceToSwitchingGenes=TRUE, keepIsoformInAllConditions=FALSE", reduceToSwitchingGenes = TRUE, keepIsoformInAllConditions = FALSE)
tryit("reduceToSwitchingGenes=TRUE, onlySigIsoforms=FALSE, dIFcutoff=0.05", reduceToSwitchingGenes = TRUE, dIFcutoff = 0.05)
x <- isoformSwitchTestDEXSeq(sl, reduceToSwitchingGenes = FALSE, quiet = TRUE); f <- x$isoformFeatures
cat("without reduction: sig isoforms (q<0.05 & |dIF|>0.1):", sum(f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1, na.rm = TRUE), "; isoforms with dIF>0.1 & q<0.05 that have an opposing isoform (dIF<-0.1) in the same gene:",
    { s <- f[which(f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1), ]; g <- unique(s$gene_id); sum(sapply(g, function(gg) { d <- f$dIF[f$gene_id == gg]; any(d > 0.1) && any(d < -0.1) })) }, "genes\n")
