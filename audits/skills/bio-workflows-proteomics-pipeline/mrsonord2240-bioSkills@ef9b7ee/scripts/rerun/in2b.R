
# RE-AUDIT Input 2 (Variant A): DIA-NN report.parquet -> fixed "DIA-NN Workflow" block VERBATIM, then limma as the block directs. SYNTHETIC.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(limma))
PP <- 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
setwd(file.path(PP, 'rerun', 'work2b'))
blk <- list.files(file.path(PP, 'rerun', 'blocks'), pattern = '^b05', full.names = TRUE)
res <- tryCatch({ suppressMessages(sys.source(blk, envir = globalenv())); 'OK' }, error = function(e) paste('ERROR:', conditionMessage(e)))
cat('[DIA-NN block verbatim]', res, '\n')
cat('rows in report:', nrow(diann), '| after q-value filter:', nrow(diann_filt), '\n')
cat('matrix m:', dim(m), '| LOWCONF groups:', sum(grepl('^LOWCONF', rownames(m))), '| zero cells in m:', sum(m == 0, na.rm = TRUE), '| NA cells:', sum(is.na(m)), '\n')
cat('log2_matrix -Inf/Inf cells:', sum(is.infinite(log2_matrix)), '| NaN:', sum(is.nan(log2_matrix)), '| rownames set:', !is.null(rownames(log2_matrix)), '\n')
