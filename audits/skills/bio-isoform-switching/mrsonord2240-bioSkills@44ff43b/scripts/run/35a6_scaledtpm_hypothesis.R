# Why does ISAR's default (scaledTPM-derived) counts route give q = 1 for RPL10 on real chrX 2v2? Test: non-integer counts?
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R")
suppressPackageStartupMessages({ library(IsoformSwitchAnalyzeR) })
PD <- "F:/OpenScience/audit-envs/alternative-splicing/public-data"
file.copy(file.path(PD, "rnasplice/reference/genes_chrX.gtf"), "annotation.gtf", overwrite = TRUE); file.copy(file.path(PD, "derived/chrX_tx.fa"), "transcripts.fa", overwrite = TRUE)
sm <- c("ERR188383", "ERR188428", "ERR188454", "ERR204916"); design <- data.frame(sampleID = sm, condition = c("GBR", "GBR", "YRI", "YRI"))
sq <- suppressMessages(importIsoformExpression(parentDir = "real_salmon/", addIsofomIdAsColumn = TRUE, showProgress = FALSE, quiet = TRUE))
cat("fraction of scaledTPM counts that are non-integer:", mean(as.matrix(sq$counts[, sm]) %% 1 != 0), "\n")
run <- function(cnt, label) { sl <- suppressWarnings(importRdata(cnt, sq$abundance, design, "annotation.gtf", "transcripts.fa", showProgress = FALSE, quiet = TRUE))
  sl <- preFilter(sl, geneExpressionCutoff = 1, isoformExpressionCutoff = 0, removeSingleIsoformGenes = TRUE, quiet = TRUE)
  sl <- isoformSwitchTestDEXSeq(sl, reduceToSwitchingGenes = FALSE, alpha = 0.05, dIFcutoff = 0.1, quiet = TRUE); f <- sl$isoformFeatures
  r <- f[f$isoform_id == "ENST00000406022", ]; cat(sprintf("%-40s sig isoforms %d | RPL10 q %.2g | tested genes %d | genes with gene_switch_q<0.05: %d\n", label, sum(f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1, na.rm = TRUE), r$isoform_switch_q_value, length(unique(f$gene_id)), length(unique(f$gene_id[which(f$gene_switch_q_value < 0.05)])))) }
cn <- sq$counts; run(cn, "default scaledTPM counts")
cr <- cn; cr[, sm] <- round(cr[, sm]); run(cr, "rounded to integers")
# scale down so the total equals raw library size ? already equal. Try multiplying counts x1 (identity) with abundance-based counts w/o TMM
