# Input 5 (Stress): publication Figure 2 -- rooted IQ-TREE tree, dual SH-aLRT/UFBoot support with legend,
# joint-rule node symbols, collapsed variant, Catarrhini clade bar, diet heatmap + mass bars, scale bar, 180 mm vector PDF.
suppressPackageStartupMessages({library(treeio); library(ggtree); library(ggplot2); library(ggtreeExtra); library(ggnewscale)})
iq <- read.iqtree("../../data/iq/primates16.treefile")
# treeio 1.30 root() on treedata keeps support on the right split but returns tip labels as "1","2",...
# (verified in runs/env/debug.log); restore names by original index.
root_keep <- function(td, og) {
  r <- treeio::root(td, outgroup = og, edgelabel = TRUE)
  if (all(grepl("^[0-9]+$", r@phylo$tip.label))) r@phylo$tip.label <- td@phylo$tip.label[as.integer(r@phylo$tip.label)]
  r
}
iq_r <- root_keep(iq, c("Microcebus_murinus", "Otolemur_garnettii"))

# verify support stayed on its bipartition after rooting (compare with unrooted input)
splitkey <- function(tips, all) { s <- sort(tips); o <- sort(setdiff(all, tips))
  if (length(o) < length(s) || (length(o) == length(s) && o[1] < s[1])) s <- o; paste(s, collapse = ",") }
smap <- function(td) { ph <- as.phylo(td); tb <- as_tibble(td); out <- c()
  for (i in which(tb$node > Ntip(ph) & !is.na(tb$UFboot))) {
    tips <- ph$tip.label[unlist(phangorn::Descendants(ph, tb$node[i], "tips"))]
    out[splitkey(tips, ph$tip.label)] <- paste0(tb$SH_aLRT[i], "/", tb$UFboot[i]) }
  out }
b4 <- smap(iq); af <- smap(iq_r)
cat("support labels on the same bipartition after rooting:", sum(b4[names(af)] == af, na.rm = TRUE), "of", length(b4), "\n")

traits <- read.delim("../../data/primates16_traits.tsv")
ring <- data.frame(label = traits$label, Diet = traits$diet, mass = traits$log10_mass_g)  # geom_fruit copy, names distinct from %<+% join
d <- as_tibble(iq_r)
cat_node <- ape::getMRCA(as.phylo(iq_r), c("Homo_sapiens", "Macaca_mulatta"))
cat("Catarrhini MRCA node:", cat_node, "\n")

base_plot <- function(tr) {
  ggtree(tr, size = 0.4) %<+% traits +
    # align = TRUE removed: its dotted leaders use geom_segment2, which fails with "could not find function is.waive"
    # (ggtree 3.14 + ggplot2 4.0.3), see fig2.log of the second run
    geom_tiplab(aes(label = gsub("_", " ", label)), fontface = "italic", size = 2.6, offset = 0.003) +
    geom_nodepoint(aes(subset = !isTip & !is.na(UFboot), fill = (SH_aLRT >= 80 & UFboot >= 95)), shape = 21, size = 1.8) +
    geom_nodelab(aes(label = ifelse(is.na(UFboot), "", paste0(SH_aLRT, "/", UFboot))), hjust = 1.15, vjust = -0.55,
                 size = 2.0) +
    scale_fill_manual(values = c(`TRUE` = "black", `FALSE` = "white"),
                      labels = c(`TRUE` = "SH-aLRT >= 80 and UFBoot >= 95", `FALSE` = "below joint threshold"),
                      name = "Node support (SH-aLRT / UFBoot)") +
    geom_treescale(x = 0, y = 0.2, width = 0.02, fontsize = 2.4, linesize = 0.6, offset = 0.25) +
    geom_cladelab(node = cat_node, label = "Catarrhini", offset = 0.075, barsize = 0.8, fontsize = 2.8, angle = 90,
                  hjust = 0.5, offset.text = 0.005)
}
p <- base_plot(iq_r)
diet <- data.frame(Diet = traits$diet, row.names = traits$label)
# gheatmap() fails here (ggtree 3.14 + ggplot2 4.0.3: "@mapping must be <ggplot2::mapping>, not S3<data.frame>", see fig2.log
# first run); adapted to the equivalent ggtreeExtra geom_fruit(geom_tile) column.
p2 <- tryCatch({
  x <- gheatmap(p + new_scale_fill(), diet, offset = 0.07, width = 0.06, colnames_angle = 0, font.size = 2.4); ggplot_build(x); x
}, error = function(e) { cat("gheatmap failed:", conditionMessage(e), "-> geom_fruit fallback\n")
  p + new_scale_fill() + geom_fruit(data = ring, geom = geom_tile, mapping = aes(y = label, fill = Diet), pwidth = 0.06,
                                    offset = 0.42, axis.params = list(axis = "x", text.size = 0.1, title = "Diet", title.size = 2.4)) })
p2 <- p2 + scale_fill_brewer(palette = "Set3", name = "Diet (synthetic)")
p3 <- p2 + new_scale_fill() +
  geom_fruit(data = ring, geom = geom_col, mapping = aes(y = label, x = mass), fill = "grey40",
             pwidth = 0.25, offset = 0.18, axis.params = list(axis = "x", text.size = 2, title = "log10 mass (g)", title.size = 2.4)) +
  labs(caption = paste("ML tree (IQ-TREE 2.4.0, HKY+F+G4), rooted on Strepsirrhini. Scale bar: substitutions/site.",
                       "\nLabels SH-aLRT (%) / UFBoot (%); filled = passes both. Tips ladderized; order carries no meaning. Synthetic data.")) +
  theme(legend.position = "bottom", legend.box = "vertical", legend.text = element_text(size = 6),
        legend.title = element_text(size = 7), plot.caption = element_text(size = 6))
ggsave("fig2_primates.pdf", p3, width = 180, height = 150, units = "mm")
ggsave("fig2_primates_view.png", p3, width = 180, height = 150, units = "mm", dpi = 150)

# collapsed variant: UFBoot < 95 -> polytomy (the three sub-threshold nodes also fail SH-aLRT >= 80 or not; checked above)
# ggtree::as.polytomy only accepts phylo (first attempt on treedata: "currently only 'phylo' object is supported")
ph_r <- as.phylo(iq_r); tbr <- as_tibble(iq_r)
ph_r$node.label <- as.character(tbr$UFboot[match((Ntip(ph_r) + 1):(Ntip(ph_r) + Nnode(ph_r)), tbr$node)])
iq_c <- ggtree::as.polytomy(ph_r, feature = "node.label", fun = function(x) !is.na(as.numeric(x)) & as.numeric(x) < 95)
cat("internal nodes before/after collapse:", Nnode(iq_r), "/", Nnode(iq_c), "\n")
pc <- ggtree(iq_c, size = 0.4) + geom_tiplab(aes(label = gsub("_", " ", label)), fontface = "italic", size = 2.6) +
  geom_treescale(x = 0, y = -0.6, width = 0.02, fontsize = 2.4) + hexpand(0.35) +
  labs(caption = "Nodes with UFBoot < 95 collapsed to polytomies.")
ggsave("fig2_collapsed_view.png", pc, width = 120, height = 100, units = "mm", dpi = 150)
cat("saved\n")
