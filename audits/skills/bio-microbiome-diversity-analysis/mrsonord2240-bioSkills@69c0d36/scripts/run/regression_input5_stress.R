# Input 5 (Stress/multi-part): "I have a longitudinal microbiome study -- 3 timepoints per subject
# (baseline/week4/week8), placebo vs treatment arms. Give me alpha diversity across visits, and test
# whether beta diversity (weighted UniFrac) differs by treatment arm with PERMANOVA."
# This tests whether the Skill's guidance is sufficient for a repeated-measures design: SKILL.md
# only tells the agent to "escalate to lme4/nlme for covariates or repeated measures" for ALPHA
# diversity; it says nothing about pseudo-replication in adonis2/PERMANOVA for repeated beta-diversity
# designs. We check whether ignoring repeated measures (pseudo-replication) actually changes the
# PERMANOVA conclusion relative to a correctly restricted permutation (strata = SubjectID).
library(phyloseq)
library(vegan)

lp <- readRDS('F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/asvtable/long_phyloseq.rds')
cat('Loaded:', nsamples(lp), 'samples,', ntaxa(lp), 'taxa\n')
sd <- as(sample_data(lp), 'data.frame')
print(table(sd$Arm, sd$visit))

depths <- sort(sample_sums(lp))
cat('Depth range:', min(depths), '-', max(depths), '\n')
chosen_depth <- as.integer(quantile(depths, 0.10))
lp_rare <- rarefy_even_depth(lp, sample.size = chosen_depth, rngseed = 42, replace = FALSE)
cat('After rarefaction:', nsamples(lp_rare), 'samples remain (of', nsamples(lp), ')\n')

alpha <- estimate_richness(lp_rare, measures = c('Shannon'))
meta <- as(sample_data(lp_rare), 'data.frame')
alpha$Arm <- meta$Arm
alpha$visit <- meta$visit
alpha$SubjectID <- meta$SubjectID
cat('\nShannon by Arm x visit:\n')
print(aggregate(Shannon ~ Arm + visit, data = alpha, FUN = mean))

# Naive (pseudo-replicated) test ignoring repeated measures
kw_naive <- kruskal.test(Shannon ~ Arm, data = alpha)
cat(sprintf('\nNaive Kruskal-Wallis Shannon ~ Arm (ignores repeated measures): p=%.4g\n', kw_naive$p.value))

# Correct: mixed model with Subject as random effect
if (requireNamespace('lme4', quietly = TRUE)) {
  library(lme4); library(lmerTest)
  m <- lmer(Shannon ~ Arm + visit + (1|SubjectID), data = alpha)
  print(summary(m)$coefficients)
} else {
  cat('lme4 not available\n')
}

# --- Beta diversity: weighted UniFrac, PERMANOVA with and without strata ---
wu <- UniFrac(lp_rare, weighted = TRUE)
meta2 <- data.frame(as(sample_data(lp_rare), 'data.frame'))

perm_naive <- adonis2(wu ~ Arm, data = meta2, permutations = 999)
cat(sprintf('\nPERMANOVA (naive, pseudo-replicated, all 3 visits pooled): R2=%.4f p=%.4g\n',
            perm_naive$R2[1], perm_naive$`Pr(>F)`[1]))

perm_strata <- adonis2(wu ~ Arm, data = meta2, permutations = 999,
                        strata = meta2$SubjectID)
cat(sprintf('PERMANOVA (restricted permutations, strata=SubjectID): R2=%.4f p=%.4g\n',
            perm_strata$R2[1], perm_strata$`Pr(>F)`[1]))

bd <- betadisper(wu, meta2$Arm)
pt <- permutest(bd)
cat(sprintf('betadisper (Arm): p=%.4g\n', pt$tab$`Pr(>F)`[1]))

cat('\nDone.\n')
