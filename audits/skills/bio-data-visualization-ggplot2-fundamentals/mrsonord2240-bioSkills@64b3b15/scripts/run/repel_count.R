# How many ggrepel labels are actually drawn with default max.overlaps = 10 vs Inf (400 synthetic labels in a dense cloud)?
source("F:/OpenScience/audits/bio-data-visualization-ggplot2-fundamentals/run/common.R")
suppressPackageStartupMessages(library(ggrepel))
set.seed(4); d2 <- data.frame(x = rnorm(400, sd = 0.05), y = rnorm(400, sd = 0.05), label = paste0("gene", 1:400))
count_labels <- function(p) {
  W <- character(0); png(tempfile(fileext = ".png"), 500, 400)
  withCallingHandlers(print(p), warning = function(w) { W <<- c(W, conditionMessage(w)); invokeRestart("muffleWarning") },
                      message = function(m) { W <<- c(W, conditionMessage(m)); invokeRestart("muffleMessage") })
  gl <- grid::grid.ls(grid::grid.force(), print = FALSE, grobs = TRUE, viewports = FALSE)
  dev.off()
  cat("grob names sample:", paste(head(unique(sub("[0-9]+$", "", gl$name)), 8), collapse = " | "), "\n")
  list(n_text = sum(grepl("text", gl$name, fixed = TRUE)), n_names = nrow(gl), cond = W)
}
r_def <- count_labels(ggplot(d2, aes(x, y)) + geom_point() + geom_text_repel(aes(label = label)))
r_inf <- count_labels(ggplot(d2, aes(x, y)) + geom_point() + geom_text_repel(aes(label = label), max.overlaps = Inf))
str(r_def); str(r_inf)
