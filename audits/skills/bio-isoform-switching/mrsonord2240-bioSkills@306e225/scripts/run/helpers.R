# shared helpers for the audit scripts (synthetic-truth scoring)
SYN <- "F:/OpenScience/audits/bio-isoform-switching/run/data/synth"
truth <- function() read.delim(file.path(SYN, "truth_genes.tsv"), stringsAsFactors = FALSE)
chk <- function(name, ok, detail = "") { cat(sprintf("[%s] %s | %s\n", if (isTRUE(ok)) "PASS" else "FAIL", name, detail)); invisible(isTRUE(ok)) }

# hand-computed dIF straight from the quant.sf TPM (independent of every package under test)
hand_dif <- function(samples_ctrl, samples_trt, qdir = file.path(SYN, "salmon_quant")) {
  rd <- function(s) read.delim(file.path(qdir, s, "quant.sf"), stringsAsFactors = FALSE)
  q <- lapply(c(samples_ctrl, samples_trt), rd); names(q) <- c(samples_ctrl, samples_trt)
  tx <- q[[1]]$Name; gene <- sub("_[ABC]$", "", tx)
  tpm <- sapply(q, function(x) x$TPM[match(tx, x$Name)])
  m1 <- rowMeans(tpm[, samples_ctrl, drop = FALSE]); m2 <- rowMeans(tpm[, samples_trt, drop = FALSE])
  # ISAR's IF is the mean over replicates of the per-sample isoform fraction (verified in 11_dif_check.R:
  # matches to 7e-5; the ratio-of-mean-TPMs definition differs by up to 0.028 on this data)
  IFs <- apply(tpm, 2, function(v) v / ave(v, gene, FUN = sum))
  i1 <- rowMeans(IFs[, samples_ctrl, drop = FALSE]); i2 <- rowMeans(IFs[, samples_trt, drop = FALSE])
  data.frame(isoform_id = tx, gene_id = gene, IF1 = i1, IF2 = i2, dIF = i2 - i1, stringsAsFactors = FALSE)
}

# score a switchAnalyzeRlist against planted truth; returns list of metrics
score_sl <- function(sl, alpha = 0.05, dif = 0.1) {
  f <- sl$isoformFeatures
  f <- f[!is.na(f$isoform_switch_q_value), ]
  sig <- f[f$isoform_switch_q_value < alpha & abs(f$dIF) > dif, ]
  sig_genes <- unique(sig$gene_id)
  t <- truth()
  list(sig_iso = sig, sig_genes = sig_genes,
       tested_genes = length(unique(f$gene_id)),
       tp_planted = intersect(sig_genes, t$gene_id[t$true_switch]),
       fn_planted = setdiff(t$gene_id[t$true_switch], sig_genes),
       fp_null = intersect(sig_genes, t$gene_id[t$type == "null"]),
       fp_dge = intersect(sig_genes, t$gene_id[t$type == "dge_only"]),
       small_called = intersect(sig_genes, t$gene_id[t$type == "small_switch"]),
       dte_called = intersect(sig_genes, t$gene_id[t$type == "dte_like"]))
}
