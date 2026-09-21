for (p in c("ggplot2","scales","ggrepel","ggtext","viridis","scico","patchwork","ggrastr","png","dplyr","RColorBrewer","airway","SummarizedExperiment","pdftools","ragg","tibble","rlang","magick","tiff")) {
  v <- tryCatch(as.character(packageVersion(p)), error=function(e) "MISSING")
  cat(sprintf("%-22s %s\n", p, v))
}
cat("R", R.version.string, "\n"); print(.libPaths()); print(capabilities()[c("cairo","png","tiff","jpeg")])
