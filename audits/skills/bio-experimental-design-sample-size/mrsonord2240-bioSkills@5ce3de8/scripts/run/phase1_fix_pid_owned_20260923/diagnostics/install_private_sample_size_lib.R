args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 1L)
private_lib <- normalizePath(args[1], winslash = "/", mustWork = TRUE)
.libPaths(c(private_lib, .libPaths()))
bioc_repos <- c(
  CRAN = "https://cloud.r-project.org",
  BioCsoft = "https://bioconductor.org/packages/3.20/bioc",
  BioCann = "https://bioconductor.org/packages/3.20/data/annotation",
  BioCexp = "https://bioconductor.org/packages/3.20/data/experiment"
)
install.packages(c("limma", "edgeR", "qvalue", "PROPER"), lib = private_lib,
                 repos = bioc_repos, dependencies = NA, type = "source")
install.packages(c("pwr", "ssize.fdr", "ssizeRNA"), lib = private_lib,
                 repos = bioc_repos["CRAN"], dependencies = NA, type = "source")
needed <- c("pwr", "ssize.fdr", "ssizeRNA", "limma", "edgeR", "qvalue", "PROPER", "DESeq2")
versions <- vapply(needed, function(pkg) as.character(packageVersion(pkg)), character(1))
stopifnot(all(needed %in% rownames(installed.packages(lib.loc = .libPaths()))))
cat(paste(sprintf("%s=%s", names(versions), versions), collapse = "\n"), "\n")
