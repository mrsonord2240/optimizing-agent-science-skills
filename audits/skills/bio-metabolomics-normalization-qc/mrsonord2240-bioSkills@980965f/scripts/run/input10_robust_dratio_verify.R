# Phase 2 Input 10: parse and verify the CLI output produced by input10_robust_dratio_cli.sh.
out <- read.csv('F:/OpenScience/audits/bio-metabolomics-normalization-qc/run/input10_kept.csv', check.names = FALSE)
kept_names <- setdiff(colnames(out), 'sample_type')
stopifnot(nrow(out) == 36L, identical(kept_names, paste0('clean_', seq_len(30))))
cat(sprintf('CLI output parsed: %d samples, %d retained features; all retained are planted clean features\n', nrow(out), length(kept_names)))
