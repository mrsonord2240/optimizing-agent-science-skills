# Input 3 (Edge): "I don't have a tree for my ASVs -- can you still give me alpha and beta diversity
# and test my two groups?" Tests the Skill's documented behavior for the no-phylogeny case:
# Common Errors table says "UniFrac errors / Faith PD missing -- no phy_tree slot ... attach a tree".
# A correctly-followed Skill should fall back to non-phylogenetic metrics (Observed/Shannon/InvSimpson,
# Bray-Curtis/Jaccard) rather than crash or silently skip the analysis.
library(phyloseq)
library(vegan)

ps <- readRDS('F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/asvtable/phyloseq_object.rds')
# Strip the tree to simulate a user with no phylogeny (rebuild without the phy_tree slot)
ps_notree <- phyloseq(otu_table(ps), sample_data(ps), tax_table(ps))
cat('Has tree after stripping:', !is.null(phy_tree(ps_notree, errorIfNULL = FALSE)), '\n')

chosen_depth <- as.integer(quantile(sample_sums(ps_notree), 0.10))
ps_rare <- rarefy_even_depth(ps_notree, sample.size = chosen_depth, rngseed = 42, replace = FALSE)

alpha <- estimate_richness(ps_rare, measures = c('Observed', 'Shannon', 'InvSimpson'))
alpha$Group <- sample_data(ps_rare)$Group
cat('Alpha diversity (non-phylogenetic) computed OK:\n')
print(aggregate(cbind(Observed, Shannon) ~ Group, data = alpha, FUN = mean))

# Attempting UniFrac on a tree-less object -- confirm it actually errors as SKILL.md's
# Common Errors table claims, rather than silently returning garbage.
uf_result <- tryCatch({
  UniFrac(ps_rare, weighted = TRUE)
}, error = function(e) e)
cat('\nUniFrac on tree-less phyloseq object:\n')
if (inherits(uf_result, 'error')) {
  cat('ERRORED as documented. Message:', conditionMessage(uf_result), '\n')
} else {
  cat('Did NOT error -- unexpected, returned a result of class', class(uf_result), '\n')
}

# Non-phylogenetic beta diversity fallback: Bray-Curtis + Jaccard + PERMANOVA/betadisper
bray <- phyloseq::distance(ps_rare, method = 'bray')
jac  <- phyloseq::distance(ps_rare, method = 'jaccard', binary = TRUE)
meta <- data.frame(as(sample_data(ps_rare), 'data.frame'))
perm_bray <- adonis2(bray ~ Group, data = meta, permutations = 999)
perm_jac  <- adonis2(jac  ~ Group, data = meta, permutations = 999)
cat(sprintf('\nBray-Curtis PERMANOVA: R2=%.4f p=%.4g\n', perm_bray$R2[1], perm_bray$`Pr(>F)`[1]))
cat(sprintf('Jaccard PERMANOVA:      R2=%.4f p=%.4g\n', perm_jac$R2[1],  perm_jac$`Pr(>F)`[1]))
bd <- betadisper(bray, meta$Group)
pt <- permutest(bd)
cat(sprintf('Bray-Curtis betadisper: p=%.4g\n', pt$tab$`Pr(>F)`[1]))
cat('\nDone.\n')
