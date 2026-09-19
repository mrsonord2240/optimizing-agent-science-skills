suppressPackageStartupMessages({library(treeio); library(ggtree); library(ggplot2)})
iq <- read.iqtree("../../data/iq/primates16.treefile")
for (lay in c("rectangular", "slanted", "circular", "fan", "equal_angle", "daylight", "ape")) {
  r <- tryCatch({ p <- ggtree(iq, layout = lay) + geom_tiplab(size = 2); ggsave(paste0("lay_", lay, ".png"), p, width = 4, height = 4, dpi = 60); "OK" },
                error = function(e) paste(conditionMessage(e), if (!is.null(e$parent)) conditionMessage(e$parent)))
  cat("layout", lay, ":", gsub("\n", " ", substr(r, 1, 160)), "\n")
}
