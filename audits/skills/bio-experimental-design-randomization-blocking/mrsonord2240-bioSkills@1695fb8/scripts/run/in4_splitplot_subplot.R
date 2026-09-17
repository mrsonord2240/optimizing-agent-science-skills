# Input 4 (regression) -- Variant B: split-plot / sequencing-lane whole-plot design,
# sub-plot fixed effect only (same scenario the pre-fix audit ran; the fix's new content
# targets the whole-plot case, tested independently in in8_*).
# Prompt: "3 sequencing lanes (whole plots); within each lane, 4 samples (2 WT, 2 KO). Test
# genotype effect on expression. Lane is hard to randomize finely -- how do I model this?"
suppressPackageStartupMessages({
  library(lme4)
  library(lmerTest)
})
set.seed(2026091701)
n_lanes <- 3
lane_effect <- rnorm(n_lanes, 0, 1.2)
df <- do.call(rbind, lapply(seq_len(n_lanes), function(l) {
  genotype <- sample(rep(c('WT', 'KO'), each = 2))
  data.frame(lane = factor(l), genotype = genotype,
             expression = lane_effect[l] + 0 * (genotype == 'KO') + rnorm(4, 0, 0.4))
}))

flat  <- lm(expression ~ genotype, data = df)
mixed <- lmer(expression ~ genotype + (1 | lane), data = df)
cat(sprintf('Flat lm() genotype SE:  %.4f\n', coef(summary(flat))['genotypeWT', 'Std. Error']))
cat(sprintf('Mixed lmer(...+(1|lane)) genotype SE: %.4f\n', coef(summary(mixed))['genotypeWT', 'Std. Error']))
vc <- as.data.frame(VarCorr(mixed))
cat(sprintf('Lane random-effect variance: %.3f\n', vc$vcov[vc$grp == 'lane']))
print(anova(mixed))
