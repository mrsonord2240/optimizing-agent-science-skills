set.seed(2026092305)
df <- expand.grid(litter = factor(sprintf("L%d", 1:4)), genotype = factor(c("WT", "KO")), drug = factor(c("vehicle", "treated")), replicate = 1:2, KEEP.OUT.ATTRS = FALSE)
litter_effect <- rnorm(4, sd = 0.8)[df$litter]
df$y <- 0.6 * (df$genotype == "KO") + 0.9 * (df$drug == "treated") + 0.9 * (df$genotype == "KO" & df$drug == "treated") + litter_effect + rnorm(nrow(df), sd = 0.35)
fit <- aov(y ~ litter + genotype * drug, data = df)
p_interaction <- summary(fit)[[1]]["genotype:drug", "Pr(>F)"]
means <- with(df, tapply(y, list(genotype, drug), mean))
stopifnot(p_interaction < 0.05, (means["KO", "treated"] - means["KO", "vehicle"]) > (means["WT", "treated"] - means["WT", "vehicle"]))
cat(sprintf("interaction_p=%.6f KO_drug_effect=%.3f WT_drug_effect=%.3f\n", p_interaction, means["KO", "treated"] - means["KO", "vehicle"], means["WT", "treated"] - means["WT", "vehicle"]))
