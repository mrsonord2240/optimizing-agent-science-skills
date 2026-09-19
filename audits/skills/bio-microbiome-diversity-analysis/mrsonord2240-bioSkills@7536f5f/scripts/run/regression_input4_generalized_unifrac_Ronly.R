# Part of Input 4 (Variant B): exercise SKILL.md's own verbatim generalized-UniFrac line
# (Beta Diversity in R section, alpha=0.5 Chen 2012 compromise) on the real fixture object,
# alongside weighted/unweighted, to confirm the documented code pattern actually runs and to see
# whether the generalized metric's PERMANOVA result sits between the weighted/unweighted extremes
# as the Skill's decision-tree table claims ("alpha=0.5 compromise").
library(phyloseq)
library(vegan)
library(GUniFrac)

ps <- readRDS('F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/asvtable/phyloseq_object.rds')
chosen_depth <- as.integer(quantile(sample_sums(ps), 0.10))
ps_rare <- rarefy_even_depth(ps, sample.size = chosen_depth, rngseed = 42, replace = FALSE, verbose = FALSE)

wu  <- UniFrac(ps_rare, weighted = TRUE)
uwu <- UniFrac(ps_rare, weighted = FALSE)
# SKILL.md's exact verbatim line (Beta Diversity in R section):
gu  <- as.dist(GUniFrac::GUniFrac(t(as(otu_table(ps_rare), 'matrix')), phy_tree(ps_rare), alpha = 0.5)$unifracs[, , 'd_0.5'])

meta <- data.frame(as(sample_data(ps_rare), 'data.frame'))
perm_wu  <- adonis2(wu  ~ Group, data = meta, permutations = 999)
perm_uwu <- adonis2(uwu ~ Group, data = meta, permutations = 999)
perm_gu  <- adonis2(gu  ~ Group, data = meta, permutations = 999)

cat('SKILL.md verbatim generalized-UniFrac (GUniFrac::GUniFrac alpha=0.5) line: ran without modification\n\n')
cat(sprintf('Weighted UniFrac (alpha=1):    R2=%.4f p=%.4g\n', perm_wu$R2[1],  perm_wu$`Pr(>F)`[1]))
cat(sprintf('Generalized UniFrac alpha=0.5: R2=%.4f p=%.4g\n', perm_gu$R2[1],  perm_gu$`Pr(>F)`[1]))
cat(sprintf('Unweighted UniFrac (alpha=0):  R2=%.4f p=%.4g\n', perm_uwu$R2[1], perm_uwu$`Pr(>F)`[1]))
cat('\nDone.\n')
