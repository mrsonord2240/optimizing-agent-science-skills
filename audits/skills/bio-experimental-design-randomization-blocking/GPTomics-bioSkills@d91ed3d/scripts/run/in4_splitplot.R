# Input 4 (Variant B) — Split-plot / sequencing-lane whole-plot design
# Prompt: "3 sequencing lanes (whole plots); within each lane, 4 samples: 2 WT, 2 KO.
#  Test genotype effect on gene expression. Lane is hard to randomize finely — how do I
#  model this and what code do I use?"
# SYNTHETIC expression data generated below, following SKILL.md's
# "Split-Plot and Nested Designs" pattern: lmer(y ~ genotype + (1 | run/sample))
# Here there is no true sub-sampling within sample, so the matching structure is
# lmer(y ~ genotype + (1 | lane)) -- lane is the whole-plot random effect.

suppressPackageStartupMessages({
  library(lme4)
  library(lmerTest)
})

set.seed(2026091701)
n_lanes <- 3
samples_per_lane <- 4  # 2 WT, 2 KO

df <- expand.grid(sample = 1:samples_per_lane, lane = paste0('L', 1:n_lanes))
df$genotype <- rep(c('WT', 'WT', 'KO', 'KO'), times = n_lanes)
lane_effect <- setNames(rnorm(n_lanes, 0, 1.2), paste0('L', 1:n_lanes))  # large lane (batch) effect
df$expression <- lane_effect[df$lane] +
  ifelse(df$genotype == 'KO', 0.5, 0) + rnorm(nrow(df), 0, 0.3)

cat('=== Data (3 lanes x 4 samples, 2 WT/2 KO per lane) ===\n')
print(df)

# WRONG: flat model ignoring lane structure (treats 12 obs as independent -> anti-conservative)
flat <- lm(expression ~ genotype, data = df)
cat('\n=== WRONG: flat lm(), ignores whole-plot error stratum ===\n')
print(summary(flat)$coefficients)

# CORRECT: split-plot mixed model, lane as whole-plot random effect
fit <- lmer(expression ~ genotype + (1 | lane), data = df)
cat('\n=== CORRECT: lmer(expression ~ genotype + (1 | lane)) ===\n')
print(anova(fit))  # Satterthwaite df via lmerTest
print(summary(fit)$coefficients)

cat('\n=== ASSERTION CHECK ===\n')
flat_se <- summary(flat)$coefficients['genotypeWT', 'Std. Error']
mixed_se <- summary(fit)$coefficients['genotypeWT', 'Std. Error']
cat('Flat-model SE for genotype (wrong, ignores lane variance):', round(flat_se, 4), '\n')
cat('Mixed-model SE for genotype (correct, whole-plot aware):', round(mixed_se, 4), '\n')
cat('Mixed model SE differs from flat model SE (structure matters):',
    abs(flat_se - mixed_se) > 1e-6, '\n')
lane_var <- as.data.frame(VarCorr(fit))$vcov[1]
cat('Lane random-effect variance estimated (>0, captures the batch/whole-plot effect):',
    lane_var > 0, ' (', round(lane_var, 3), ')\n')
