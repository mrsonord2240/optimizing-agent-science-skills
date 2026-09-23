# Phase 2 audit input 5: execute every shipped R example exactly by sourcing it.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
root <- 'F:/OpenScience/wt/differential-expression-deseq2-basics/differential-expression/deseq2-basics/examples'

source(file.path(root, 'basic_workflow.R'))
stopifnot(nrow(res_shrunk) == 1000L, sum(!is.na(res_shrunk$padj)) > 0L)
cat('basic_workflow.R: PASS; significant=', nrow(sig_genes), '\n')

source(file.path(root, 'batch_correction.R'))
stopifnot(nrow(res) == 1000L, 'condition_treated_vs_control' %in% resultsNames(dds))
cat('batch_correction.R: PASS; coefficient=', resultsNames(dds)[3], '\n')

source(file.path(root, 'multi_condition.R'))
stopifnot(nrow(res_A) == 1000L, nrow(res_B) == 1000L, nrow(res_AB) == 1000L)
cat('multi_condition.R: PASS; three contrasts returned 1000 rows each\n')
