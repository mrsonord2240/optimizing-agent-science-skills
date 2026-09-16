# Gate 8 (shipped-means-present): run BOTH shipped examples VERBATIM, straight
# from the read-only upstream clone. Nothing is modified; only .libPaths is set.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
EX <- 'F:/OpenScience/external/GPTomics__bioSkills/pathway-analysis/gsea/examples'
for (f in c('gsea_go.R','gsea_msigdb.R')) {
  p <- file.path(EX, f)
  cat('\n================ ', f, ' (exists:', file.exists(p), ') ================\n')
  t0 <- Sys.time()
  ok <- tryCatch({ source(p, echo = FALSE); 'COMPLETED' },
                 error = function(e) paste('ERROR:', conditionMessage(e)))
  cat('[', f, ']', ok, '-', round(as.numeric(difftime(Sys.time(), t0, units='secs')),1), 's\n')
}
cat('\nEXIT OK\n')
