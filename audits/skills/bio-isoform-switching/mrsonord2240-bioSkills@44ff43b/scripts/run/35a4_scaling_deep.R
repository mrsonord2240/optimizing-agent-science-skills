setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R")
suppressPackageStartupMessages({ library(IsoformSwitchAnalyzeR); library(tximport) })
sm <- c("ERR188383", "ERR188428", "ERR188454", "ERR204916"); design <- data.frame(sampleID = sm, condition = c("GBR", "GBR", "YRI", "YRI"))
t2g <- read.delim("F:/OpenScience/audit-envs/alternative-splicing/public-data/rnasplice/salmon/genes_chrX.tx2gene.tsv", header = FALSE); colnames(t2g) <- c("tx", "gene")
files <- setNames(file.path("real_salmon", sm, "quant.sf"), sm)
sq <- suppressMessages(importIsoformExpression(parentDir = "real_salmon/", addIsofomIdAsColumn = TRUE, showProgress = FALSE, quiet = TRUE))
id <- sq$counts$isoform_id
run <- function(cnt, ab, label) {
  sl <- suppressWarnings(importRdata(cnt, ab, design, "annotation.gtf", "transcripts.fa", showProgress = FALSE, quiet = TRUE))
  sl <- preFilter(sl, geneExpressionCutoff = 1, isoformExpressionCutoff = 0, removeSingleIsoformGenes = TRUE, quiet = TRUE)
  sl <- isoformSwitchTestDEXSeq(sl, reduceToSwitchingGenes = FALSE, alpha = 0.05, dIFcutoff = 0.1, quiet = TRUE)
  f <- sl$isoformFeatures; f <- f[!is.na(f$isoform_switch_q_value), ]
  r <- f[f$gene_name == "RPL10" & f$isoform_id == "ENST00000406022", ]
  cat(sprintf("%-46s genes %3d | q<0.05&|dIF|>0.1 isoforms %3d genes %2d | RPL10 ENST00000406022 dIF %.3f q %.2g\n", label, length(unique(f$gene_id)), sum(f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1),
      length(unique(f$gene_id[f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1])), r$dIF, r$isoform_switch_q_value)) }
ab <- sq$abundance
run(sq$counts, ab, "ISAR default counts (from abundance)")
for (cfa in c("no", "scaledTPM", "lengthScaledTPM", "dtuScaledTPM")) {
  txi <- suppressMessages(tximport(files, type = "salmon", txOut = TRUE, countsFromAbundance = cfa, tx2gene = t2g))
  cn <- data.frame(isoform_id = id, txi$counts[id, ], check.names = FALSE)
  cat(sprintf("   cor(ISAR counts, tximport %s counts) = %s\n", cfa, paste(round(sapply(sm, function(s) cor(sq$counts[[s]], txi$counts[id, s])), 4), collapse = " ")))
  run(cn, ab, paste0("tximport ", cfa, " counts + ISAR abundance"))
}
