.libPaths(c("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/R-lib", .libPaths()))
dir <- "F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/reaudit-tax"
runs <- readRDS(file.path(dir, "seeded_3runs.rds"))
taxa <- runs[[1]]
for (rank in colnames(taxa)) {
  n <- sum(!is.na(taxa[, rank]))
  cat(sprintf("  %-8s %d/%d (%.1f%%)\n", rank, n, nrow(taxa), 100*n/nrow(taxa)))
}
