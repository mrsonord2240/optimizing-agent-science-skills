# Diagnostic script (not a scored input) -- root-causes the Input 8 CAUSE crash by printing
# cause:::in_sample_elpd_loo's own source. See eval_viewer's Input 8 section.
library(cause)
cat("cause version:", as.character(packageVersion("cause")), "\n")
cat("loo version:", as.character(packageVersion("loo")), "\n")
print(cause:::in_sample_elpd_loo)
