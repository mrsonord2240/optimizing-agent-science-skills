# Input 5 (regression) -- Stress: 2x2 factorial blocked by litter, with interaction
# Prompt: "Test genotype (WT/KO) x drug (vehicle/treated) in a 2x2 factorial, blocked by
# litter (4 litters, 2 animals/cell, 32 total). Randomize treatment within litter, give the
# model formula with block + interaction, and explain how to interpret a significant
# interaction."
set.seed(2026091705)
litter <- rep(paste0('L', 1:4), each = 8)
grid <- expand.grid(genotype = c('WT', 'KO'), drug = c('vehicle', 'treated'), rep = 1:2)
df <- do.call(rbind, lapply(1:4, function(i) cbind(grid, litter = paste0('L', i))))
litter_effect <- setNames(rnorm(4, 0, 0.6), paste0('L', 1:4))
# planted interaction: drug effect is much larger within KO than WT
df$response <- 1.0 +
  0.8 * (df$genotype == 'KO') +
  0.5 * (df$drug == 'treated') +
  1.1 * (df$genotype == 'KO' & df$drug == 'treated') +
  litter_effect[df$litter] + rnorm(nrow(df), 0, 0.5)

fit <- aov(response ~ litter + genotype * drug, data = df)
print(summary(fit))

means <- aggregate(response ~ genotype + drug, data = df, mean)
drug_in_ko <- means$response[means$genotype == 'KO' & means$drug == 'treated'] -
              means$response[means$genotype == 'KO' & means$drug == 'vehicle']
drug_in_wt <- means$response[means$genotype == 'WT' & means$drug == 'treated'] -
              means$response[means$genotype == 'WT' & means$drug == 'vehicle']
cat(sprintf('\nDrug effect within KO: %.3f\nDrug effect within WT: %.3f\n', drug_in_ko, drug_in_wt))
