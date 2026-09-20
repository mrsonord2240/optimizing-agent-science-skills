setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R")
suppressPackageStartupMessages({ library(IsoformSwitchAnalyzeR); library(tximport); library(DEXSeq); library(DRIMSeq); library(BiocParallel) })
sm <- c("ERR188383", "ERR188428", "ERR188454", "ERR204916"); design <- data.frame(sampleID = sm, condition = c("GBR", "GBR", "YRI", "YRI"))
sq <- suppressMessages(importIsoformExpression(parentDir = "real_salmon/", addIsofomIdAsColumn = TRUE, showProgress = FALSE, quiet = TRUE))
txi <- suppressMessages(tximport(setNames(file.path("real_salmon", sm, "quant.sf"), sm), type = "salmon", txOut = TRUE, countsFromAbundance = "no"))
id <- sq$counts$isoform_id
cat("RPL10 isoforms: counts (raw NumReads) vs ISAR/scaledTPM counts\n")
t2g <- read.delim("F:/OpenScience/audit-envs/alternative-splicing/public-data/rnasplice/salmon/genes_chrX.tx2gene.tsv", header = FALSE); colnames(t2g) <- c("tx", "gene")
g <- t2g$tx[t2g$gene == t2g$gene[t2g$tx == "ENST00000406022"]]; g <- intersect(g, id)
print(round(cbind(raw = txi$counts[g, ], scaled = as.matrix(sq$counts[match(g, id), sm])), 1))
cat("total counts raw:", round(sum(txi$counts[id, ])), " scaledTPM:", round(sum(as.matrix(sq$counts[, sm]))), "\n")
# plain DEXSeq (Skill's manual pipeline style) on both count types, gene RPL10 only + all genes
for (nm in c("raw", "scaledTPM")) {
  cn <- if (nm == "raw") txi$counts[id, ] else as.matrix(sq$counts[, sm]); rownames(cn) <- id
  gene <- t2g$gene[match(id, t2g$tx)]; ok <- !is.na(gene)
  d <- dmDSdata(counts = data.frame(gene_id = gene[ok], feature_id = id[ok], cn[ok, ], check.names = FALSE), samples = data.frame(sample_id = sm, condition = factor(design$condition)))
  d <- dmFilter(d, min_samps_gene_expr = 4, min_samps_feature_expr = 2, min_gene_expr = 10, min_feature_expr = 5, min_samps_feature_prop = 2, min_feature_prop = 0.05)
  k <- DRIMSeq::counts(d)
  dx <- DEXSeqDataSet(countData = round(as.matrix(k[, sm])), sampleData = data.frame(condition = factor(design$condition), row.names = sm), design = ~ sample + exon + condition:exon, featureID = k$feature_id, groupID = k$gene_id)
  dx <- estimateSizeFactors(dx); dx <- estimateDispersions(dx, quiet = TRUE); dx <- testForDEU(dx, reducedModel = ~ sample + exon)
  q <- perGeneQValue(DEXSeqResults(dx, independentFiltering = FALSE))
  cat(sprintf("plain DEXSeq on %-10s counts: %d genes tested, %d with q<0.05, RPL10 gene q = %.2g\n", nm, length(q), sum(q < 0.05, na.rm = TRUE), q[t2g$gene[t2g$tx == "ENST00000406022"]]))
}
