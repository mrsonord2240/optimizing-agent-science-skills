# Purpose: Verify the two documented chromVAR runs produced identical, nonempty outputs.
# Usage: r.sh 02_assert_chromvar_outputs.R chromvar_1_diff_motifs.csv chromvar_2_diff_motifs.csv
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 2)
run1 <- read.csv(args[1], check.names = FALSE)
run2 <- read.csv(args[2], check.names = FALSE)
stopifnot(nrow(run1) > 0, identical(run1, run2))
cat('identical_csv=TRUE rows=', nrow(run1),
    ' significant=', sum(run1$p_val_adj < 0.05), '\n', sep = '')
