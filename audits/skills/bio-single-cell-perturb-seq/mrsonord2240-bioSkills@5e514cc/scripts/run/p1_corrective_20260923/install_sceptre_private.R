private_lib <- "F:/OpenScience/audits/bio-single-cell-perturb-seq/run/p1_corrective_20260923/R-private-lib"
dir.create(private_lib, recursive = TRUE, showWarnings = FALSE)
.libPaths(c(private_lib, "F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib", .libPaths()))
if (!requireNamespace("remotes", quietly = TRUE)) {
  install.packages("remotes", lib = private_lib, repos = "https://cloud.r-project.org")
}
remotes::install_github("Katsevich-Lab/sceptre@21f9ea098b69c444a884a49bc254de711968e3b5",
                        lib = private_lib, dependencies = NA, upgrade = "never", quiet = FALSE)
library(sceptre)
stopifnot(as.character(packageVersion("sceptre")) == "0.99.0")
cat("PASS private sceptre=", as.character(packageVersion("sceptre")), "\n", sep = "")
