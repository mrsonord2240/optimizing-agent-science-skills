# Input 2: layout ratios via panel-background colour bounding boxes in a rendered PNG (independent of grob internals)
source("F:/OpenScience/audits/bio-data-visualization-multipanel-figures/run/common.R")
cols <- c(A = "#ff0000", B = "#00ff00", C = "#0000ff", D = "#ffff00")
mkp <- function(lbl, geom = "pt") {
  df <- data.frame(x = 1:5, y = c(2, 4, 3, 5, 4))
  ggplot(df, aes(x, y)) + geom_point(colour = "black") + theme_classic() + labs(title = lbl) +
    theme(panel.background = element_rect(fill = cols[[lbl]], colour = NA))
}
pA <- mkp("A"); pB <- mkp("B"); pC <- mkp("C"); pD <- mkp("D")
bbox <- function(im, hex) {
  rgb <- col2rgb(hex)[, 1] / 255
  m <- abs(im[,,1] - rgb[1]) < 0.02 & abs(im[,,2] - rgb[2]) < 0.02 & abs(im[,,3] - rgb[3]) < 0.02
  if (!any(m)) return(c(NA, NA, NA, NA))
  r <- which(rowSums(m) > 0); c <- which(colSums(m) > 0)
  c(x0 = min(c), x1 = max(c), y0 = min(r), y1 = max(r))   # px
}
render <- function(fig, name, w = 180, h = 120, dpi = 100) {
  f <- file.path(OUT, paste0(name, ".png")); ggsave(f, fig, width = w, height = h, units = "mm", dpi = dpi)
  im <- png::readPNG(f)
  b <- t(sapply(names(cols), function(k) bbox(im, cols[[k]]))); rownames(b) <- names(cols)
  cbind(b, w = b[, "x1"] - b[, "x0"] + 1, h = b[, "y1"] - b[, "y0"] + 1)
}
show <- function(b, name) { cat("\n#", name, "\n"); print(b) }

# 1. widths = c(2,1)
b <- render(pA + pB + plot_layout(widths = c(2, 1)), "i2_widths"); show(b, "p1 + p2 + plot_layout(widths=c(2,1))")
chk("panel width ratio A:B = 2.0 (+-3%)", abs(b["A","w"] / b["B","w"] - 2) < 0.06)
# 2. mixed (p1 | p2) / p3
b <- render((pA | pB) / pC, "i2_mixed"); show(b, "(A | B) / C")
chk("C spans full width: C panel width ~ A+B panels + gap (>= 1.8x A)", b["C","w"] > 1.8 * b["A","w"])
chk("C sits below A and B (C.y0 > A.y1)", b["C","y0"] > b["A","y1"])
chk("A and B same top (row aligned)", abs(b["A","y0"] - b["B","y0"]) <= 1)
# 3. design string
design <- "
AAB
AAB
CCC
"
b <- render(pA + pB + pC + plot_layout(design = design), "i2_design"); show(b, "design AAB/AAB/CCC")
chk("design: A is 2 columns wide vs B (ratio ~2, +-10%)", abs(b["A","w"] / b["B","w"] - 2) < 0.2)
chk("design: A is 2 rows tall vs C (ratio ~2 in height, +-15%)", abs(b["A","h"] / b["C","h"] - 2) < 0.3)
chk("design: C spans all three columns (>= 2.8x B width)", b["C","w"] > 2.8 * b["B","w"] * 0.95)
# 4. inset
b <- render(pA + inset_element(pB, left = 0.6, bottom = 0.6, right = 1, top = 1), "i2_inset"); show(b, "inset_element(B, .6,.6,1,1) on A")
chk("inset lies in upper-right of A panel", b["B","x0"] > b["A","x0"] + 0.5*(b["A","x1"]-b["A","x0"]) & b["B","y1"] < b["A","y0"] + 0.5*(b["A","y1"]-b["A","y0"]))
cat("inset width/panel width =", round(b["B","w"]/ (b["A","x1"]-b["A","x0"]+1 + 0), 3), " (requested 0.4 of panel, A panel partly covered)\n")
# 5. cowplot
b <- render(plot_grid(pA, pB, pC, pD, ncol = 2, labels = "AUTO", align = "hv", rel_widths = c(1, 2)), "i2_cow_relw"); show(b, "cowplot ncol=2 rel_widths=c(1,2) align=hv")
chk("cowplot rel_widths c(1,2): B panel ~2x A panel wide (+-15%; cell ratio, not panel ratio)", abs(b["B","w"] / b["A","w"] - 2) < 0.3)
top <- plot_grid(pA, pB, ncol = 2, labels = c("A", "B")); bot <- plot_grid(pC, pD, ncol = 2, labels = c("C", "D"))
b <- render(plot_grid(top, bot, nrow = 2, rel_heights = c(1, 1.2)), "i2_cow_nested"); show(b, "cowplot nested rel_heights=c(1,1.2)")
chk("nested: bottom row panel ~1.2x top height (+-15%)", abs(b["C","h"] / b["A","h"] - 1.2) < 0.18)
cat("done\n")
