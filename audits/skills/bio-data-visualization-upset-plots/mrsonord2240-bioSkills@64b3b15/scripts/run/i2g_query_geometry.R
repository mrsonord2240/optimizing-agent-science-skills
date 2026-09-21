# Query-highlight bars: are the drawn rectangles the width of one bar? Read the highlight layer's xmin/xmax (planted data) on ggplot2 4.0.3.
source("F:/OpenScience/audits/bio-data-visualization-upset-plots/run/helpers.R")
suppressMessages({library(ComplexUpset); library(ggplot2)})
OUT <- "F:/OpenScience/audits/bio-data-visualization-upset-plots/run/out/"
sets <- read_lists("F:/OpenScience/audits/bio-data-visualization-upset-plots/data/planted_sets.tsv"); sets <- sets[c("A","B","C","D","E","F","G")]
el <- unique(unlist(sets)); df <- data.frame(element = el); for (s in names(sets)) df[[s]] <- df$element %in% sets[[s]]
q <- function(int, col) upset_query(intersect = int, color = col, fill = col, only_components = c('intersections_matrix','Intersection size'))
test <- function(label, qs, f) {
  p <- suppressWarnings(upset(df, intersect = names(sets), queries = qs))
  suppressWarnings(ggsave(paste0(OUT, f), p, width = 11, height = 5, dpi = 100))
  subs <- c(p$patches$plots, list(p)); subs <- subs[!sapply(subs, function(s) inherits(s, "spacer"))]
  for (s in subs) { g <- sapply(s$layers, function(l) class(l$geom)[1]); if (sum(g == "GeomBar") >= 1 && !any(suppressWarnings(ggplot_build(s))$data[[which(g == "GeomBar")[1]]]$ymin < 0)) {
     b <- suppressWarnings(ggplot_build(s)); for (li in which(g == "GeomBar")) { d <- b$data[[li]]; cat(sprintf("%s | GeomBar layer %d: %d rows; widths (xmax-xmin): %s\n", label, li, nrow(d), paste(round(unique(d$xmax - d$xmin), 2), collapse=","))) } } }
}
test("1 query A-B", list(q(c('A','B'), '#D55E00')), "i2g_1q_AB.png")
test("1 query A-B-D", list(q(c('A','B','D'), '#0072B2')), "i2g_1q_ABD.png")
test("2 queries A-B, A-B-D", list(q(c('A','B'), '#D55E00'), q(c('A','B','D'), '#0072B2')), "i2g_2q.png")
