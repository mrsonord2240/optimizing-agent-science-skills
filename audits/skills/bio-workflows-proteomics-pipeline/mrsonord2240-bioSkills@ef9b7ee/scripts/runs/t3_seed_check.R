# T3 determinism check: the Complete R Workflow block has no set.seed before its downshift imputation. Run it under 3 seeds.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
PP <- 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
setwd(file.path(PP, 'runs', 'work1'))
blk <- list.files(file.path(PP, 'runs', 'blocks'), pattern = '^b01', full.names = TRUE)
truth <- read.csv(file.path(PP, 'data', 'truth_proteins.csv'), na.strings = character(0))
for (s in c(1, 2, 3)) {
  set.seed(s); e <- new.env()
  invisible(capture.output(suppressMessages(sys.source(blk, envir = e))))
  r <- e$results; sig <- sub(';.*', '', r$protein[r$significant]); cl <- truth$class[match(sig, truth$protein)]
  cat(sprintf('seed %d: significant %d | null %d\n', s, length(sig), sum(cl == 'null', na.rm = TRUE)))
}
