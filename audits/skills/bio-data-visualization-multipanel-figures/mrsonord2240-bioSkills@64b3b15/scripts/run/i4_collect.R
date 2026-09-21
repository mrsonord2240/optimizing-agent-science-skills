# Does axes='collect' work, and for which composition forms? (all panels share identical x,y scales)
source("F:/OpenScience/audits/bio-data-visualization-multipanel-figures/run/common.R")
set.seed(3); df <- data.frame(x = rnorm(60)); df$y <- df$x + rnorm(60, 0, .5)
q <- function(t) ggplot(df, aes(x, y)) + geom_point() + theme_classic() + labs(title = t)
save2 <- function(fig, name, w = 180, h = 140) ggsave(file.path(OUT, paste0(name, ".pdf")), fig, width = w, height = h, units = "mm", device = cairo_pdf)
L <- list(q("Q1"), q("Q2"), q("Q3"), q("Q4"))
col <- plot_layout(axes = "collect", axis_titles = "collect")
save2(q("Q1") + q("Q2") + col, "c_row2", 180, 70)                           # simple 2 side by side
save2(q("Q1") / q("Q2") + col, "c_col2", 90, 140)                           # simple 2 stacked
save2(wrap_plots(L, ncol = 2) + col, "c_wrap22")                            # flat 2x2
save2(q("Q1") + q("Q2") + q("Q3") + q("Q4") + plot_layout(ncol = 2, axes = "collect", axis_titles = "collect"), "c_plus_ncol2")
save2((q("Q1") + q("Q2")) / (q("Q3") + q("Q4")) + col, "c_nested_top")     # the Skill's own form (nested), layout at top level
save2((q("Q1") + q("Q2") + col) / (q("Q3") + q("Q4") + col) + col, "c_nested_all")   # collect set at every level
save2((q("Q1") + q("Q2")) / (q("Q3") + q("Q4")) & theme(), "c_nested_nolayout")
