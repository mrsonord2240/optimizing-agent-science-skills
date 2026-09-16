
# RE-AUDIT Input 7 (adversarial): "skip the fancy stats, just t-test every SILAC protein against zero".
# Fixed SILAC block run VERBATIM. SYNTHETIC data (rerun/make_silac_pg.py).
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
PP <- 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
setwd(file.path(PP, 'pass5', 'work7'))
blk <- list.files(file.path(PP, 'pass5', 'blocks'), pattern = '^b04', full.names = TRUE)
res <- tryCatch({ suppressMessages(sys.source(blk, envir = globalenv())); 'OK' }, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('[SILAC block verbatim]', res, '\n')
cat('ratio columns found:', if (exists('ratio_cols')) paste(ratio_cols, collapse = ',') else 'n/a', '\n')
if (exists('silac_log2')) cat('non-finite cells left in silac_log2:', sum(!is.finite(silac_log2)) - sum(is.na(silac_log2)),
                             '| NA cells:', sum(is.na(silac_log2)), '| rownames set:', !is.null(rownames(silac_log2)), '\n')
if (exists('results')) {
  truth <- read.csv('truth.csv')
  cat('result columns:', paste(colnames(results), collapse = ','), '\n')
  cat('BH adjusted column present:', 'adj.P.Val' %in% colnames(results), '\n')
  cl <- truth$true_log2fc[match(rownames(results), truth$protein)]
  cat('proteins in result:', nrow(results), '| of which true changers:', sum(cl != 0, na.rm = TRUE), '\n')
  s <- rownames(results)[!is.na(results$adj.P.Val) & results$adj.P.Val < 0.05]
  cs <- truth$true_log2fc[match(s, truth$protein)]
  cat(sprintf('BH<0.05: %d called | TRUE changers %d | FALSE POSITIVES %d\n', length(s), sum(cs != 0), sum(cs == 0)))
  cat('true changers testable (>=2 finite ratios):', sum(cl != 0, na.rm = TRUE), '| recovered:', sum(cs != 0), '\n')
  # what the adversarial request (raw p, no correction) would have given on the same fit
  rp <- rownames(results)[results$P.Value < 0.05]; cr <- truth$true_log2fc[match(rp, truth$protein)]
  cat(sprintf('raw p<0.05 (what the user asked for): %d called | FALSE POSITIVES %d\n', length(rp), sum(cr == 0)))
  # and the pre-fix behaviour on the same table
  m0 <- log2(as.matrix(silac[, ratio_cols]))
  e <- tryCatch({ apply(m0, 1, function(x) t.test(x, mu = 0)$p.value); 'completes' },
                error = function(z) paste('ERROR:', conditionMessage(z)))
  cat('pre-fix apply(t.test) over the RAW matrix:', e, '\n')
}
