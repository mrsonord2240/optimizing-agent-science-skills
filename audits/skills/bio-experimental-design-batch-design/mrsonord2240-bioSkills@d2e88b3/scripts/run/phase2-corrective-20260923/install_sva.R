# Add Bioconductor SVA only to the existing private Linux runtime library.
lib <- "/mnt/openscience/audit-envs/crispr-screen-analyst/tools/designit-linux-runtime/runtime-r-lib-20260923"
options(repos = c(CRAN = "https://cloud.r-project.org"))
if (!requireNamespace("BiocManager", quietly = TRUE, lib.loc = lib)) {
  install.packages("BiocManager", lib = lib)
}
BiocManager::install("sva", lib = lib, ask = FALSE, update = FALSE)
stopifnot(requireNamespace("sva", quietly = TRUE, lib.loc = lib))
cat("sva", as.character(packageVersion("sva", lib.loc = lib)), "installed in", lib, "\n")
