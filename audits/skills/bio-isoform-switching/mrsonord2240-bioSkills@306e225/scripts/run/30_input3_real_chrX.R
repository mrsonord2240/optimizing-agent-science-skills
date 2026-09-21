# INPUT 3 (Edge): REAL data, nf-core rnasplice chrX (GEUVADIS LCLs, 2 GBR v 2 YRI, Salmon 2.7.0 quant, Ensembl GRCh37 GTF).
# 3A Skill workflow block verbatim (metadata rows shuffled); 3B count-route table; 3C cause tests for the scaledTPM claim.
setwd("F:/OpenScience/audits/bio-isoform-switching/run/work"); source("../helpers.R"); source("../helpers2.R")
suppressPackageStartupMessages({ library(IsoformSwitchAnalyzeR); library(tximport); library(DEXSeq) })
PD <- "F:/OpenScience/audit-envs/alternative-splicing/public-data"; set.seed(303)
sm <- c("ERR188383", "ERR188428", "ERR188454", "ERR204916"); cnd <- c("GBR", "GBR", "YRI", "YRI")
unlink("w3", recursive = TRUE); dir.create("w3/salmon_quant", recursive = TRUE); setwd("w3")
for (s in sm) { dir.create(file.path("salmon_quant", s)); file.copy(file.path(PD, "rnasplice/salmon", s, "quant.sf"), file.path("salmon_quant", s, "quant.sf")) }
file.copy(file.path(PD, "rnasplice/reference/genes_chrX.gtf"), "annotation.gtf"); file.copy(file.path(PD, "derived/chrX_tx.fa"), "transcripts.fa")
meta <- data.frame(sample_id = sm, condition = cnd)[c(3, 1, 4, 2), ]; write.table(meta, "sample_metadata.tsv", sep = "\t", quote = FALSE, row.names = FALSE)
cat("### 3A Skill block r_01.R verbatim on real chrX\n")
run_block("r_01.R"); f <- aSwitchList$isoformFeatures
sigA <- f[!is.na(f$isoform_switch_q_value) & f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1, ]
cat(sprintf("Skill block: %d isoforms in %d genes | RPL10 ENST00000406022 dIF %.4f q %.3g\n", nrow(sigA), length(unique(sigA$gene_id)), f$dIF[f$isoform_id == "ENST00000406022"][1], f$isoform_switch_q_value[f$isoform_id == "ENST00000406022"][1]))
chk("3A Skill block finds the RPL10 switch with a significant q (<1e-6)", f$isoform_switch_q_value[f$isoform_id == "ENST00000406022"][1] < 1e-6)
chk("3A number of switching isoforms in 20-32 (fixer: 26)", nrow(sigA) >= 20 && nrow(sigA) <= 32, nrow(sigA))
# hand-computed dIF for RPL10 from quant.sf (renormalised over the isoforms ISAR retained)
q <- lapply(sm, function(s) read.delim(file.path("salmon_quant", s, "quant.sf"), stringsAsFactors = FALSE)); names(q) <- sm
gi <- unique(f$isoform_id[f$gene_id == f$gene_id[f$isoform_id == "ENST00000406022"][1]])
tp <- sapply(sm, function(s) q[[s]]$TPM[match(gi, q[[s]]$Name)]); IFh <- apply(tp, 2, function(v) v / sum(v)); hand <- rowMeans(IFh[, cnd == "YRI", drop = FALSE]) - rowMeans(IFh[, cnd == "GBR", drop = FALSE])
cat("RPL10 isoforms retained:", paste(gi, collapse = ","), " hand dIF for ENST00000406022:", round(hand[match("ENST00000406022", gi)], 4), "\n")
cat("ISAR condition_1 / condition_2:", f$condition_1[1], f$condition_2[1], "\n")
chk("3A ISAR dIF for the top real switch within 0.02 of a hand computation", abs(f$dIF[f$isoform_id == "ENST00000406022"][1] - hand[match("ENST00000406022", gi)]) < 0.02)
saveRDS(list(sig = sigA$isoform_id), "sig_raw.rds")

cat("\n### 3B count-route table (isoformSwitchTestDEXSeq, q<0.05 & |dIF|>0.1)\n")
design <- data.frame(sampleID = sm, condition = cnd)
runroute <- function(cnt, ab, label) {
  sl <- suppressWarnings(importRdata(cnt, ab, design, "annotation.gtf", "transcripts.fa", showProgress = FALSE, quiet = TRUE))
  sl <- preFilter(sl, geneExpressionCutoff = 1, isoformExpressionCutoff = 0, IFcutoff = 0.01, removeSingleIsoformGenes = TRUE, keepIsoformInAllConditions = TRUE, quiet = TRUE)
  sl <- isoformSwitchTestDEXSeq(sl, reduceToSwitchingGenes = FALSE, alpha = 0.05, dIFcutoff = 0.1, quiet = TRUE)
  f <- sl$isoformFeatures; s <- f[!is.na(f$isoform_switch_q_value) & f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1, ]
  r <- f[f$isoform_id == "ENST00000406022", ]
  cat(sprintf("%-55s %3d isoforms / %2d genes | RPL10 q %.3g | isoform q<0.05 (any dIF) %d\n", label, nrow(s), length(unique(s$gene_id)), r$isoform_switch_q_value[1], sum(f$isoform_switch_q_value < 0.05, na.rm = TRUE)))
  invisible(sl) }
