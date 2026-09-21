# Input 4 (edge): every "Per-Method Failure Modes" claim in SKILL.md, produced as PDF+PNG(72 dpi) for python analysis
source("F:/OpenScience/audits/bio-data-visualization-multipanel-figures/run/common.R")
set.seed(3)
df <- data.frame(x = rnorm(60), g = rep(c("ctrl", "trt"), 30)); df$y <- df$x + rnorm(60, 0, .5)
bg <- function(col) theme(panel.background = element_rect(fill = col, colour = NA))
save2 <- function(fig, name, w = 180, h = 70) {
  ggsave(file.path(OUT, paste0(name, ".pdf")), fig, width = w, height = h, units = "mm", device = cairo_pdf)
  ggsave(file.path(OUT, paste0(name, ".png")), fig, width = w, height = h, units = "mm", dpi = 72)
}
# F1 tag alignment with different y-label widths
short <- ggplot(df, aes(x, y)) + geom_point() + theme_classic() + labs(title = "P1", y = "y") + bg("#ff0000")
long  <- ggplot(df, aes(x, y * 1000)) + geom_point() + theme_classic() + labs(title = "P2", y = "a rather long y axis label (units)") + bg("#00ff00")
save2((short | long) + plot_annotation(tag_levels = "a"), "f1_default")
save2((short | long) + plot_annotation(tag_levels = "a", theme = theme(plot.tag.position = c(0.02, 0.98))), "f1_fix_annot")
save2((short | long) + plot_annotation(tag_levels = "a") & theme(plot.tag.position = c(0.02, 0.98)), "f1_fix_amp")
save2((short | long) + plot_annotation(tag_levels = "a") & theme(plot.tag.position = c(0.02, 0.98)) & theme(plot.tag = element_text(face = "bold", size = 8)), "f1_fix_amp_bold8")
# F2 shared legend
mk <- function(pal, title) ggplot(df, aes(x, y, colour = g)) + geom_point() + scale_colour_manual(values = pal) + theme_classic() + labs(title = title)
same <- c(ctrl = "#1b9e77", trt = "#d95f02"); other <- c(ctrl = "#0000ff", trt = "#ff00ff")
save2((mk(same, "S1") | mk(same, "S2")) + plot_layout(guides = "collect"), "f2_same")
save2((mk(same, "S1") | mk(other, "S2")) + plot_layout(guides = "collect"), "f2_diffpal")
save2((mk(same, "S1") | (mk(other, "S2") & theme(legend.position = "none"))) + plot_layout(guides = "collect"), "f2_dropone")
# F2b: same palette but one panel uses fill= instead of colour= (a common cause of unmerged legends)
pf <- ggplot(df, aes(g, y, fill = g)) + geom_boxplot() + scale_fill_manual(values = same) + theme_classic() + labs(title = "S3")
save2((mk(same, "S1") | pf) + plot_layout(guides = "collect"), "f2_colour_vs_fill")
# F4 default device
fig <- (short | long)
ggsave(file.path(OUT, "f4_defaultdev.pdf"), fig, width = 180, height = 70, units = "mm")
# F3 units default
r <- try(ggsave(file.path(OUT, "f3_inches.pdf"), fig, width = 180, height = 140), silent = TRUE)
cat("F3 ggsave(width=180,height=140) default units ->", if (inherits(r, "try-error")) paste("ERROR:", conditionMessage(attr(r, "condition"))) else "no error", "\n")
r <- ggsave(file.path(OUT, "f3_inches_nolimit.pdf"), fig, width = 180, height = 140, limitsize = FALSE)
cat("f3 nolimit file bytes", file.size(file.path(OUT, "f3_inches_nolimit.pdf")), "\n")
# F5 cowplot align
sh <- ggplot(df, aes(x, y)) + geom_point() + theme_classic() + labs(title = "N1", y = "y") + bg("#ff0000")
wd <- ggplot(df, aes(x, y * 1000)) + geom_point() + theme_classic() + labs(title = "N2", y = "long axis label here") + bg("#00ff00")
for (a in c("none", "v", "h", "hv")) save2(plot_grid(sh, wd, ncol = 1, align = a, axis = if (a == "none") "" else "lr"), paste0("f5_cow_ncol1_", a), 90, 120)
for (a in c("none", "v", "hv")) save2(plot_grid(sh, wd, ncol = 1, align = a), paste0("f5b_cow_noaxis_", a), 90, 120)
# F6 axes collect, shared scales, 2x2 with x,y same everywhere
q <- function(t) ggplot(df, aes(x, y)) + geom_point() + theme_classic() + labs(title = t)
save2((q("Q1") | q("Q2")) / (q("Q3") | q("Q4")), "f6_nocollect", 180, 140)
save2(((q("Q1") | q("Q2")) / (q("Q3") | q("Q4"))) + plot_layout(axes = "collect"), "f6_axes", 180, 140)
save2(((q("Q1") | q("Q2")) / (q("Q3") | q("Q4"))) + plot_layout(axes = "collect", axis_titles = "collect"), "f6_axes_titles", 180, 140)
save2(((q("Q1") | q("Q2")) / (q("Q3") | q("Q4"))) + plot_layout(axis_titles = "collect"), "f6_titles_only", 180, 140)
cat("done\n")
