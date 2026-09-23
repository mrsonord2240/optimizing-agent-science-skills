# Pass-5 Input 8: THREE-condition dose design (Ctl / Low / High, n=4 each, two batches) through the
# FIXED "Complete R Workflow" block, run VERBATIM. SYNTHETIC (pass5/make_3cond.py).
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
PP <- 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
blk <- list.files(file.path(PP,'pass5','blocks'), pattern='^b01', full.names=TRUE)
setwd(file.path(PP,'pass5','workC'))
res <- tryCatch({ suppressWarnings(sys.source(blk, envir=globalenv())); 'OK' },
                error=function(e) paste('ERROR:', conditionMessage(e)))
cat('\n[Complete R Workflow block verbatim, 3 conditions]', res, '\n')
if (res == 'OK' && exists('results')) {
  truth <- read.csv('truth.csv')
  cls <- truth$class[match(results$protein, truth$protein)]
  for (cn in unique(results$contrast)) {
    k <- results$contrast == cn
    s <- k & results$significant
    cat(sprintf('%-14s: called %3d | FP among true nulls %d / %d tested nulls | dose_up %d dose_down %d high_only %d\n',
        cn, sum(s), sum(cls[s]=='null', na.rm=TRUE), sum(cls[k]=='null', na.rm=TRUE),
        sum(cls[s]=='dose_up', na.rm=TRUE), sum(cls[s]=='dose_down', na.rm=TRUE),
        sum(cls[s]=='high_only', na.rm=TRUE)))
  }
  cat('total significant:', sum(results$significant), '| contrasts:', paste(unique(results$contrast), collapse=','), '\n')
  cat('design columns:', colnames(design), '| batch in design:', has_batch, '\n')
  cat('annotation row order == matrix column order:',
      identical(as.character(sample_info$sample), colnames(normalized)), '\n')
}
