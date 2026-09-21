# Extract and run every R code block in SKILL.md verbatim on SYNTHETIC three_group data
suppressPackageStartupMessages({library(ggplot2); library(dplyr)})
D <- "F:/OpenScience/audits/bio-data-visualization-statistical-annotation"
md <- paste(readLines(file.path(D, "run/skill/data-visualization/statistical-annotation/SKILL.md"), encoding = "UTF-8"), collapse = "\n")
m <- gregexpr("(?s)```r\n(.*?)```", md, perl = TRUE)
blocks <- regmatches(md, m)[[1]]; blocks <- sub("^```r\n", "", sub("```$", "", blocks))
cat("R blocks:", length(blocks), "\n")
df <- read.csv(file.path(D, "data/three_group.csv"))
pairs <- list(c('Control','Treatment'), c('Control','Vehicle'), c('Treatment','Vehicle'))
for (i in seq_along(blocks)) {
  cat("\n=== block", i, ":", strsplit(blocks[i], "\n")[[1]][1:2], "\n")
  env <- globalenv()
  res <- tryCatch({ exprs <- parse(text = blocks[i]); out <- NULL; for (e in exprs) { out <- withVisible(eval(e, env)); if (out$visible && inherits(out$value, "ggplot")) { f <- file.path(D, "figs", sprintf("skillblock%d.png", i)); ggsave(f, out$value, width = 6, height = 5, dpi = 100); cat("saved", f, "\n") } else if (out$visible) print(out$value) }; "OK" },
    error = function(e) paste("ERROR:", conditionMessage(e)))
  cat("status:", res, "\n")
}
# block 4 with 3 groups fails? try with only the two groups
cat("\n=== ggsignif block on 2-group subset\n")
df2 <- df[df$group %in% c("Control","Treatment"),]
library(ggsignif)
p <- ggplot(df2, aes(group, value, fill = group)) + geom_boxplot() +
  geom_signif(comparisons = list(c('Control','Treatment')), test = 'wilcox.test', map_signif_level = TRUE, step_increase = 0.1) +
  scale_fill_manual(values = c('#0072B2', '#D55E00'))
ggsave(file.path(D, "figs", "skill_ggsignif_2grp.png"), p, width = 4, height = 4, dpi = 100)
print(ggplot_build(p)$data[[2]]$annotation[1]); cat("truth wilcox p:", wilcox.test(value~group, df2)$p.value, "\n")
