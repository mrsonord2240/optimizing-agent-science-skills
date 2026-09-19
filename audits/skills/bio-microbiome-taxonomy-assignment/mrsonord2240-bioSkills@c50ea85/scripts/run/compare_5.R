.libPaths(c("F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/R-lib", .libPaths()))
dir <- "F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/reaudit-tax"
runs <- readRDS(file.path(dir, "seeded_3runs.rds"))
run4 <- readRDS(file.path(dir, "run4.rds"))
run5 <- readRDS(file.path(dir, "run5.rds"))
allruns <- c(runs, list(run4), list(run5))
cat("Total seeded runs (across separate processes for 4,5):", length(allruns), "\n")
for (i in 1:4) for (j in (i+1):5) {
  cat(sprintf("Run %d vs Run %d: identical=%s\n", i, j, identical(allruns[[i]], allruns[[j]])))
}
