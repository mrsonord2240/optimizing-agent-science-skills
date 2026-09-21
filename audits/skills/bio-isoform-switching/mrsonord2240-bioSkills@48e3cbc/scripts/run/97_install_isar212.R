# Install IsoformSwitchAnalyzeR 2.12.0 (Bioconductor 3.23 release source tarball, public) into a PRIVATE scratch lib (work/lib212), not the shared R-lib,
# to check by running whether a newer release chooses the DTU test automatically and how it behaves on the same data.
lib <- "F:/OpenScience/audits/bio-isoform-switching/run/work/lib212"
res <- tryCatch(install.packages("F:/OpenScience/audits/bio-isoform-switching/run/work/isar_src/isar_2.12.0.tar.gz", lib = lib, repos = NULL, type = "source", dependencies = FALSE), error = function(e) conditionMessage(e), warning = function(w) conditionMessage(w))
print(res); print(list.files(lib))
.libPaths(c(lib, .libPaths())); print(tryCatch(suppressPackageStartupMessages({ library(IsoformSwitchAnalyzeR); as.character(packageVersion("IsoformSwitchAnalyzeR")) }), error = function(e) paste("LOAD ERROR:", conditionMessage(e))))
