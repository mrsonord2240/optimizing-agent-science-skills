lib <- normalizePath("Rlib_dev"); .libPaths(c(lib, Sys.getenv("R_LIBS_USER"), .libPaths()))
options(repos = c(CRAN = "https://cloud.r-project.org"))
url <- "https://github.com/YuLab-SMU/ggtree/archive/refs/heads/devel.tar.gz"
tf <- file.path(tempdir(), "ggtree-devel.tar.gz"); download.file(url, tf, mode = "wb")
install.packages(tf, repos = NULL, type = "source", lib = lib)
library(ggtree, lib.loc = lib); cat("ggtree dev", as.character(packageVersion("ggtree", lib.loc = lib)), "\n")
suppressPackageStartupMessages({library(treeio); library(ggplot2)})
iq <- read.iqtree("../../data/iq/primates16.treefile")
for (lay in c("slanted", "daylight", "equal_angle")) {
  r <- tryCatch({ p <- ggtree(iq, layout = lay) + geom_tiplab(size = 2); ggsave(paste0("dev_lay_", lay, ".png"), p, width = 5, height = 5, dpi = 80); "OK" },
                error = function(e) conditionMessage(e))
  cat("dev layout", lay, ":", substr(gsub("\n", " ", r), 1, 150), "\n")
}