sq_def <- suppressMessages(importIsoformExpression("salmon_quant/", addIsofomIdAsColumn = TRUE, showProgress = FALSE, quiet = TRUE))
sl_def <- runroute(sq_def$counts, sq_def$abundance, "ISAR default (calculateCountsFromAbundance=TRUE)")
sq_raw <- suppressMessages(importIsoformExpression("salmon_quant/", addIsofomIdAsColumn = TRUE, calculateCountsFromAbundance = FALSE, showProgress = FALSE, quiet = TRUE))
sl_raw <- runroute(sq_raw$counts, sq_raw$abundance, "ISAR calculateCountsFromAbundance=FALSE (Skill)")
fl <- setNames(file.path("salmon_quant", sm, "quant.sf"), sm)
for (m in c("lengthScaledTPM", "scaledTPM", "dtuScaledTPM")) {
  t2g <- read.delim(file.path(PD, "rnasplice/salmon/genes_chrX.tx2gene.tsv"), header = FALSE); colnames(t2g) <- c("tx", "gene")
  tx <- tximport(fl, type = "salmon", txOut = TRUE, countsFromAbundance = m, tx2gene = t2g)
  runroute(data.frame(isoform_id = rownames(tx$counts), tx$counts, check.names = FALSE), data.frame(isoform_id = rownames(tx$abundance), tx$abundance, check.names = FALSE), paste("tximport", m))
}

cat("\n### 3C cause tests\n")
rpl <- function(sl) { g <- sl$isoformFeatures$gene_ref[sl$isoformFeatures$isoform_id == "ENST00000406022"][1]; a <- sl$isoformSwitchAnalysis; a[a$gene_ref == g, c("isoform_id", "pvalue", "padj", "dIF")] }
cat("RPL10 isoform rows, raw route:\n"); print(rpl(sl_raw)); cat("RPL10 isoform rows, ISAR default route:\n"); print(rpl(sl_def))
plain <- function(cnt, label) {
  cn <- as.data.frame(cnt); rownames(cn) <- cn$isoform_id; cn$isoform_id <- NULL; cn <- cn[, sm]
  g <- f$gene_id[match(rownames(cn), f$isoform_id)]; keep <- !is.na(g) & rowSums(cn) > 0; cn <- cn[keep, ]; g <- g[keep]
  dx <- DEXSeqDataSet(round(as.matrix(cn)), data.frame(condition = factor(cnd), row.names = sm), design = ~ sample + exon + condition:exon, featureID = rownames(cn), groupID = g)
  dx <- estimateSizeFactors(dx); dx <- estimateDispersions(dx, quiet = TRUE); dx <- testForDEU(dx, reducedModel = ~ sample + exon)
  r <- DEXSeqResults(dx, independentFiltering = FALSE); pg <- perGeneQValue(r); gg <- f$gene_id[f$isoform_id == "ENST00000406022"][1]
  rr <- as.data.frame(r[r$groupID == gg, c("featureID", "pvalue", "padj")])
  cat(sprintf("plain DEXSeq [%s]: gene-level perGeneQ RPL10 = %.3g ; genes perGeneQ<0.05: %d ; RPL10 isoform padj min %.3g (isoform rows %d)\n", label, pg[gg], sum(pg < 0.05, na.rm = TRUE), min(rr$padj, na.rm = TRUE), nrow(rr))); print(rr) }
plain(sq_raw$counts, "raw route")
plain(sq_def$counts, "default scaledTPM route")
len2 <- q[[1]]$Length[match(sq_raw$counts$isoform_id, q[[1]]$Name)]
fac <- median(len2) / len2; cat("length factor range:", round(range(fac), 3), "| median length", median(len2), "\n")
c1 <- sq_raw$counts; c1[, sm] <- c1[, sm] * fac; runroute(c1, sq_raw$abundance, "raw counts x median(len)/len")
c2 <- sq_raw$counts; c2[, sm] <- c2[, sm] * sample(fac); runroute(c2, sq_raw$abundance, "raw counts x SAME factors permuted across isoforms")
c3 <- sq_raw$counts; c3[, sm] <- sweep(as.matrix(c3[, sm]), 2, c(0.7, 1.3, 0.9, 1.1), "*"); runroute(c3, sq_raw$abundance, "raw counts x per-sample constants (global scaling only)")
c4 <- sq_raw$counts; c4[, sm] <- c4[, sm] * sqrt(fac); runroute(c4, sq_raw$abundance, "raw counts x sqrt(median(len)/len)")
gn <- f$gene_id[match(c1$isoform_id, f$isoform_id)]; c5 <- c1
for (s in sm) { tot_raw <- ave(sq_raw$counts[[s]], gn, FUN = sum); tot_new <- ave(c1[[s]], gn, FUN = sum); c5[[s]] <- c1[[s]] * ifelse(tot_new > 0, tot_raw / tot_new, 1) }
runroute(c5, sq_raw$abundance, "length-scaled, gene totals restored to raw")
cat("DONE 3A-3C\n")
