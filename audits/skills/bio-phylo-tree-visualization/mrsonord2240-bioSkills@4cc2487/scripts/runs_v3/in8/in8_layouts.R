# Recheck the Version Compatibility block's layout-failure claims properly, with
# geom_tiplab attached (as a real figure would have), since a bare ggtree(layout=)
# call with no other layers may not exercise the same fortify/is.waive path.
suppressPackageStartupMessages({library(ggtree); library(ggplot2); library(ape)})
tr <- read.tree('data/primates16_true.nwk')

try_layout <- function(layout_name) {
  res <- tryCatch({
    p <- ggtree(tr, layout = layout_name) + geom_tiplab(size = 2)
    ggplot_build(p)
    'OK'
  }, error = function(e) paste('ERROR:', conditionMessage(e)))
  cat(sprintf('layout=%-12s -> %s\n', layout_name, res))
}

for (lay in c('rectangular', 'circular', 'fan', 'slanted', 'equal_angle', 'daylight', 'ape', 'unrooted')) {
  try_layout(lay)
}

cat('\n--- geom_tiplab(align = TRUE) on rectangular ---\n')
res_align <- tryCatch({
  p <- ggtree(tr) + geom_tiplab(align = TRUE, size = 2)
  ggplot_build(p)
  'OK'
}, error = function(e) paste('ERROR:', conditionMessage(e)))
cat(res_align, '\n')
