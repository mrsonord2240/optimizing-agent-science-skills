# argparse (+ findpython) into a PRIVATE library under the audit folder (no change to the shared R-lib). Needed only by FLAIR's diffSplice_drimSeq.R (`flair diffSplice --test`).
lib <- "F:/OpenScience/audits/bio-long-read-splicing/run/out/rlib_extra"
dir.create(lib, showWarnings = FALSE, recursive = TRUE)
.libPaths(c(lib, .libPaths()))
install.packages(c("argparse", "findpython"), lib = lib, repos = "https://cloud.r-project.org", type = "binary")
print(sapply(c("argparse", "findpython", "data.table", "DRIMSeq"), function(p) tryCatch(as.character(packageVersion(p)), error = function(e) "MISSING")))
