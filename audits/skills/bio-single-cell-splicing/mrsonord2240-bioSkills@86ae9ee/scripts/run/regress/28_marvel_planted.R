# Input 5 (planted truth, MARVEL): SYNTHETIC 200-event x 60-cell plate-like junction matrix with known group PSI, 20% low-coverage cells.
# Runs the CORRECTED MARVEL call chain (the Skill's literal AssignModality/CompareValues calls fail; see 25_*), and checks recovery, direction and null FPR.
suppressMessages({library(MARVEL); library(data.table)})
set.seed(7)
NE <- 200; NC <- 60
cells <- sprintf('cell%02d', 1:NC); grp <- rep(c('A','B'), each = NC/2); lowcov <- runif(NC) < 0.2
cls <- c(rep('big', 40), rep('mid', 20), rep('null', NE - 60))
psiA <- psiB <- numeric(NE)
for (i in 1:NE) {
  if (cls[i] == 'null') { psiA[i] <- psiB[i] <- round(runif(1, 0.2, 0.8), 2) }
  else if (cls[i] == 'big') { if (runif(1) < .5) { psiA[i] <- .9; psiB[i] <- .1 } else { psiA[i] <- .1; psiB[i] <- .9 } }
  else { if (runif(1) < .5) { psiA[i] <- .75; psiB[i] <- .45 } else { psiA[i] <- .45; psiB[i] <- .75 } }
}
# coordinates: exon1 [s, s+99], intron 400, exon2 [ ,+89], intron 400, exon3 [ ,+99]
ev <- data.frame(idx = 1:NE)
ev$s1 <- 100000 + (1:NE) * 5000; ev$e1 <- ev$s1 + 99; ev$s2 <- ev$e1 + 401; ev$e2 <- ev$s2 + 89; ev$s3 <- ev$e2 + 401; ev$e3 <- ev$s3 + 99
ev$tran_id <- sprintf('chr1:%d:%d:+@chr1:%d:%d:+@chr1:%d:%d', ev$s1, ev$e1, ev$s2, ev$e2, ev$s3, ev$e3)
# MARVEL 2.0.5's ComputePSI.SE crashes ('non-character argument' in strsplit) when the SE table has NO minus-strand event, so the last 3 (null) events are minus-strand
neg <- (NE-2):NE
ev$tran_id[neg] <- sprintf('chr1:%d:%d:-@chr1:%d:%d:-@chr1:%d:%d', ev$s3[neg], ev$e3[neg], ev$s2[neg], ev$e2[neg], ev$s1[neg], ev$e1[neg])
ev$gene_id <- sprintf('SYNG%03d', 1:NE); ev$gene_short_name <- ev$gene_id; ev$gene_type <- 'protein_coding'
j1 <- sprintf('chr1:%d:%d', ev$e1 + 1, ev$s2 - 1); j2 <- sprintf('chr1:%d:%d', ev$e2 + 1, ev$s3 - 1); js <- sprintf('chr1:%d:%d', ev$e1 + 1, ev$s3 - 1)
M <- matrix(0L, nrow = 3 * NE, ncol = NC, dimnames = list(c(j1, j2, js), cells))
for (c in 1:NC) for (i in 1:NE) {
  pm <- if (grp[c] == 'A') psiA[i] else psiB[i]
  pc <- min(max(rbeta(1, max(pm * 20, .5), max((1 - pm) * 20, .5)), .001), .999)
  n <- rnbinom(1, size = 2, mu = if (lowcov[c]) 3 else 60)          # reads that discriminate (inc junction pair vs skip)
  ninc <- rbinom(1, n, pc); nsk <- n - ninc
  a <- rbinom(1, ninc, .5)
  M[j1[i], c] <- a; M[j2[i], c] <- ninc - a; M[js[i], c] <- nsk
}
# INTERNAL consistency for the scoring: MARVEL uses mean of the two inclusion junctions, so raw counts are as generated
sj <- data.table(coord.intron = rownames(M), as.data.frame(M))
pheno <- data.frame(sample.id = cells, cell.type = grp, stringsAsFactors = FALSE)
feat <- list(SE = ev[, c('tran_id', 'gene_id', 'gene_short_name', 'gene_type')])
gf <- unique(ev[, c('gene_id', 'gene_short_name', 'gene_type')])
expd <- data.frame(gene_id = gf$gene_id, matrix(round(rnorm(nrow(gf) * NC, 6, 1), 3), nrow = nrow(gf), dimnames = list(NULL, cells)))
write.table(data.frame(coord.intron = rownames(M), M), 'F:/OpenScience/audits/bio-single-cell-splicing/run/data/marvel_planted_SJ.tsv', sep = '\t', quote = FALSE, row.names = FALSE)   # SYNTHETIC
write.table(data.frame(ev[, c('tran_id','gene_id')], cls, psiA, psiB), 'F:/OpenScience/audits/bio-single-cell-splicing/run/data/marvel_planted_truth.tsv', sep = '\t', quote = FALSE, row.names = FALSE)

