# INPUT 4 (real data): run SKILL.md block S04 LITERALLY (source of blocks/S04_r.R, echo on) in the staged demo dir, then check its results by content.
setwd('F:/OpenScience/audits/bio-single-cell-splicing/run/out/in4_demo')
options(warn = 1)
source('F:/OpenScience/audits/bio-single-cell-splicing/run/blocks/S04_r.R', echo = TRUE, max.deparse.length = Inf)
cat('\n===== CHECKS =====\n')
stopifnot(is.data.frame(res), nrow(res) > 0, all(c('tran_id', 'mean.g1', 'mean.g2', 'mean.diff', 'p.val', 'p.val.adj') %in% colnames(res)))
cat('CompareValues result rows:', nrow(res), '\n'); print(res[order(res$p.val.adj), c('tran_id', 'mean.g1', 'mean.g2', 'mean.diff', 'p.val', 'p.val.adj')][1:min(5, nrow(res)), ])
cat('Modality results dim:', dim(marvel$Modality$Results), '\n'); print(table(marvel$Modality$Results$modality.bimodal.adj, useNA = 'ifany'))
# (1) hand PSI from raw junction counts (sj is the wide matrix S04 built) vs marvel$PSI$SE  [convention in ComputePSI: mean of two inclusion junctions / (that + skip)]
psi <- marvel$PSI$SE; rownames(psi) <- psi$tran_id; cells <- setdiff(colnames(sj), 'coord.intron'); sjm <- as.data.frame(sj); rownames(sjm) <- sjm$coord.intron
np <- 0; maxd <- 0; nev <- 0
for (tid in rownames(psi)) {
  p <- strsplit(strsplit(tid, '@')[[1]], ':'); e <- lapply(p, function(x) as.integer(x[2:3])); chr <- p[[1]][1]
  if (p[[1]][4] == '-') { e <- rev(e) }   # minus-strand tran_id lists exons 5'->3' on the transcript: reverse to genomic order
  j <- c(paste(chr, e[[1]][2] + 1, e[[2]][1] - 1, sep = ':'), paste(chr, e[[2]][2] + 1, e[[3]][1] - 1, sep = ':'), paste(chr, e[[1]][2] + 1, e[[3]][1] - 1, sep = ':'))
  if (!all(j %in% rownames(sjm))) next
  nev <- nev + 1
  a <- unlist(sjm[j[1], cells]); b <- unlist(sjm[j[2], cells]); s <- unlist(sjm[j[3], cells])
  for (cl in cells) {
    inc <- (a[cl] + b[cl]) / 2; hand <- inc / (inc + s[cl]); mp <- psi[tid, cl]
    if (a[cl] + b[cl] + s[cl] >= 10 && !is.na(mp) && !is.na(hand)) { np <- np + 1; maxd <- max(maxd, abs(mp - hand)) }
  }
}
cat('events checked by hand:', nev, ' cell-event PSI pairs compared:', np, ' max |MARVEL - hand|:', maxd, '\n')
stopifnot(np > 50, maxd < 1e-9)
# (2) second method for the wilcox comparison: scipy-equivalent wilcox.test on the PSI matrix for the top event
top <- res$tran_id[which.min(res$p.val)]; x <- unlist(psi[top, neurons]); y <- unlist(psi[top, glia])
w <- wilcox.test(x, y, exact = FALSE, correct = FALSE)
cat('top event', top, ': independent wilcox.test p =', signif(w$p.value, 4), 'vs MARVEL p.val', signif(res$p.val[res$tran_id == top], 4), '; mean.g1(x100)', round(mean(x, na.rm = TRUE) * 100, 2), 'vs', round(res$mean.g1[res$tran_id == top], 2), '\n')
cat('mean.diff == mean.g2 - mean.g1 on all rows:', all(abs(res$mean.diff - (res$mean.g2 - res$mean.g1)) < 1e-8), '\n')
