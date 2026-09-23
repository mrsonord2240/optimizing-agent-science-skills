private_lib <- "F:/OpenScience/audits/bio-single-cell-perturb-seq/run/p1_corrective_20260923/R-private-lib"
dir.create(private_lib, recursive = TRUE, showWarnings = FALSE)
.libPaths(c(private_lib, "F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib", .libPaths()))
source_dir <- "F:/OpenScience/audits/bio-single-cell-perturb-seq/run/p1_corrective_20260923/sceptre-source"
tarball <- file.path(tempdir(), "sceptre_0.99.0.tar.gz")
old_wd <- getwd()
setwd(dirname(source_dir))
on.exit(setwd(old_wd), add = TRUE)
status <- system2(file.path(R.home("bin"), "R"),
                  c("CMD", "build", "--no-build-vignettes", basename(source_dir)),
                  env = paste0("R_LIBS=", paste(.libPaths(), collapse = .Platform$path.sep)))
stopifnot(status == 0)
file.copy(file.path(dirname(source_dir), "sceptre_0.99.0.tar.gz"), tarball, overwrite = TRUE)
install.packages(tarball, repos = NULL, type = "source", lib = private_lib,
                 INSTALL_opts = c("--no-byte-compile", "--no-clean-on-error"))
library(sceptre)
stopifnot(as.character(packageVersion("sceptre")) == "0.99.0")
cat("PASS no-byte-compile private sceptre=", as.character(packageVersion("sceptre")), "\n", sep = "")
