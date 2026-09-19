priv_lib <- 'F:/OpenScience/audits/bio-single-cell-perturb-seq/run/R-private-lib'
dir.create(priv_lib, recursive = TRUE, showWarnings = FALSE)
.libPaths(c(priv_lib, 'F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
cat("R version:", R.version.string, "\n")
cat(".libPaths():\n"); print(.libPaths())

if (!requireNamespace("remotes", quietly = TRUE)) {
  install.packages("remotes", lib = priv_lib, repos = "https://cran.r-project.org")
}
cat("remotes available:", requireNamespace("remotes", quietly = TRUE), "\n")

result <- tryCatch({
  remotes::install_github("Katsevich-Lab/sceptre", lib = priv_lib, upgrade = "never", quiet = FALSE)
  "INSTALL_CALL_COMPLETED"
}, error = function(e) paste("INSTALL_ERROR:", conditionMessage(e)))
cat(result, "\n")

ver <- tryCatch(as.character(packageVersion("sceptre", lib.loc = priv_lib)), error = function(e) paste("NOT INSTALLED:", conditionMessage(e)))
cat("sceptre packageVersion:", ver, "\n")

load_ok <- tryCatch({ library(sceptre, lib.loc = priv_lib); TRUE }, error = function(e) { cat("library() FAILED:", conditionMessage(e), "\n"); FALSE })
cat("library(sceptre) succeeded:", load_ok, "\n")
if (load_ok) {
  cat("exported functions include import_data:", exists("import_data"), "\n")
}
