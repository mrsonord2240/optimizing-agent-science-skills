# SYNTHETIC count-level DTU test (planted truth): 300 genes x 2-4 isoforms, 3 v 3, Dirichlet-multinomial counts, 30 genes with planted DTU.
# Uses SKILL's dmFilter parameters verbatim, then the DRIMSeq test (SKILL: 'then proceed with the standard DEXSeq + stageR pipeline').
set.seed(20260920)
suppressMessages({library(DRIMSeq); library(DEXSeq); library(stageR)})
ng <- 300; dtu <- sort(sample(ng, 30))
rows <- list()
for (g in seq_len(ng)) {
  k <- sample(2:4, 1)
  a <- rgamma(k, 2); p1 <- sort(a / sum(a), decreasing = TRUE)
  p2 <- p1
  if (g %in% dtu) { p1 <- c(0.65, rep(0.35 / (k - 1), k - 1)); p2 <- c(0.25, rep(0.75 / (k - 1), k - 1)) }  # major isoform switches
  tot <- rpois(1, 500)
  cnt <- matrix(0L, nrow = k, ncol = 6)
  for (s in 1:6) {
    pp <- if (s <= 3) p1 else p2
    pr <- rgamma(k, pp * 60); pr <- pr / sum(pr)
    cnt[, s] <- as.integer(rmultinom(1, rpois(1, tot * runif(1, 0.7, 1.3)), pr))
  }
  for (j in seq_len(k)) rows[[length(rows) + 1]] <- data.frame(ids = paste0("iso", g, "_", j, "_G", g), t(cnt[j, ]))
}
counts <- do.call(rbind, rows)
sn <- c("c1_ctrl_b1", "c2_ctrl_b1", "c3_ctrl_b1", "t1_trt_b1", "t2_trt_b1", "t3_trt_b1")
colnames(counts) <- c("ids", sn)
write.table(counts, "F:/OpenScience/audits/bio-long-read-splicing/run/data/synth/dtu_counts_flair_format.tsv", sep = "\t", quote = FALSE, row.names = FALSE)
cat("synthetic FLAIR-format count matrix:", nrow(counts), "isoforms,", ng, "genes,", length(dtu), "planted DTU genes\n")

counts$gene_id <- sub("^.*_", "", counts$ids); counts$feature_id <- counts$ids
samples <- data.frame(sample_id = sn, condition = sub("^[^_]+_([^_]+)_.*$", "\\1", sn))
d <- dmDSdata(counts = counts[, c("gene_id", "feature_id", sn)], samples = samples)
d <- dmFilter(d, min_samps_feature_expr = 3, min_feature_expr = 5, min_samps_feature_prop = 3, min_feature_prop = 0.1, min_samps_gene_expr = 6, min_gene_expr = 10)
cat("after SKILL dmFilter: genes", length(unique(DRIMSeq::counts(d)$gene_id)), "features", nrow(DRIMSeq::counts(d)), "\n")
design <- model.matrix(~ condition, data = DRIMSeq::samples(d))
d <- dmPrecision(d, design = design); d <- dmFit(d, design = design); d <- dmTest(d, coef = "conditiontrt")
res <- DRIMSeq::results(d)
truth <- paste0("G", dtu)
called <- res$gene_id[!is.na(res$adj_pvalue) & res$adj_pvalue < 0.05]
tp <- sum(called %in% truth); fp <- sum(!(called %in% truth)); fn <- sum(!(truth %in% called))
cat(sprintf("DRIMSeq gene-level DTU: called %d ; TP %d ; FP %d ; FN %d (of %d planted; %d planted genes fell to the SKILL dmFilter)\n", length(called), tp, fp, fn, length(truth), sum(!(truth %in% res$gene_id))))
cat(sprintf("recall %.2f  precision %.2f\n", tp / length(truth), tp / max(length(called), 1)))
rf <- DRIMSeq::results(d, level = "feature")
pScreen <- res$pvalue; names(pScreen) <- res$gene_id
pConfirm <- matrix(rf$pvalue, ncol = 1); rownames(pConfirm) <- rf$feature_id
tx2gene <- data.frame(transcript = rf$feature_id, gene = rf$gene_id)
sr <- stageRTx(pScreen = pScreen, pConfirmation = pConfirm, pScreenAdjusted = FALSE, tx2gene = tx2gene)
sr <- stageWiseAdjustment(sr, method = "dtu", alpha = 0.05, allowNA = TRUE)
padj <- getAdjustedPValues(sr, order = FALSE, onlySignificantGenes = TRUE)
cat("stageR: significant genes", length(unique(padj$geneID)), " transcripts confirmed", sum(padj[, 4] < 0.05, na.rm = TRUE), " planted genes among stageR-significant:", sum(unique(padj$geneID) %in% truth), "\n")
