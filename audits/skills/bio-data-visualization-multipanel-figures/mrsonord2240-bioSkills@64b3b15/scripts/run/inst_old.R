# install old patchwork versions into audit-private libs (does not touch any shared lib)
base <- "F:/OpenScience/audits/bio-data-visualization-multipanel-figures"
libs <- c("1.2.0" = file.path(base, "lib-pw120"), "1.1.3" = file.path(base, "lib-pw113"))
for (v in names(libs)) {
  install.packages(paste0("https://cran.r-project.org/src/contrib/Archive/patchwork/patchwork_", v, ".tar.gz"), repos = NULL, type = "source", lib = libs[[v]], quiet = TRUE)
  cat(v, "->", as.character(packageVersion("patchwork", lib.loc = libs[[v]])), "\n")
}
