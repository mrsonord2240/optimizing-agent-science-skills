# Input 2, R route from SKILL.md: treeio read.iqtree splits SH-aLRT/UFBoot. SYNTHETIC data.
suppressPackageStartupMessages({library(treeio); library(ape)})
x <- read.iqtree("../../data/iq10.treefile")
tb <- as_tibble(x)
cat("columns:", paste(names(tb), collapse = ", "), "\n")
print(as.data.frame(tb[!is.na(tb[[ncol(tb)]]), ]))
a <- read.tree("../../data/iq10.treefile")
cat("ape node.label:", paste(a$node.label, collapse = " "), "\n")
