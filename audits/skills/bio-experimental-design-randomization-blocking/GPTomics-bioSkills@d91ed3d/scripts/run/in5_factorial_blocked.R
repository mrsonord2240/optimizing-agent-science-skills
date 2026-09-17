# Input 5 (Stress / multi-part) — 2x2 factorial, blocked by litter, with interaction
# Prompt: "Test genotype (WT/KO) x drug (vehicle/treated) in a 2x2 factorial, blocked by
#  litter (4 litters), 2 animals per genotype x drug x litter cell (32 animals total).
#  Randomize treatment within litter; give the model formula including block and
#  interaction; tell me how to interpret a significant interaction."
# SYNTHETIC data with a PLANTED interaction effect, generated below.

set.seed(2026091705)
n_litters <- 4
per_cell <- 2  # animals per genotype x drug x litter cell

design <- expand.grid(litter = paste0('Lit', 1:n_litters),
                       genotype = c('WT', 'KO'),
                       drug = c('vehicle', 'treated'),
                       rep = 1:per_cell)
design$id <- sprintf('M%02d', seq_len(nrow(design)))

# Randomize treatment assignment order within litter block (documented random mechanism)
design <- design[order(design$litter, sample(nrow(design))), ]

# Planted interaction: KO+treated gets an extra boost beyond additive WT/KO and veh/treated effects
litter_effect <- setNames(rnorm(n_litters, 0, 0.5), paste0('Lit', 1:n_litters))
design$response <- litter_effect[design$litter] +
  ifelse(design$genotype == 'KO', 0.3, 0) +
  ifelse(design$drug == 'treated', 0.3, 0) +
  ifelse(design$genotype == 'KO' & design$drug == 'treated', 1.2, 0) +  # interaction
  rnorm(nrow(design), 0, 0.4)

cat('=== Design cell counts (litter x genotype x drug) ===\n')
print(table(design$litter, design$genotype, design$drug))

# Model formula per SKILL.md: block term + factorial + interaction
fit <- aov(response ~ litter + genotype * drug, data = design)
cat('\n=== Model: aov(response ~ litter + genotype * drug) ===\n')
print(summary(fit))

cat('\n=== Simple-effects interpretation (since interaction present) ===\n')
agg <- aggregate(response ~ genotype + drug, data = design, FUN = mean)
print(agg)
ko_effect <- agg$response[agg$genotype == 'KO' & agg$drug == 'treated'] -
             agg$response[agg$genotype == 'KO' & agg$drug == 'vehicle']
wt_effect <- agg$response[agg$genotype == 'WT' & agg$drug == 'treated'] -
             agg$response[agg$genotype == 'WT' & agg$drug == 'vehicle']
cat('Drug effect within KO:', round(ko_effect, 3), '\n')
cat('Drug effect within WT:', round(wt_effect, 3), '\n')

cat('\n=== ASSERTION CHECK ===\n')
p_interaction <- summary(fit)[[1]][['Pr(>F)']][which(rownames(summary(fit)[[1]]) == 'genotype:drug')]
cat('Interaction term is estimable and significant (planted, p<0.05):',
    !is.na(p_interaction) && p_interaction < 0.05, ' (p=', signif(p_interaction, 3), ')\n')
cat('Drug effect differs by genotype (interaction manifests as unequal simple effects):',
    abs(ko_effect - wt_effect) > 0.5, '\n')
cat('Litter block term present in the model:', 'litter' %in% trimws(rownames(summary(fit)[[1]])), '\n')
