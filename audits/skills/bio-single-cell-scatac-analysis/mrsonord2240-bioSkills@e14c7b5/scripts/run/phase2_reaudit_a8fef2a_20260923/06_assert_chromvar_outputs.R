# Purpose: Verify nonempty and deterministic output artifacts despite wrapper status.
# Usage: rs.sh 06_assert_chromvar_outputs.R run1.csv run2.csv run1.rds run2.rds
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
a <- commandArgs(trailingOnly = TRUE); stopifnot(length(a) == 4)
csv1 <- read.csv(a[1], check.names = FALSE); csv2 <- read.csv(a[2], check.names = FALSE)
obj1 <- readRDS(a[3]); obj2 <- readRDS(a[4])
stopifnot(nrow(csv1) > 0L, identical(csv1, csv2), 'chromvar' %in% names(obj1),
          'chromvar' %in% names(obj2), ncol(obj1) == 270L, ncol(obj2) == 270L)
cat('identical_csv=TRUE rows=', nrow(csv1), ' adjusted_significant=',
    sum(csv1$p_val_adj < 0.05), ' cells=', ncol(obj1), '\n', sep='')
