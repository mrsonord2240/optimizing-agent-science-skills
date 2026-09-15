# Input 3 (Edge) adapted output: 320 tips -> circular layout (Skill threshold 150-500), host ring + year ring, scale bar
suppressPackageStartupMessages({library(ggtree); library(treeio); library(ggplot2); library(ggtreeExtra); library(ggnewscale)})
tr   <- read.tree("../../data/big320.nwk")
meta <- read.delim("../../data/big320_meta.tsv")
cat("tips:", Ntip(tr), " ultrametric:", ape::is.ultrametric(tr, tol = 1e-6), "\n")

p <- ggtree(tr, layout = "circular", size = 0.15) %<+% meta +
  geom_tiplab(size = 0.9, offset = 0.9, linesize = 0.05) +
  geom_treescale(x = 0, y = 0, width = 1, fontsize = 2.5, linesize = 0.4)
p <- p + geom_fruit(geom = geom_tile, mapping = aes(y = label, fill = host), width = 0.6, offset = 0.04) +
  scale_fill_brewer(palette = "Set2", name = "Host") +
  new_scale_fill() +
  geom_fruit(geom = geom_tile, mapping = aes(y = label, fill = year), width = 0.6, offset = 0.04) +
  scale_fill_viridis_c(name = "Sampling year") +
  labs(caption = "Circular layout (rooted; centre = root). Scale bar in simulation branch-length units. Inner ring host, outer ring year. Synthetic data.") +
  theme(legend.position = "right", plot.caption = element_text(size = 7))
ggsave("big320_circular.pdf", p, width = 10, height = 9)
ggsave("big320_circular_view.png", p, width = 10, height = 9, dpi = 110)
cat("saved big320_circular.pdf\n")
