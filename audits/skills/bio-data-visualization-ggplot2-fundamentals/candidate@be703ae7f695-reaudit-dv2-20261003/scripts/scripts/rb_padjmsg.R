suppressMessages({library(ggplot2); library(ggrepel); library(patchwork)})
suppressMessages(source("F:/OpenScience/wt/normalize-dv-lane1/skills/bio-data-visualization-ggplot2-fundamentals/scripts/publication_figures.R"))
raw <- read.csv("F:/OpenScience/audit-envs/data-visualization/public-data/differential-expression/airway_dex_deseq2_results.csv")
e <- tryCatch(create_volcano(raw[, c("log2FoldChange", "gene")]), error = function(e) conditionMessage(e)); cat("missing padj ->", gsub("\n", " | ", e), "\n")
