# Shared evaluation helper: score a fitted FraserDataSet against planted truth (SYNTHETIC cohort).
suppressPackageStartupMessages({library(FRASER); library(GenomicRanges)})
eval_fds <- function(fds, synth, delta = 0.1, padj = 0.05, rename = c(PATIENT_001 = "S05"), tag = "") {
  res <- results(fds, psiType = "jaccard", padjCutoff = padj, deltaPsiCutoff = delta)
  cat(sprintf("[%s] FRASER %s | samples=%d | junctions kept=%d | total calls (padj<%g,|dPsi|>=%g)=%d\n", tag,
              as.character(packageVersion("FRASER")), ncol(fds), nrow(fds), padj, delta, length(res)))
  truth <- read.delim(file.path(synth, "planted_truth.tsv"), stringsAsFactors = FALSE)
  genes <- read.delim(file.path(synth, "genes.tsv"), stringsAsFactors = FALSE)
  gr_genes <- GRanges(genes$chrom, IRanges(genes$start, genes$end), gene = genes$gene)
  sid <- as.character(res$sampleID); for (n in names(rename)) sid[sid == n] <- rename[[n]]
  res$sample <- sid
  hg <- rep(NA_character_, length(res)); ov <- findOverlaps(res, gr_genes); hg[queryHits(ov)] <- gr_genes$gene[subjectHits(ov)]
  res$gene <- hg
  present <- as.character(colnames(fds)); for (n in names(rename)) present[present == n] <- rename[[n]]; truth <- truth[truth$sample %in% present, ]   # only score events whose sample is in this cohort
  spl <- truth[truth$type %in% c("exon_skipping", "cryptic_donor", "intron_retention", "pseudoexon"), ]
  det <- 0
  for (i in seq_len(nrow(spl))) {
    t <- spl[i, ]; h <- res[res$sample == t$sample & !is.na(res$gene) & res$gene == t$gene]
    if (length(h)) det <- det + 1
    cat(sprintf("  %-4s %-4s %-17s : %s\n", t$sample, t$gene, t$type,
      if (length(h)) sprintf("DETECTED n=%d min_padj=%.1e max|dPsi|=%.2f", length(h), min(h$padjust), max(abs(h$deltaPsi))) else "not detected"))
  }
  # the two expression-only events: FRASER should NOT call them (splicing unchanged)
  for (i in which(truth$type %in% c("expression_down", "expression_up"))) {
    t <- truth[i, ]; h <- res[res$sample == t$sample & !is.na(res$gene) & res$gene == t$gene]
    cat(sprintf("  %-4s %-4s %-17s : FRASER calls=%d (expected 0; expression-only)\n", t$sample, t$gene, t$type, length(h)))
  }
  planted_pairs <- paste(truth$sample, truth$gene)
  np <- res[!(paste(res$sample, res$gene) %in% planted_pairs)]
  fp <- np[np$sample != "S29"]
  tested <- nrow(fds) * ncol(fds)
  cat(sprintf("  planted splicing events detected: %d/%d\n", det, nrow(spl)))
  cat(sprintf("  non-planted calls (excl. S29 mismatch): %d in %d samples; distinct sample-gene pairs %d; per junction-sample test rate %.2e\n",
              length(fp), length(unique(fp$sample)), length(unique(paste(fp$sample, fp$gene))), length(fp) / tested))
  cat(sprintf("  S29 tissue-mismatch sample calls: %d (distinct genes %d); other samples median calls %.1f\n", sum(res$sample == "S29"),
              length(unique(res$gene[res$sample == "S29"])), median(table(factor(fp$sample, levels = setdiff(unique(as.character(sid)), c("S29")))))))
  invisible(list(res = res, det = det, fp = length(fp), n_spl = nrow(spl), fp_samples = length(unique(fp$sample)), s29 = sum(res$sample == "S29")))
}
