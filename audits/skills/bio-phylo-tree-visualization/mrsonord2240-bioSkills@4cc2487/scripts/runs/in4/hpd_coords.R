# second, numeric check that the drawn HPD bars equal the annotated intervals
suppressPackageStartupMessages({library(treeio); library(ggtree); library(ggplot2)})
b <- read.beast("../../data/beast_mcc.tree")
p <- revts(ggtree(b) + geom_range("height_0.95_HPD"))
bd <- ggplot_build(p)$data
for (i in seq_along(bd)) cat("layer", i, ":", paste(names(bd[[i]]), collapse = " "), "\n")
L <- bd[[which(sapply(bd, function(d) "xmin" %in% names(d) || ("x" %in% names(d) && "xend" %in% names(d) && any(d$x != d$xend))))[1]]]
td <- as_tibble(b)
hp <- do.call(rbind, lapply(td$`height_0.95_HPD`, function(v) if (length(v) == 2) v else c(NA, NA)))
ref <- data.frame(node = td$node, hpd_lo = hp[, 1], hpd_hi = hp[, 2])
xs <- intersect(c("node", "x", "xend", "xmin", "xmax", "y"), names(L))
m <- merge(L[, xs], ref, by = "node")
print(m[m$node > Ntip(b), ])
R3 <- bd[[3]]; R3 <- R3[order(R3$y), c("y", "x", "xend")]
cat("range layer (x = -upper HPD age, xend = -lower HPD age):\n"); print(R3)
cat("annotated HPDs (sorted by lower):\n"); print(ref[ref$node > Ntip(b), ][order(ref$hpd_lo[ref$node > Ntip(b)]), ])
