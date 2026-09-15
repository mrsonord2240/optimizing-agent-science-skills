# Input 8 (NEW): verify the fixed Skill's ggtree/ggplot2 version block on this stack and its named fallbacks.
suppressPackageStartupMessages({library(ggtree); library(ggplot2); library(treeio); library(ape)})
cat('ggtree', as.character(packageVersion('ggtree')), '| ggplot2', as.character(packageVersion('ggplot2')), '\n')
tr <- read.tree('../../data/primates16_true.nwk')
try_build <- function(lab, expr) {
  r <- tryCatch({ p <- expr; invisible(ggplot_build(p)); png(tempfile(fileext = '.png')); print(p); dev.off(); 'OK' },
                error = function(e) { try(dev.off(), silent = TRUE); paste('ERROR:', conditionMessage(e)) })
  cat(sprintf('%-28s %s\n', lab, substr(r, 1, 110)))
}
for (lay in c('rectangular', 'circular', 'fan', 'slanted', 'equal_angle', 'daylight')) try_build(paste('layout', lay), ggtree(tr, layout = lay))
try_build('geom_tiplab(align = TRUE)', ggtree(tr) + geom_tiplab(align = TRUE))
m <- data.frame(a = runif(Ntip(tr)), row.names = tr$tip.label)
try_build('gheatmap', gheatmap(ggtree(tr), m))
suppressPackageStartupMessages(library(ggtreeExtra))
d <- data.frame(label = tr$tip.label, v = seq_along(tr$tip.label))
try_build('geom_fruit fallback', ggtree(tr, layout = 'circular') + geom_fruit(data = d, geom = geom_tile, mapping = aes(y = label, fill = v)))
png('ape_unrooted.png'); r <- tryCatch({ plot.phylo(tr, type = 'unrooted'); 'OK' }, error = function(e) conditionMessage(e)); dev.off()
cat(sprintf('%-28s %s\n', "ape plot.phylo(type='unrooted')", r))
