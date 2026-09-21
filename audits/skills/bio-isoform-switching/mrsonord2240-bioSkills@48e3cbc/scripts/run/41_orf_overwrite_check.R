# Does the Skill's stated NMD-flag degradation after analyzeORF('longest') over annotated ORFs (sens 0.96/spec 1.00 -> 0.64/0.89) reproduce?
# Reference: Ensembl biotype. Tested on the UNFILTERED import (the fixer's 1738 isoforms) and on the filtered set.
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work/w3"); source("../../helpers.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
sm <- c("ERR188383", "ERR188428", "ERR188454", "ERR204916"); design <- data.frame(sampleID = sm, condition = c("GBR", "GBR", "YRI", "YRI"))
sq <- suppressMessages(importIsoformExpression("salmon_quant/", addIsofomIdAsColumn = TRUE, calculateCountsFromAbundance = FALSE, showProgress = FALSE, quiet = TRUE))
sl <- suppressWarnings(importRdata(sq$counts, sq$abundance, design, "annotation.gtf", "transcripts.fa", addAnnotatedORFs = TRUE, showProgress = FALSE, quiet = TRUE))
fl <- strsplit(readLines("annotation.gtf"), "\t", fixed = TRUE); bio <- tapply(vapply(fl, `[`, "", 2), vapply(fl, function(x) sub('.*transcript_id "([^"]+)".*', "\\1", x[9]), ""), function(x) x[1])
ev <- function(orf, label) {
  o <- orf[!is.na(orf$orf_origin), ]; o$b <- bio[o$isoform_id]; o <- o[o$b %in% c("nonsense_mediated_decay", "protein_coding"), ]
  t <- o$b == "nonsense_mediated_decay"; cl <- !is.na(o$PTC) & o$PTC == TRUE
  cat(sprintf("%-42s n=%4d NMD-biotype %2d | sens %.2f (%d/%d) spec %.2f (%d/%d) | %s\n", label, nrow(o), sum(t), sum(cl & t) / sum(t), sum(cl & t), sum(t), sum(!cl & !t) / sum(!t), sum(!cl & !t), sum(!t), paste(names(table(o$orf_origin)), table(o$orf_origin), collapse = ","))) }
cat("isoforms in import:", nrow(sl$isoformFeatures) / 1, "| orfAnalysis rows:", nrow(sl$orfAnalysis), "\n")
ev(sl$orfAnalysis, "unfiltered, annotated ORFs")
sl2 <- suppressWarnings(analyzeORF(sl, orfMethod = "longest", genomeObject = NULL, quiet = TRUE)); ev(sl2$orfAnalysis, "unfiltered, after analyzeORF('longest')")
sl3 <- preFilter(sl, geneExpressionCutoff = 1, isoformExpressionCutoff = 0, IFcutoff = 0.01, removeSingleIsoformGenes = TRUE, keepIsoformInAllConditions = TRUE, quiet = TRUE)
ev(sl3$orfAnalysis, "prefiltered, annotated ORFs")
sl4 <- suppressWarnings(analyzeORF(sl3, orfMethod = "longest", genomeObject = NULL, quiet = TRUE)); ev(sl4$orfAnalysis, "prefiltered, after analyzeORF('longest')")
cat("orf_origin after analyzeORF (unfiltered):", paste(names(table(sl2$orfAnalysis$orf_origin)), table(sl2$orfAnalysis$orf_origin)), "\n")
cat("DONE 41\n")
