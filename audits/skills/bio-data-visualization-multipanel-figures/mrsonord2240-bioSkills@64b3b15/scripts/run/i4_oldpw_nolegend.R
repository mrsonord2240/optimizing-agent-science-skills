# Run under a specific patchwork version: PWLIB env var = lib dir. Tests (a) plot_annotation(theme=tag) honoured? (b) axes='collect' accepted/ignored?
lib <- Sys.getenv("PWLIB"); tagp <- Sys.getenv("TAGP", "x")
.libPaths(c(lib, .libPaths()))
source("F:/OpenScience/audits/bio-data-visualization-multipanel-figures/run/common.R")
cat("patchwork", as.character(packageVersion("patchwork")), " ggplot2", as.character(packageVersion("ggplot2")), "\n")
df <- read.csv(file.path(DATA, "i1_df.csv"))
p1 <- ggplot(df, aes(x, y)) + geom_point() + theme_classic() + labs(title = "SCATTER")
p4 <- ggplot(df, aes(x, y)) + geom_point() + theme_classic() + labs(title = "COLOR")
tagw <- Sys.getenv("TAGW", "old")
for (sz in c(6, 20)) {
  f <- (p1 + p4) + plot_annotation(tag_levels = 'a', theme = theme(plot.tag = element_text(face = 'bold', size = sz)))
  fn <- file.path(OUT, sprintf("pw%s_tag_%d.pdf", tagw, sz))
  ggsave(fn, f, width = 180, height = 70, units = 'mm', device = cairo_pdf)
}
r <- try({ f <- (p1 / p4) + plot_layout(axes = 'collect', axis_titles = 'collect', guides='collect'); ggsave(file.path(OUT, sprintf("pw%s_collect.pdf", tagw)), f, width = 90, height = 120, units = 'mm', device = cairo_pdf); "OK" }, silent = TRUE)
cat("axes='collect' call result:", if (inherits(r, "try-error")) paste("ERROR:", conditionMessage(attr(r, "condition"))) else r, "\n")
