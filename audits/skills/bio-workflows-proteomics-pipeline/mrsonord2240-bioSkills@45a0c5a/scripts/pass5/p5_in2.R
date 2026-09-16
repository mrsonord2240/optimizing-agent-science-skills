
# RE-AUDIT Input 2 (Variant A): DIA-NN report.parquet -> fixed "DIA-NN Workflow" block VERBATIM, then limma as the block directs. SYNTHETIC.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(limma))
PP <- 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
setwd(file.path(PP, 'pass5', 'work2'))
blk <- list.files(file.path(PP, 'pass5', 'blocks'), pattern = '^b05', full.names = TRUE)
res <- tryCatch({ suppressMessages(sys.source(blk, envir = globalenv())); 'OK' }, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('[DIA-NN block verbatim]', res, '\n')
cat('rows in report:', nrow(diann), '| after q-value filter:', nrow(diann_filt), '\n')
cat('matrix m:', dim(m), '| LOWCONF groups:', sum(grepl('^LOWCONF', rownames(m))), '| zero cells in m:', sum(m == 0, na.rm = TRUE), '| NA cells:', sum(is.na(m)), '\n')
cat('log2_matrix -Inf/Inf cells:', sum(is.infinite(log2_matrix)), '| NaN:', sum(is.nan(log2_matrix)), '| rownames set:', !is.null(rownames(log2_matrix)), '\n')
si <- read.csv('sample_annotation.csv'); cn <- sub('_DIA$', '', colnames(log2_matrix))
L <- log2_matrix; colnames(L) <- cn
si <- si[match(cn, si$sample), ]; si$condition <- factor(si$condition)
d <- model.matrix(~0 + condition + batch, data = si); colnames(d)[1:2] <- levels(si$condition)
fit <- tryCatch(eBayes(contrasts.fit(lmFit(L, d), makeContrasts(Treatment - Control, levels = d)), trend = TRUE, robust = TRUE),
                error = function(e) { cat('limma on the block output ERROR:', conditionMessage(e), '\n'); NULL })
if (!is.null(fit)) {
  tt <- topTable(fit, number = Inf, adjust.method = 'BH')
  truth <- read.csv(file.path(PP, 'data', 'truth_proteins.csv'), na.strings = character(0))
  s <- rownames(tt)[!is.na(tt$adj.P.Val) & tt$adj.P.Val < 0.05]
  cl <- truth$class[match(s, truth$protein)]
  clall <- truth$class[match(rownames(tt), truth$protein)]
  cat('limma eBayes(trend,robust) COMPLETES on the block output\n')
  cat(sprintf('BH<0.05: %d called | FALSE POS (true null) %d | up %d | down %d | on_off %d | unmatched %d\n',
      length(s), sum(cl == 'null', na.rm = TRUE), sum(cl == 'up', na.rm = TRUE), sum(cl == 'down', na.rm = TRUE),
      sum(cl == 'on_off', na.rm = TRUE), sum(is.na(cl))))
  cat('true changers in matrix:', sum(clall %in% c('up','down'), na.rm = TRUE), '| recovered:', sum(cl %in% c('up','down')), '\n')
  nn <- !is.na(clall) & clall == 'null'
  cat(sprintf('true nulls tested %d | raw p<0.05 %.1f%% (nominal 5%%) | mean log2FC %+.4f\n',
      sum(nn), 100*mean(tt$P.Value[nn] < 0.05, na.rm = TRUE), mean(tt$logFC[nn], na.rm = TRUE)))
}
