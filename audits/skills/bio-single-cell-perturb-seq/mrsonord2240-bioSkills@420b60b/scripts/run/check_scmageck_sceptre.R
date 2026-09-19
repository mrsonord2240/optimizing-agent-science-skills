.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
cat("R version:", R.version.string, "\n")

cran_pkgs <- rownames(available.packages(repos = "https://cran.r-project.org"))
cat("scMAGeCK on CRAN:", "scMAGeCK" %in% cran_pkgs, "\n")
cat("sceptre on CRAN:", "sceptre" %in% cran_pkgs, "\n")

if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager", repos="https://cran.r-project.org")
bioc_pkgs <- tryCatch(rownames(BiocManager::available()), error = function(e) character(0))
cat("scMAGeCK on Bioconductor release:", "scMAGeCK" %in% bioc_pkgs, "\n")
cat("sceptre on Bioconductor release:", "sceptre" %in% bioc_pkgs, "\n")

cat("sceptre installed here (packageVersion):\n")
res <- tryCatch(as.character(packageVersion("sceptre")), error = function(e) paste("NOT INSTALLED:", conditionMessage(e)))
print(res)
