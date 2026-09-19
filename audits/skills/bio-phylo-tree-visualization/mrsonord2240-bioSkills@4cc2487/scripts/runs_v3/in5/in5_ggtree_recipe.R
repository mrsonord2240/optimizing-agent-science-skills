# Input 5 (Stress): "Draw a publication figure from my IQ-TREE run: root on the
# strepsirrhines, show dual SH-aLRT/UFBoot support, and add a metadata ring."
# Runs the SKILL.md '## ggtree + treeio Recipe (R)' section VERBATIM (not auditor-authored
# fig2.R as the pre-fix/84-score audits used) against the real primates16 IQ-TREE output,
# adapting only the file path and outgroup names.
suppressPackageStartupMessages({library(treeio); library(ggtree); library(ggtreeExtra); library(ggplot2)})

iq <- read.iqtree('data/iq/primates16.treefile')   # read.iqtree also accepts the .treefile w/ support

root_keep <- function(td, outgroup) {
  r <- treeio::root(td, outgroup = outgroup, edgelabel = TRUE)
  if (all(grepl('^[0-9]+$', r@phylo$tip.label))) r@phylo$tip.label <- td@phylo$tip.label[as.integer(r@phylo$tip.label)]
  r
}
iq_r <- root_keep(iq, c('Microcebus_murinus', 'Otolemur_garnettii'))

cat('Tip count after rooting:', length(iq_r@phylo$tip.label), '\n')
cat('Any numeric-only tip labels left (bad restore)?', any(grepl('^[0-9]+$', iq_r@phylo$tip.label)), '\n')

p <- ggtree(iq_r, size = 0.4) +
  geom_tiplab(size = 2.6, offset = 0.003) +
  geom_nodelab(aes(label = ifelse(is.na(UFboot), '', paste0(SH_aLRT, '/', UFboot))), size = 2, hjust = 1.1, vjust = -0.5) +
  geom_treescale(width = 0.02, fontsize = 2.4)

meta <- data.frame(label = iq_r@phylo$tip.label, trait = seq_along(iq_r@phylo$tip.label))
p2 <- p + geom_fruit(data = meta, geom = geom_tile, mapping = aes(y = label, fill = trait), pwidth = 0.06, offset = 0.08)

built <- tryCatch({ b <- ggplot_build(p2); paste('OK,', length(b$plot$layers), 'layers') },
                   error = function(e) paste('ERROR:', conditionMessage(e)))
cat('ggplot_build result:', built, '\n')

out <- 'fig_in5.pdf'
ggsave(out, p2, width = 180, height = 150, units = 'mm')
cat('ggsave file size (bytes):', file.info(out)$size, '\n')

# Count non-NA dual-support node labels actually present after rooting.
d <- iq_r@data
n_support <- sum(!is.na(d$UFboot))
cat('Non-NA UFboot node labels after rooting:', n_support, 'of', nrow(d), 'internal rows\n')

# groupOTU stem-coloring check, as the SKILL.md sentence claims.
grp <- groupOTU(iq_r, list(GreatApes = c('Homo_sapiens', 'Pan_troglodytes', 'Pan_paniscus', 'Gorilla_gorilla', 'Pongo_abelii')), group_name = 'grp')
pg <- ggtree(grp, aes(color = grp), size = 0.6)
bg <- ggplot_build(pg)
seg <- bg$data[[1]]
# identify the stem edge into the GreatApes MRCA vs an edge clearly outside the group
cols <- unique(seg$colour)
cat('Distinct segment colours drawn by groupOTU coloring:', length(cols), '->', paste(cols, collapse=', '), '\n')
