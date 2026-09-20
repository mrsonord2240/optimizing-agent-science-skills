setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R")
suppressPackageStartupMessages(library(IsoformSwitchAnalyzeR))
sl <- readRDS("in1_dexseq.rds"); f <- sl$isoformFeatures
keep <- c(sprintf("ctrl_%d", 1:3), sprintf("trt_%d", 1:3))
hd <- hand_dif(keep[1:3], keep[4:6])
# alt hand computation: mean of per-sample IF
rd <- function(s) read.delim(file.path(SYN, "salmon_quant", s, "quant.sf"), stringsAsFactors = FALSE)
q <- lapply(keep, rd); tx <- q[[1]]$Name; gene <- sub("_[ABC]$","",tx)
tpm <- sapply(q, function(x) x$TPM); IFs <- apply(tpm, 2, function(v) v / ave(v, gene, FUN = sum))
alt <- data.frame(isoform_id = tx, IF1m = rowMeans(IFs[,1:3]), IF2m = rowMeans(IFs[,4:6])); alt$dIFm <- alt$IF2m - alt$IF1m
m <- merge(merge(f[, c("isoform_id","gene_id","IF1","IF2","dIF")], hd[, c("isoform_id","IF1","IF2","dIF")], by="isoform_id", suffixes=c("",".ratio_of_means")), alt, by="isoform_id")
cat("max |ISAR dIF - ratio-of-means-TPM dIF| =", max(abs(m$dIF - m$dIF.ratio_of_means)), "\n")
cat("max |ISAR dIF - mean-of-sample-IF dIF|  =", max(abs(m$dIF - m$dIFm)), "\n")
cat("max |ISAR dIF - dIF from isoformRepIF/IF matrix|:\n")
ri <- sl$isoformRepIF; cat("isoformRepIF cols:", paste(colnames(ri), collapse=","), "\n")
rm <- merge(f[,c("isoform_id","dIF")], ri, by="isoform_id"); rm$d_rep <- rowMeans(rm[, keep[4:6]]) - rowMeans(rm[, keep[1:3]])
cat("max |ISAR dIF - mean repIF diff|       =", max(abs(rm$dIF - rm$d_rep)), "\n")
# which iso are the worst? Is mismatch tied to low-expression isoforms dropped by preFilter (gene sums change)?
m$gap <- abs(m$dIF - m$dIF.ratio_of_means); print(head(m[order(-m$gap), c("isoform_id","IF1","IF1.ratio_of_means","dIF","dIF.ratio_of_means","dIFm")], 6))
# gene sum recomputed only over isoforms retained after preFilter
kept <- unique(f$isoform_id); tpm_k <- tpm[tx %in% kept, ]; gk <- gene[tx %in% kept]
IFk <- apply(tpm_k, 2, function(v) v / ave(v, gk, FUN = sum)); a2 <- data.frame(isoform_id = tx[tx %in% kept], dIFk = rowMeans(IFk[,4:6]) - rowMeans(IFk[,1:3]))
mm <- merge(f[,c("isoform_id","dIF")], a2, by="isoform_id"); cat("max |ISAR dIF - (dIF renormalised over retained isoforms)| =", max(abs(mm$dIF - mm$dIFk)), "\n")
mean_rep <- apply(tpm_k, 1, function(v) 0); ratio <- data.frame(isoform_id = tx[tx %in% kept], i1 = rowMeans(tpm_k[,1:3]), i2 = rowMeans(tpm_k[,4:6]), g = gk)
ratio$dIF_r <- with(ratio, i2/ave(i2,g,FUN=sum) - i1/ave(i1,g,FUN=sum)); mm2 <- merge(f[,c("isoform_id","dIF")], ratio, by="isoform_id")
cat("max |ISAR dIF - ratio-of-means renormalised over retained isoforms| =", max(abs(mm2$dIF - mm2$dIF_r)), "\n")
