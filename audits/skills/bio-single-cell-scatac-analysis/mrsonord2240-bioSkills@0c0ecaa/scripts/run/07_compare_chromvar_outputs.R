# Purpose: Assert deterministic chromVAR output once the private R library is exposed.
# Inputs:   argv[1:2] = two differential-motif CSV files.
# Usage:    r.sh 07_compare_chromvar_outputs.R run1.csv run2.csv
a <- commandArgs(trailingOnly = TRUE); stopifnot(length(a) == 2)
x <- read.csv(a[1], check.names = FALSE); y <- read.csv(a[2], check.names = FALSE)
stopifnot(identical(x, y), nrow(x) > 0)
cat('identical_csv=TRUE rows=', nrow(x), ' significant=', sum(x$p_val_adj < 0.05), '\n', sep='')
