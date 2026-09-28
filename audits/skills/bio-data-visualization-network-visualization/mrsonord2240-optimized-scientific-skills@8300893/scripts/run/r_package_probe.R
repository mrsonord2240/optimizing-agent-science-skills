suppressPackageStartupMessages({
  library(igraph)
  library(ggraph)
  library(ggplot2)
})
cat("igraph", as.character(packageVersion("igraph")), "ggraph", as.character(packageVersion("ggraph")), "ggplot2", as.character(packageVersion("ggplot2")), "\n")
cat("package probe completed\n")
