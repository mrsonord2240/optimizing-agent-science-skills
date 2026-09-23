lib <- "/home/sci/.local/share/openscience-pathway-enrichment-r-20260923"
pkgconfig <- "/home/sci/.local/share/openscience-pathway-enrichment-r-20260923-deps/pkgconfig"
dir.create(lib, recursive = TRUE, showWarnings = FALSE)
.libPaths(c(lib, .libPaths()))
Sys.setenv(PKG_CONFIG_PATH = pkgconfig)
options(repos = c(CRAN = "https://cloud.r-project.org"), timeout = 900)
install.packages("gdtools", lib = lib)
BiocManager::install(c("ggiraph", "ggtree", "enrichplot", "clusterProfiler"), lib = lib, ask = FALSE, update = FALSE)
for (pkg in c("clusterProfiler", "enrichplot", "org.Hs.eg.db", "GOSemSim", "ggplot2", "ggridges", "ggarchery")) {
  stopifnot(requireNamespace(pkg, quietly = TRUE))
  cat(pkg, "=", as.character(packageVersion(pkg)), "\n", sep = "")
}
