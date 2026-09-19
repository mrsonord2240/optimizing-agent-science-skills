# Re-test with FULL RENDER (ggsave), not just ggplot_build, since is.waive-style
# grid coordinate errors can occur at the draw/grob stage rather than the build stage.
suppressPackageStartupMessages({library(ggtree); library(ggplot2); library(ape)})
tr <- read.tree('data/primates16_true.nwk')

try_layout_render <- function(layout_name) {
  f <- tempfile(fileext = '.png')
  res <- tryCatch({
    p <- ggtree(tr, layout = layout_name) + geom_tiplab(size = 2)
    ggsave(f, p, width = 6, height = 6, dpi = 72)
    sz <- if (file.exists(f)) file.info(f)$size else NA
    paste0('OK (', sz, ' bytes)')
  }, error = function(e) paste('ERROR:', conditionMessage(e)))
  cat(sprintf('render layout=%-12s -> %s\n', layout_name, res))
}

for (lay in c('rectangular', 'slanted', 'equal_angle', 'daylight', 'ape')) {
  try_layout_render(lay)
}

cat('\n--- render geom_tiplab(align = TRUE) on rectangular ---\n')
f2 <- tempfile(fileext = '.png')
res2 <- tryCatch({
  p <- ggtree(tr) + geom_tiplab(align = TRUE, size = 2) + theme_tree2()
  ggsave(f2, p, width = 6, height = 6, dpi = 72)
  paste0('OK (', file.info(f2)$size, ' bytes)')
}, error = function(e) paste('ERROR:', conditionMessage(e)))
cat(res2, '\n')

cat('\nggtree/ggplot2/rlang session info:\n')
cat('ggtree', as.character(packageVersion('ggtree')), '| ggplot2', as.character(packageVersion('ggplot2')),
    '| rlang', as.character(packageVersion('rlang')), '\n')
