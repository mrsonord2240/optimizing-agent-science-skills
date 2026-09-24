source("F:/OpenScience/audits/bio-data-visualization-multipanel-figures/run/common.R")
suppressPackageStartupMessages(library(gridExtra))
df <- read.csv(file.path(DATA, "i1_df.csv"))
mk <- function(t) ggplot(df, aes(x, y)) + geom_point() + theme_classic() + labs(title = t)
p1 <- mk("ONE"); p2 <- mk("TWO"); p3 <- mk("THREE"); p4 <- mk("FOUR")
# SKILL cowplot block 1 (verbatim args)
combined <- plot_grid(p1, p2, p3, p4, ncol = 2, labels = 'AUTO', label_size = 12, label_fontface = 'bold', align = 'hv', rel_widths = c(1, 1), rel_heights = c(1, 1))
ggsave(file.path(OUT, 'cow1.pdf'), combined, width = 180, height = 140, units = 'mm', device = cairo_pdf)
# block 2 nested
top_row <- plot_grid(p1, p2, ncol = 2, labels = c('A', 'B')); bottom <- plot_grid(p3, p4, ncol = 2, labels = c('C', 'D'))
combined2 <- plot_grid(top_row, bottom, nrow = 2, rel_heights = c(1, 1.2))
ggsave(file.path(OUT, 'cow2.pdf'), combined2, width = 180, height = 140, units = 'mm', device = cairo_pdf)
# lowercase
ggsave(file.path(OUT, 'cow3.pdf'), plot_grid(p1, p2, p3, labels = 'auto'), width = 180, height = 70, units = 'mm', device = cairo_pdf)
# patchwork tag_levels 'A' and 'i'
ggsave(file.path(OUT, 'pw_A.pdf'), (p1 + p2 + p3 + p4) + plot_annotation(tag_levels = 'A'), width = 180, height = 140, units = 'mm', device = cairo_pdf)
ggsave(file.path(OUT, 'pw_i.pdf'), (p1 + p2 + p3) + plot_annotation(tag_levels = 'i'), width = 180, height = 70, units = 'mm', device = cairo_pdf)
# gridExtra (named in description; no example in SKILL.md): does grid.arrange/arrangeGrob work with ggplot objects + layout_matrix
ga <- arrangeGrob(p1, p2, p3, layout_matrix = rbind(c(1, 2), c(3, 3)))
ggsave(file.path(OUT, 'gridextra.pdf'), ga, width = 180, height = 140, units = 'mm', device = cairo_pdf)
cat("done\n")
