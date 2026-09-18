# Single IHW attempt at pinned nbins=5, on the re-audit's own 18,000-feature table.
# Run this script repeatedly from bash to build a crash-rate distribution (each run is
# a fresh R process, since a segfault kills the process outright).
de <- read.csv("../data/de_pvalues_reaudit.csv")
library(IHW)
res <- ihw(de$pvalue, de$mean_expression, alpha = 0.05, nbins = 5)
cat(sprintf("OK rejections=%d nbins=%d\n", rejections(res), res@nbins))