build <- function(labels) {
  ph <- data.frame(sample.id = cells, cell.type = labels)
  m <- CreateMarvelObject(SpliceJunction = sj, SplicePheno = ph, SpliceFeature = feat, GeneFeature = gf, Exp = expd)
  m <- ComputePSI(m, CoverageThreshold = 10, EventType = 'SE')
  m <- TransformExpValues(m, offset = 1, transformation = 'log2', threshold.lower = 1)
  m
}
run_cmp <- function(m, labels, method) {
  g1 <- cells[labels == 'A']; g2 <- cells[labels == 'B']
  m <- CompareValues(m, cell.group.g1 = g1, cell.group.g2 = g2, min.cells = 10, method = method, level = 'splicing', event.type = 'SE', show.progress = FALSE, assign.modality = FALSE)
  x <- m$DE$PSI$Table; if (is.list(x) && !is.data.frame(x)) { cat('DE$PSI$Table is a list with', names(x), '
'); x <- x[[1]] }; x
}
m <- build(grp)
cat('PSI SE dim:', dim(m$PSI$SE), ' NA fraction in PSI:', round(mean(is.na(m$PSI$SE[, cells])), 3), ' (planted low-coverage cells fraction:', round(mean(lowcov), 3), ')\n')
# direct per-cell PSI accuracy on normal cells
psi <- as.matrix(m$PSI$SE[, cells]); rownames(psi) <- m$PSI$SE$tran_id
truth_m <- sapply(seq_along(cells), function(c) if (grp[c] == 'A') psiA else psiB); rownames(truth_m) <- ev$tran_id
ok <- !is.na(psi[ev$tran_id, ])
cat('mean |PSI - true group PSI| on non-NA cells:', round(mean(abs(psi[ev$tran_id, ][ok] - truth_m[ok])), 3), '\n')
for (meth in c('wilcox', 'dts')) {
  res <- tryCatch(run_cmp(m, grp, meth), error = function(e) { cat('CompareValues', meth, 'ERROR:', conditionMessage(e), '\n'); NULL })
  if (is.null(res)) next
  cat('\n== method', meth, ' result cols:', paste(colnames(res), collapse = ','), ' n rows', nrow(res), '\n')
  res$cls <- cls[match(res$tran_id, ev$tran_id)]; tr <- data.frame(tran_id = ev$tran_id, psiA, psiB)
  res$dtrue <- (tr$psiB - tr$psiA)[match(res$tran_id, tr$tran_id)]
  padj <- if ('p.val.adj' %in% colnames(res)) 'p.val.adj' else grep('adj', colnames(res), value = TRUE)[1]
  dcol <- grep('mean.diff|delta|mean.g2.g1|mean.g1|psi', colnames(res), value = TRUE); cat('padj col:', padj, ' delta-like cols:', paste(dcol, collapse = ','), '\n')
  print(aggregate(list(sig = res[[padj]] < 0.05), by = list(cls = res$cls), FUN = sum)); print(table(res$cls))
  dd <- if ('mean.diff' %in% colnames(res)) res$mean.diff else NA
  if (!all(is.na(dd))) { cat('direction agreement (sign mean.diff == sign(psiB - psiA)? uses g2-g1) among planted sig:', mean(sign(dd[res$cls != 'null' & res[[padj]] < .05]) == sign(res$dtrue[res$cls != 'null' & res[[padj]] < .05])), '\n') }
  cat(meth, ': null events with adj p < 0.05:', sum(res$cls == 'null' & res[[padj]] < .05), 'of', sum(res$cls == 'null'), '; raw p<0.05:', sum(res$cls == 'null' & res$p.val < .05), '\n')
  if (meth == 'wilcox') {
    stopifnot(sum(res$cls == 'big' & res[[padj]] < .05) >= 0.9 * sum(res$cls == 'big'))
    cat('ASSERT OK: >=90% of big planted events detected (wilcox)\n')
  }
}
# NULL: permute group labels 3 times, wilcox
for (s in 1:3) {
  set.seed(100 + s); perm <- sample(grp)
  mp <- build(perm); rp <- tryCatch(run_cmp(mp, perm, 'wilcox'), error = function(e) NULL)
  if (!is.null(rp)) { padj <- if ('p.val.adj' %in% colnames(rp)) 'p.val.adj' else grep('adj', colnames(rp), value = TRUE)[1]
    cat('permutation', s, ': tested', nrow(rp), ' raw p<0.05:', sum(rp$p.val < .05), ' adj p<0.05:', sum(rp[[padj]] < .05), '\n') }
}
