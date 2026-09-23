suppressPackageStartupMessages({library(treeio); library(ggtree); library(ggtreeExtra); library(ggplot2); library(ape)})

treefile <- '/mnt/openscience/audits/bio-phylo-tree-visualization/data/tree.treefile'
nwk <- '/mnt/openscience/audits/bio-phylo-tree-visualization/data/tree.nwk'
out_dir <- '/mnt/openscience/audits/bio-phylo-tree-visualization/run'

iq <- read.iqtree(treefile)
root_keep <- function(td, outgroup) {
  r <- treeio::root(td, outgroup = outgroup, edgelabel = TRUE)
  if (all(grepl('^[0-9]+$', r@phylo$tip.label))) r@phylo$tip.label <- td@phylo$tip.label[as.integer(r@phylo$tip.label)]
  r
}
iq_r <- root_keep(iq, c('OutA', 'OutB'))
p <- ggtree(iq_r, size = 0.4) +
  geom_tiplab(size = 2.6, offset = 0.003) +
  geom_nodelab(aes(label = ifelse(is.na(UFboot), '', paste0(SH_aLRT, '/', UFboot))), size = 2, hjust = 1.1, vjust = -0.5) +
  geom_treescale(width = 0.02, fontsize = 2.4)
meta <- data.frame(label = iq_r@phylo$tip.label, trait = seq_along(iq_r@phylo$tip.label))
p2 <- p + geom_fruit(data = meta, geom = geom_tile, mapping = aes(y = label, fill = trait), pwidth = 0.06, offset = 0.08)
pdf_path <- file.path(out_dir, 'ggtree_composite.pdf')
ggsave(pdf_path, p2, width = 180, height = 150, units = 'mm')
stopifnot(file.exists(pdf_path), file.info(pdf_path)$size > 1000L, length(ggplot_build(p2)$data) >= 5L)

tr <- read.tree(nwk)
ape_path <- file.path(out_dir, 'ape_unrooted.pdf')
pdf(ape_path, width = 7, height = 7)
plot(tr, type = 'unrooted', cex = 0.6, no.margin = TRUE)
add.scale.bar(cex = 0.7, lwd = 1)
dev.off()
stopifnot(file.exists(ape_path), file.info(ape_path)$size > 1000L)
cat(sprintf('ASSERT ggtree_layers=%d composite_bytes=%d ape_bytes=%d\n', length(ggplot_build(p2)$data), file.info(pdf_path)$size, file.info(ape_path)$size))
