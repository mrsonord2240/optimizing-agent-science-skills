# INPUT 4: run SKILL.md block S04 LITERALLY on a planted dir (arg1 = dir), then score against planted truth and against a hand computation. Usage: Rscript 36_marvel_planted_S04.R <dir> <planted|null>
args <- commandArgs(TRUE); d <- args[1]; mode <- args[2]
setwd(d); options(warn = 1)
r <- tryCatch({ source('F:/OpenScience/audits/bio-single-cell-splicing/run/blocks/S04_r.R', echo = FALSE); 'OK' }, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('block S04 status:', r, '\n'); if (r != 'OK') quit(status = 1)
truth <- read.table('truth.tsv', header = TRUE, sep = '\t', stringsAsFactors = FALSE)
cat('PSI SE dim', dim(marvel$PSI$SE), '; CompareValues rows', nrow(res), '\n')
res$cls <- truth$cls[match(res$tran_id, truth$tran_id)]; res$dtrue <- (truth$psiB_glia - truth$psiA_neuron)[match(res$tran_id, truth$tran_id)]
res$sig <- res$p.val.adj < 0.05
print(table(cls = res$cls, sig = res$sig))
pl <- res[res$cls != 'null' & res$sig, ]
if (nrow(pl)) cat('sign(mean.diff)==sign(psiB - psiA) among significant planted:', mean(sign(pl$mean.diff) == sign(pl$dtrue)), ' n', nrow(pl), '\n')
cat('null events: adj p<0.05', sum(res$cls == 'null' & res$sig), 'of', sum(res$cls == 'null'), '; raw p<0.05', sum(res$cls == 'null' & res$p.val < 0.05), '\n')
# hand PSI from raw counts (mean of the two inclusion junctions / (that + skip)), all cell-event pairs above CoverageThreshold=10
psi <- marvel$PSI$SE; rownames(psi) <- psi$tran_id; cells <- setdiff(colnames(sj), 'coord.intron'); sjm <- as.data.frame(sj); rownames(sjm) <- sjm$coord.intron
np <- 0; maxd <- 0; nna <- 0
for (tid in rownames(psi)) {
  p <- strsplit(strsplit(tid, '@')[[1]], ':'); e <- lapply(p, function(x) as.integer(x[2:3])); chr <- p[[1]][1]; if (p[[1]][4] == '-') e <- rev(e)
  jj <- c(paste(chr, e[[1]][2] + 1, e[[2]][1] - 1, sep = ':'), paste(chr, e[[2]][2] + 1, e[[3]][1] - 1, sep = ':'), paste(chr, e[[1]][2] + 1, e[[3]][1] - 1, sep = ':'))
  a <- if (jj[1] %in% rownames(sjm)) unlist(sjm[jj[1], cells]) else rep(0, length(cells)); b <- if (jj[2] %in% rownames(sjm)) unlist(sjm[jj[2], cells]) else rep(0, length(cells)); s <- if (jj[3] %in% rownames(sjm)) unlist(sjm[jj[3], cells]) else rep(0, length(cells))
  names(a) <- names(b) <- names(s) <- cells
  for (cl in cells) {
    tot <- a[cl] + b[cl] + s[cl]; mp <- psi[tid, cl]
    if (tot >= 10) { hand <- (a[cl] + b[cl]) / 2 / ((a[cl] + b[cl]) / 2 + s[cl]); if (!is.na(mp) && !is.na(hand)) { np <- np + 1; maxd <- max(maxd, abs(mp - hand)) } else nna <- nna + 1 }
  }
}
cat('hand-computed PSI pairs compared:', np, ' max |MARVEL - hand| =', maxd, ' (NA in one of the two: ', nna, ')\n'); stopifnot(np > 1000, maxd < 1e-9)
# per-group truth accuracy of MARVEL PSI on non-NA cells
grp <- seurat_obj@meta.data[cells, 'cell.type']; tm <- sapply(seq_along(cells), function(i) if (grp[i] == 'neuron') truth$psiA_neuron else truth$psiB_glia); rownames(tm) <- truth$tran_id
pm <- as.matrix(psi[truth$tran_id, cells]); ok <- !is.na(pm); cat('mean |PSI - true group PSI| on non-NA cell-events:', round(mean(abs(pm[ok] - tm[ok])), 3), ' NA fraction', round(mean(is.na(pm)), 3), '\n')
if (mode == 'planted') {
  cat('big detected', sum(res$cls == 'big' & res$sig), '/', sum(res$cls == 'big'), ' mid', sum(res$cls == 'mid' & res$sig), '/', sum(res$cls == 'mid'), '\n')
  stopifnot(sum(res$cls == 'big' & res$sig) >= 0.9 * sum(res$cls == 'big')); cat('ASSERT OK big >= 90%\n')
} else { stopifnot(sum(res$sig) <= 2); cat('ASSERT OK null: <= 2 significant\n') }
cat('Modality table:'); print(table(marvel$Modality$Results$modality.bimodal.adj))
