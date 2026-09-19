# Input 1 (Canonical): full alpha+beta diversity workflow on the fixture phyloseq object,
# following SKILL.md's exact R pattern (rarefy_even_depth, estimate_richness, picante::pd,
# UniFrac weighted+unweighted, adonis2, betadisper).
library(phyloseq)
library(vegan)

ps <- readRDS('F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/asvtable/phyloseq_object.rds')
cat('Loaded:', nsamples(ps), 'samples,', ntaxa(ps), 'taxa\n')

depths <- sort(sample_sums(ps))
cat('Depth range:', min(depths), '-', max(depths), '| median:', median(depths), '\n')

# Knob 1: sampling depth - SKILL.md says pick from the plateau, NOT min(sample_sums)
chosen_depth <- as.integer(quantile(depths, 0.10))
dropped <- names(sample_sums(ps))[sample_sums(ps) < chosen_depth]
cat('Chosen depth (10th pctile, per SKILL.md guidance):', chosen_depth, '\n')
cat('Samples dropped:', length(dropped), '->', if(length(dropped)) paste(dropped, collapse=', ') else 'none', '\n')

ps_rare <- rarefy_even_depth(ps, sample.size = chosen_depth, rngseed = 42, replace = FALSE)
cat('After rarefaction:', nsamples(ps_rare), 'samples remain\n')

alpha <- estimate_richness(ps_rare, measures = c('Observed', 'Shannon', 'InvSimpson'))
alpha$Shannon_eff <- exp(alpha$Shannon)
alpha$Group <- sample_data(ps_rare)$Group

cat('\n--- Alpha diversity summary ---\n')
print(aggregate(cbind(Observed, Shannon, Shannon_eff, InvSimpson) ~ Group, data = alpha, FUN = mean))

kw_shannon <- kruskal.test(Shannon ~ Group, data = alpha)
kw_obs <- kruskal.test(Observed ~ Group, data = alpha)
cat(sprintf('Kruskal-Wallis Shannon: chi-sq=%.3f p=%.4g\n', kw_shannon$statistic, kw_shannon$p.value))
cat(sprintf('Kruskal-Wallis Observed: chi-sq=%.3f p=%.4g\n', kw_obs$statistic, kw_obs$p.value))

# Faith PD (picante)
faith <- picante::pd(as(t(otu_table(ps_rare)), 'matrix'), phy_tree(ps_rare), include.root = TRUE)
alpha$Faith_PD <- faith$PD
cat('\nFaith PD by group:\n')
print(aggregate(Faith_PD ~ Group, data = alpha, FUN = mean))
kw_faith <- kruskal.test(Faith_PD ~ Group, data = alpha)
cat(sprintf('Kruskal-Wallis Faith PD: chi-sq=%.3f p=%.4g\n', kw_faith$statistic, kw_faith$p.value))

# Knob 3: beta diversity metrics - weighted AND unweighted UniFrac + Bray-Curtis
wu  <- UniFrac(ps_rare, weighted = TRUE)
uwu <- UniFrac(ps_rare, weighted = FALSE)
bray <- phyloseq::distance(ps_rare, method = 'bray')

meta <- data.frame(as(sample_data(ps_rare), 'data.frame'))  # coerced per TOOLS.md S6 trap

perm_wu   <- adonis2(wu   ~ Group, data = meta, permutations = 999)
perm_uwu  <- adonis2(uwu  ~ Group, data = meta, permutations = 999)
perm_bray <- adonis2(bray ~ Group, data = meta, permutations = 999)

cat('\n--- PERMANOVA (adonis2, 999 perms) ---\n')
cat(sprintf('Weighted UniFrac:   R2=%.4f  p=%.4g\n', perm_wu$R2[1],   perm_wu$`Pr(>F)`[1]))
cat(sprintf('Unweighted UniFrac: R2=%.4f  p=%.4g\n', perm_uwu$R2[1],  perm_uwu$`Pr(>F)`[1]))
cat(sprintf('Bray-Curtis:        R2=%.4f  p=%.4g\n', perm_bray$R2[1], perm_bray$`Pr(>F)`[1]))

# MANDATORY betadisper alongside PERMANOVA
bd_wu  <- betadisper(wu, meta$Group)
pt_wu  <- permutest(bd_wu)
bd_uwu <- betadisper(uwu, meta$Group)
pt_uwu <- permutest(bd_uwu)

cat('\n--- betadisper (location vs dispersion check) ---\n')
cat(sprintf('Weighted UniFrac betadisper:   p=%.4g\n', pt_wu$tab$`Pr(>F)`[1]))
cat(sprintf('Unweighted UniFrac betadisper: p=%.4g\n', pt_uwu$tab$`Pr(>F)`[1]))

cat('\nDone.\n')
