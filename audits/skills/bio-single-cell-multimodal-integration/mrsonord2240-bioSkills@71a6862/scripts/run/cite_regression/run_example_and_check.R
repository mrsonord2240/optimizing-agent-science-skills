.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
# Run the SHIPPED examples/cite_seq_analysis.R completely unmodified (copied verbatim into
# this test dir, not imported/edited) against independent synthetic 10x-format directories.
source('cite_seq_analysis_example.R')

truth <- readRDS('truth.rds')
names(truth) <- colnames(obj)  # obj is left in the global env by the sourced script
cl <- Idents(obj)
tab <- table(cl, truth)
cat("\nCluster x truth cross-tab:\n")
print(tab)

# purity: for each cluster, fraction belonging to its majority true type
purity <- sum(apply(tab, 1, max)) / sum(tab)
cat(sprintf("\nOverall cluster purity vs ground truth: %.3f\n", purity))
cat("n clusters:", length(unique(cl)), "\n")
