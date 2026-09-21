# Run the shipped example verbatim (each top-level expression evaluated in order) on SYNTHETIC data
suppressPackageStartupMessages(library(ggplot2))
D <- "F:/OpenScience/audits/bio-data-visualization-statistical-annotation"
df <- read.csv(file.path(D, "data", "three_group.csv"))
df_paired <- read.csv(file.path(D, "data", "paired.csv"))
df_nested <- read.csv(file.path(D, "data", "nested.csv"))
setwd(file.path(D, "run", "scratch"))
exprs <- parse("statanno_phd.R", keep.source = FALSE)
k <- 0
for (e in exprs) {
  txt <- paste(deparse(e)[1], collapse = "")
  r <- tryCatch(withCallingHandlers(eval(e, globalenv()), warning = function(w) {cat("WARNING:", conditionMessage(w), "\n"); invokeRestart("muffleWarning")}),
                error = function(err) { cat("ERROR at [", substr(txt, 1, 70), "]:", conditionMessage(err), "\n"); NULL })
  if (inherits(r, "ggplot")) { k <- k + 1; f <- file.path(D, "figs", sprintf("ex_plot%d.png", k)); tryCatch({ggsave(f, r, width = 6, height = 5, dpi = 100); cat("saved", f, "\n")}, error = function(err) cat("SAVE ERROR:", conditionMessage(err), "\n")) }
}
cat("---- objects\n"); print(shapiro_results); print(stat_test); print(effect_sizes)
cat("pdf exists:", file.exists("stat_annotated.pdf"), file.size("stat_annotated.pdf"), "\n")
