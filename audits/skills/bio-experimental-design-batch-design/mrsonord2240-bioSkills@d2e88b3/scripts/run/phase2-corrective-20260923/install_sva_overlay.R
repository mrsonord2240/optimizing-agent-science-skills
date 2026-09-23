base <- "/mnt/openscience/audit-envs/crispr-screen-analyst/tools/designit-linux-runtime/runtime-r-lib-20260923"
overlay <- "/mnt/openscience/audit-envs/crispr-screen-analyst/tools/designit-linux-runtime/runtime-sva-overlay-20260923"
dir.create(overlay, recursive = TRUE, showWarnings = FALSE)
.libPaths(c(overlay, base, .Library))
options(repos = c(CRAN = "https://cloud.r-project.org"))
install.packages("BH", lib = overlay)
BiocManager::install(c("BiocParallel", "sva"), lib = overlay, ask = FALSE, update = FALSE)
stopifnot(requireNamespace("sva", quietly = TRUE), requireNamespace("limma", quietly = TRUE))
cat("sva=", as.character(packageVersion("sva")), " BiocParallel=", as.character(packageVersion("BiocParallel")), "\n", sep = "")
