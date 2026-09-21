# Input 1: SKILL.md patchwork 2x2 block, run as written on synthetic data (df has x,y,group,value)
source("F:/OpenScience/audits/bio-data-visualization-multipanel-figures/run/common.R")
cat("patchwork", as.character(packageVersion("patchwork")), " ggplot2", as.character(packageVersion("ggplot2")), "\n")
set.seed(1)
n <- 200
df <- data.frame(x = rnorm(n), group = rep(c("ctrl", "trt"), each = n/2))
df$y <- 0.8 * df$x + rnorm(n, 0, .6) + ifelse(df$group == "trt", 1, 0)
df$value <- df$y
write.csv(df, file.path(DATA, "i1_df.csv"), row.names = FALSE)

# --- SKILL.md block, verbatim except titles added so each panel is identifiable in the PDF text layer
p1 <- ggplot(df, aes(x, y)) + geom_point() + theme_classic() + labs(title = "SCATTER")
p2 <- ggplot(df, aes(group, value)) + geom_boxplot() + theme_classic() + labs(title = "BOX")
p3 <- ggplot(df, aes(x)) + geom_histogram() + theme_classic() + labs(title = "HIST")
p4 <- ggplot(df, aes(x, y, color = group)) + geom_point() + theme_classic() + labs(title = "COLOR")

fig <- (p1 + p2) / (p3 + p4) +
    plot_annotation(tag_levels = 'a',
                    theme = theme(plot.tag = element_text(face = 'bold', size = 10))) +
    plot_layout(guides = 'collect',         # share legends
                axes = 'collect',           # share axes (patchwork >= 1.2.0)
                axis_titles = 'collect')

ggsave(file.path(OUT, 'i1_figure1.pdf'), fig, width = 180, height = 140, units = 'mm', device = cairo_pdf)
ggsave(file.path(OUT, 'i1_figure1.png'), fig, width = 180, height = 140, units = 'mm', dpi = 300)

# ---- assertions on content
cat("\nclass:", class(fig), "\n")
chk("4 panels in the patchwork object", length(fig$patches$plots) + 1 == 4)
g <- patchwork::patchworkGrob(fig)
nm <- vapply(g$grobs, function(z) z$name, "")
cat("grob names (unique kinds):", paste(sort(unique(sub("-[0-9]+.*$", "", nm))), collapse = ", "), "\n")
cat("panel grobs:", sum(grepl("^panel", nm)), " guide-box grobs:", sum(grepl("guide-box", nm)), " tag grobs:", sum(grepl("tag", nm)), "\n")
chk("exactly one legend after guides='collect'", sum(grepl("guide-box", nm) & !vapply(g$grobs, function(z) inherits(z, "zeroGrob"), TRUE)) == 1)
cat("xlab grobs:", sum(grepl("^xlab", nm)), " ylab grobs:", sum(grepl("^ylab", nm)), "\n")
cat("axis grobs:", paste(nm[grepl("axis", nm)], collapse=" | "), "\n")
info <- png_info(file.path(OUT, 'i1_figure1.png'))
cat(sprintf("PNG expected at 300 dpi: %d x %d\n", round(180/25.4*300), round(140/25.4*300)))
chk("PNG pixel size matches 180x140 mm at 300 dpi (+-2px)", abs(info$w - round(180/25.4*300)) <= 2 && abs(info$h - round(140/25.4*300)) <= 2)
chk("PNG not blank", info$nonwhite > 0.02)
