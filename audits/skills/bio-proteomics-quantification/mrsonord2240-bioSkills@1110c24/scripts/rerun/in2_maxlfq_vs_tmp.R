# Quant Input 2 (regression): real MaxLFQ (iq) on the same evidence vs MSstats TMP; block b02 verbatim per protein. SYNTHETIC.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
QQ <- 'F:/OpenScience/audits/bio-proteomics-quantification'
ev <- read.table(file.path(QQ, 'rerun', 'work', 'evidence.txt'), sep = '\t', header = TRUE, quote = '', comment.char = '')
ev <- ev[!(ev$Reverse %in% '+') & !(ev$Potential.contaminant %in% '+') & !is.na(ev$Intensity) & ev$Intensity > 0, ]
ev$ion <- paste(ev$Modified.sequence, ev$Charge)
agg <- aggregate(Intensity ~ Leading.razor.protein + ion + Raw.file, data = ev, FUN = sum)
agg$l2 <- log2(agg$Intensity)
for (normed in c(TRUE, FALSE)) {
  a <- agg
  if (normed) a$l2 <- a$l2 - ave(a$l2, a$Raw.file, FUN = median) + median(a$l2)   # run-normalize peptide log2 first (Skill Approach)
  runs <- sort(unique(a$Raw.file)); est <- list(); ann <- 0
  blk <- list.files(file.path(QQ, 'rerun', 'blocks'), pattern = '^b02', full.names = TRUE)
  for (p in unique(a$Leading.razor.protein)) {
    s <- a[a$Leading.razor.protein == p, ]
    peptide_log2_matrix <- matrix(NA, length(unique(s$ion)), length(runs), dimnames = list(unique(s$ion), runs))
    peptide_log2_matrix[cbind(s$ion, s$Raw.file)] <- s$l2
    e <- new.env(); assign('peptide_log2_matrix', peptide_log2_matrix, e)
    suppressMessages(sys.source(blk, envir = e))
    est[[p]] <- e$protein_estimate; if (nzchar(e$result$annotation)) ann <- ann + 1
  }
  M <- do.call(rbind, est); colnames(M) <- runs
  cat(sprintf('maxLFQ (%s): proteins %d | per-run median (centred): %s | non-empty annotation: %d\n',
      ifelse(normed, 'run-normalized input', 'NOT normalized'), nrow(M), paste(round(apply(M, 2, median, na.rm = TRUE) - median(M, na.rm = TRUE), 3), collapse = ' '), ann))
  assign(ifelse(normed, 'M_norm', 'M_raw'), M)
}
proc <- readRDS(file.path(QQ, 'rerun', 'in1_processed.rds'))$ProteinLevelData
tmp <- tapply(proc$LogIntensities, list(as.character(proc$Protein), as.character(proc$originalRUN)), mean)
truth <- read.csv(file.path(QQ, 'data', 'truth_proteins.csv')); rownames(truth) <- truth$protein
fcx <- function(m) rowMeans(m[, grep('^T', colnames(m)), drop = FALSE], na.rm = TRUE) - rowMeans(m[, grep('^C', colnames(m)), drop = FALSE], na.rm = TRUE)
cat('TMP cols:', colnames(tmp), '| TMP rows:', head(rownames(tmp), 3), '| maxLFQ cols:', colnames(M_norm), '| rows:', head(rownames(M_norm), 3), '
')
f_tmp <- fcx(tmp); f_n <- fcx(M_norm); f_r <- fcx(M_raw)
pp <- Reduce(intersect, list(names(f_tmp), names(f_n)))
pp <- pp[pp %in% truth$protein & truth[pp, 'class'] != 'on_off' & is.finite(f_tmp[pp]) & is.finite(f_n[pp])]
tr <- truth[pp, 'true_log2fc']
cat(sprintf('corr with truth (%d proteins): TMP %.3f | MaxLFQ norm %.3f | MaxLFQ raw %.3f\n', length(pp), cor(f_tmp[pp], tr), cor(f_n[pp], tr), cor(f_r[pp], tr)))
d <- abs(f_n[pp] - f_tmp[pp]); cat(sprintf('|FC MaxLFQ - FC TMP|: median %.3f | >0.5: %d | >1: %d\n', median(d), sum(d > 0.5), sum(d > 1)))
cat(sprintf('mean(FC - truth): TMP %+.3f | MaxLFQ norm %+.3f | MaxLFQ raw %+.3f\n', mean(f_tmp[pp] - tr), mean(f_n[pp] - tr), mean(f_r[pp] - tr)))
cat('class counts:', paste(names(table(truth[pp, 'class'])), table(truth[pp, 'class'])), '| median FC of true nulls (TMP):', round(median(f_tmp[pp][truth[pp, 'class'] == 'null']), 3), '\n')
