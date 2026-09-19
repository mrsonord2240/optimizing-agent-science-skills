suppressPackageStartupMessages({library(treeio); library(ggtree); library(ggplot2)})
beast <- read.beast('data/beast_mcc.tree')
d <- as_tibble(beast)
hpd_col <- 'height_0.95_HPD'

p_auto   <- ggtree(beast) + geom_range(hpd_col, color = 'red', alpha = 0.4, size = 2, center = 'auto')
p_height <- ggtree(beast) + geom_range(hpd_col, color = 'red', alpha = 0.4, size = 2, center = 'height')

b_auto <- ggplot_build(p_auto)
b_height <- ggplot_build(p_height)
cat('Number of layers (auto):', length(b_auto$data), '| (height):', length(b_height$data), '\n')
for (i in seq_along(b_auto$data)) {
  cat('auto layer', i, 'cols:', paste(colnames(b_auto$data[[i]]), collapse=','), '\n')
}
# The range/error-bar layer should have x + xmin/xmax OR x/xend style columns; print head of any
# layer containing 'x' twice or 'width'.
for (i in seq_along(b_auto$data)) {
  cols <- colnames(b_auto$data[[i]])
  if (any(grepl('xmin|xend|width', cols))) {
    cat('--- candidate range layer', i, '(auto) ---\n')
    print(head(b_auto$data[[i]][, intersect(cols, c('x','xmin','xmax','xend','y','width')), drop=FALSE]))
  }
}
