# Input 4d: verify the Skill's ggrepel claim ("default max.overlaps=10 silently drops labels; warning only") on real airway data.
suppressMessages({library(ggplot2); library(ggrepel); library(dplyr); library(DESeq2)})
options(warn = 1)
D <- "F:/OpenScience/audits/bio-data-visualization-volcano-and-ma-plots"
code <- readLines(file.path(D, "run/blocks/skill_block02.R"))
code_default <- sub("max.overlaps = Inf, ", "", code, fixed = TRUE)
stopifnot(!identical(code, code_default))
o <- readRDS(file.path(D, "data/airway_objs.rds")); res <- o$apeglm
count_labels <- function(p, file) {
  png(file.path(D, "figs", file), 1400, 1200, res = 180)
  msgs <- character(); withCallingHandlers(print(p), warning = function(w) { msgs <<- c(msgs, conditionMessage(w)); invokeRestart("muffleWarning") }); dev.off()
  msgs
}
eval(parse(text = code_default)); pA <- volcano_plot(res, top_n = 60)
mA <- count_labels(pA, "i4d_repel_default_top60.png")
cat("DEFAULT max.overlaps, top_n=60 -> print-time warnings:", if (length(mA)) paste(unique(mA), collapse = " | ") else "<none>", "\n")
eval(parse(text = code)); pB <- volcano_plot(res, top_n = 60)
mB <- count_labels(pB, "i4d_repel_inf_top60.png")
cat("Inf max.overlaps,     top_n=60 -> print-time warnings:", if (length(mB)) paste(unique(mB), collapse = " | ") else "<none>", "\n")
