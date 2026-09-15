# Input 6 (Scope Boundary): unrooted radial drawing; refuse the "tarsiers are basal" caption; rooting/pruning routed to
# tree-manipulation (a minimal outgroup-rooted comparison panel is drawn to show why the claim fails).
suppressPackageStartupMessages({library(treeio); library(ggtree); library(ggplot2); library(patchwork)})
iq <- read.iqtree("../../data/iq/primates16.treefile")
pu <- ggtree(iq, layout = "daylight", size = 0.4) +
  geom_tiplab(aes(label = gsub("_", " ", label)), size = 2.4, fontface = "italic") +
  geom_treescale(width = 0.02, fontsize = 2.4) + hexpand(0.25) + vexpand(0.1) +
  labs(title = "A  Unrooted (daylight) -- no root, no 'basal' taxon")
root_keep <- function(td, og) {   # treeio 1.30 root() returns numeric tip labels; restore by index
  r <- treeio::root(td, outgroup = og, edgelabel = TRUE)
  if (all(grepl("^[0-9]+$", r@phylo$tip.label))) r@phylo$tip.label <- td@phylo$tip.label[as.integer(r@phylo$tip.label)]
  r
}
pr <- ggtree(root_keep(iq, c("Microcebus_murinus", "Otolemur_garnettii")), size = 0.4) +
  geom_tiplab(aes(label = gsub("_", " ", label)), size = 2.4, fontface = "italic") +
  geom_treescale(x = 0, y = -0.5, width = 0.02, fontsize = 2.4) + hexpand(0.4) +
  labs(title = "B  Rooted on Strepsirrhini (outgroup)")
p <- pu + pr + plot_annotation(caption = "Tarsius is sister to Anthropoidea, not 'basal'; a radial layout makes no rooting claim. Synthetic data.")
ggsave("unrooted_vs_rooted.pdf", p, width = 10, height = 5)
ggsave("unrooted_vs_rooted_view.png", p, width = 10, height = 5, dpi = 110)
cat("saved\n")
