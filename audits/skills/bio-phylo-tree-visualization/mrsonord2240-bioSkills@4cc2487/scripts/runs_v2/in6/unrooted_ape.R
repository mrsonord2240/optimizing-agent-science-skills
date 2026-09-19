# Input 6 fallback: ggtree unrooted layouts crash in this env (ggtree 3.14 + ggplot2 4.0.3: "could not find function is.waive");
# per the Skill's introspect-and-adapt rule, draw the unrooted panel with ape::plot.phylo(type = "unrooted").
suppressPackageStartupMessages({library(treeio); library(ape)})
ph <- as.phylo(read.iqtree("../../data/iq/primates16.treefile"))
ph$node.label <- NULL
phr <- root(ph, outgroup = c("Microcebus_murinus", "Otolemur_garnettii"), resolve.root = TRUE)
cat("Tarsius sister to Anthropoidea in rooted tree:",
    is.monophyletic(phr, setdiff(ph$tip.label, c("Microcebus_murinus", "Otolemur_garnettii"))), "(haplorhines)",
    is.monophyletic(phr, setdiff(ph$tip.label, c("Microcebus_murinus", "Otolemur_garnettii", "Tarsius_syrichta"))), "(anthropoids)\n")
draw <- function() {
  par(mfrow = c(1, 2), mar = c(3, 1, 3, 1))
  plot(ph, type = "unrooted", lab4ut = "axial", cex = 0.6, no.margin = FALSE, font = 3)
  add.scale.bar(cex = 0.6); title("A  Unrooted: no root, no 'basal' taxon", cex.main = 0.8)
  plot(ladderize(phr), cex = 0.6, font = 3, x.lim = 0.45)
  add.scale.bar(cex = 0.6); title("B  Rooted on Strepsirrhini (outgroup)", cex.main = 0.8)
  mtext("Scale bars: substitutions/site. Tarsius is sister to Anthropoidea; it is not 'basal'. Synthetic data.", side = 1, line = 1.5, cex = 0.6, adj = 1)
}
pdf("unrooted_vs_rooted.pdf", width = 10, height = 5); draw(); dev.off()
png("unrooted_vs_rooted_view.png", width = 1100, height = 550, res = 110); draw(); dev.off()
cat("saved\n")
