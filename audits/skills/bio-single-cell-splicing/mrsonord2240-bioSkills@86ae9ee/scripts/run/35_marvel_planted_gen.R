# SYNTHETIC MARVEL inputs with KNOWN group PSI (auditor's own design; differs from the pre-fix 200 x 60 set).
# Rscript 35_marvel_planted_gen.R <outdir> <seed> [null]
#  120 SE events: 30 big (PSI 0.85 vs 0.25), 20 mid (0.60 vs 0.35), 70 null (same PSI, U(0.2,0.8)); 20 events on the minus strand (spread over classes);
#  40 cells (20 neuron / 20 glia), 25% low-coverage (mean 4 molecules/event vs 40); per-cell PSI ~ Beta(conc 15); each junction read seen with prob 0.6.
#  'null' -> every event null. Writes the files SKILL.md block S04 reads: star_pass2/<cell>_SJ.out.tab, events_*.txt, gene_features.tsv, tpm.tsv, annotation.gtf, cells.rds  + truth.tsv
args <- commandArgs(TRUE); out <- args[1]; seed <- as.integer(args[2]); ALLNULL <- length(args) > 2 && args[3] == 'null'
suppressMessages({library(Seurat)}); set.seed(seed)
dir.create(file.path(out, 'star_pass2'), showWarnings = FALSE, recursive = TRUE)
NE <- 120; NC <- 40; cells <- sprintf('cell%02d', 1:NC); grp <- rep(c('neuron', 'glia'), each = NC / 2); low <- runif(NC) < 0.25
cls <- c(rep('big', 30), rep('mid', 20), rep('null', 70)); if (ALLNULL) cls[] <- 'null'
psiA <- psiB <- numeric(NE)
for (i in 1:NE) {
  if (cls[i] == 'null') psiA[i] <- psiB[i] <- round(runif(1, .2, .8), 2)
  else if (cls[i] == 'big') { if (runif(1) < .5) { psiA[i] <- .85; psiB[i] <- .25 } else { psiA[i] <- .25; psiB[i] <- .85 } }
  else { if (runif(1) < .5) { psiA[i] <- .60; psiB[i] <- .35 } else { psiA[i] <- .35; psiB[i] <- .60 } }
}
neg <- sort(sample(1:NE, 20)); strand <- ifelse(1:NE %in% neg, '-', '+')
ev <- data.frame(idx = 1:NE, chr = sample(c('chr1', 'chr2', 'chr3'), NE, TRUE))
ev$s1 <- 200000 + (1:NE) * 6000; ev$e1 <- ev$s1 + sample(80:200, NE, TRUE); ev$s2 <- ev$e1 + sample(300:900, NE, TRUE); ev$e2 <- ev$s2 + sample(40:150, NE, TRUE)
ev$s3 <- ev$e2 + sample(300:900, NE, TRUE); ev$e3 <- ev$s3 + sample(80:200, NE, TRUE)
ev$tran_id <- ifelse(strand == '+',
  sprintf('%s:%d:%d:+@%s:%d:%d:+@%s:%d:%d', ev$chr, ev$s1, ev$e1, ev$chr, ev$s2, ev$e2, ev$chr, ev$s3, ev$e3),
  sprintf('%s:%d:%d:-@%s:%d:%d:-@%s:%d:%d', ev$chr, ev$s3, ev$e3, ev$chr, ev$s2, ev$e2, ev$chr, ev$s1, ev$e1))
ev$gene_id <- sprintf('SYNG%03d', 1:NE); ev$gene_short_name <- sprintf('Gene%03d', 1:NE); ev$gene_type <- 'protein_coding'
j1 <- sprintf('%s:%d:%d', ev$chr, ev$e1 + 1, ev$s2 - 1); j2 <- sprintf('%s:%d:%d', ev$chr, ev$e2 + 1, ev$s3 - 1); js <- sprintf('%s:%d:%d', ev$chr, ev$e1 + 1, ev$s3 - 1)
M <- matrix(0L, 3 * NE, NC, dimnames = list(c(j1, j2, js), cells))
for (c in 1:NC) for (i in 1:NE) {
  pm <- if (grp[c] == 'neuron') psiA[i] else psiB[i]; pc <- min(max(rbeta(1, max(pm * 15, .5), max((1 - pm) * 15, .5)), .001), .999)
  n <- rnbinom(1, size = 2, mu = if (low[c]) 4 else 40); ninc <- rbinom(1, n, pc); nsk <- n - ninc
  M[j1[i], c] <- rbinom(1, ninc, .6); M[j2[i], c] <- rbinom(1, ninc, .6); M[js[i], c] <- rbinom(1, nsk, .6)
}
for (c in 1:NC) { v <- M[, c]; ok <- v > 0; p <- do.call(rbind, strsplit(rownames(M)[ok], ':'))
  write.table(data.frame(p[, 1], p[, 2], p[, 3], 0, 1, 1, v[ok], 0, 30), file.path(out, 'star_pass2', paste0(cells[c], '_SJ.out.tab')), sep = '\t', quote = FALSE, row.names = FALSE, col.names = FALSE) }
feat_cols <- c('tran_id', 'gene_id', 'gene_short_name', 'gene_type')
write.table(ev[, feat_cols], file.path(out, 'events_SE.txt'), sep = '\t', quote = FALSE, row.names = FALSE)
for (e in c('MXE', 'RI', 'A5SS', 'A3SS')) write.table(ev[0, feat_cols], file.path(out, paste0('events_', e, '.txt')), sep = '\t', quote = FALSE, row.names = FALSE)   # header-only tables
gf <- unique(ev[, c('gene_id', 'gene_short_name', 'gene_type')]); write.table(gf, file.path(out, 'gene_features.tsv'), sep = '\t', quote = FALSE, row.names = FALSE)
expd <- data.frame(gene_id = gf$gene_id, matrix(round(rgamma(nrow(gf) * NC, 3, .5), 2), nrow = nrow(gf), dimnames = list(NULL, cells)))
write.table(expd, file.path(out, 'tpm.tsv'), sep = '\t', quote = FALSE, row.names = FALSE)
gtf <- data.frame(ev$chr, 'SYN', 'gene', ev$s1, ev$e3, '.', strand, '.', sprintf('gene_id "%s"; gene_type "protein_coding"; gene_name "%s";', ev$gene_id, ev$gene_short_name))
write.table(gtf, file.path(out, 'annotation.gtf'), sep = '\t', quote = FALSE, row.names = FALSE, col.names = FALSE)
cnt <- as.matrix(expd[, -1]); rownames(cnt) <- expd$gene_id
so <- CreateSeuratObject(counts = round(cnt) + 1L, meta.data = data.frame(cell.type = grp, row.names = cells)); saveRDS(so, file.path(out, 'cells.rds'))
write.table(data.frame(tran_id = ev$tran_id, strand, cls, psiA_neuron = psiA, psiB_glia = psiB), file.path(out, 'truth.tsv'), sep = '\t', quote = FALSE, row.names = FALSE)
cat('generated', NE, 'events', sum(strand == '-'), 'minus-strand;', NC, 'cells;', sum(low), 'low-coverage;', if (ALLNULL) 'ALL NULL' else paste(names(table(cls)), table(cls), collapse = ' '), '\n')
