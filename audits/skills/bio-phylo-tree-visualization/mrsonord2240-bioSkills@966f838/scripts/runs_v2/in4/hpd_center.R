suppressPackageStartupMessages({library(treeio); library(ggtree); library(ggplot2)})
b <- read.beast("../../data/beast_mcc.tree")
td <- as_tibble(b); int <- td[td$node > Ntip(b), ]
ann <- t(sapply(int$`height_0.95_HPD`, identity)); ann <- data.frame(node = int$node, age = int$height, lo = ann[, 1], hi = ann[, 2])
for (cen in c("auto", "height", "height_median")) {
  r <- tryCatch({
    p <- revts(ggtree(b) + geom_range("height_0.95_HPD", center = cen))
    L <- ggplot_build(p)$data[[3]]; L <- L[L$x != L$xend, ]
    d <- data.frame(y = L$y, drawn_lo = pmin(-L$x, -L$xend), drawn_hi = pmax(-L$x, -L$xend))
    yy <- ggplot_build(p)$data[[1]]; yy <- unique(yy[, c("node", "y")])
    d <- merge(merge(d, yy, by = "y"), ann, by = "node")
    d$err_lo <- round(d$drawn_lo - d$lo, 2); d$err_hi <- round(d$drawn_hi - d$hi, 2)
    print(d[, c("node", "age", "lo", "hi", "drawn_lo", "drawn_hi", "err_lo", "err_hi")])
    sprintf("max |error| = %.2f Ma", max(abs(c(d$err_lo, d$err_hi))))
  }, error = function(e) conditionMessage(e))
  cat("center =", cen, "->", r, "\n\n")
}
