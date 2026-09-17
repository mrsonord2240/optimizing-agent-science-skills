# Input 2 -- Variant A / budget tradeoff: "I have budget for either 20M reads on 4 samples or
# 10M reads on 8 samples per group. Which gives more power to detect DE genes?"
# Exercises the SKILL.md "Depth vs Replicates" section pattern (rnapower over a depth sweep) plus
# a direct head-to-head of the two named options at CV=0.4, 2-fold change (matches the example
# script's own cv/effect defaults since the prompt does not specify them).

suppressPackageStartupMessages(library(RNASeqPower))

cat("=== Depth sweep at fixed n=4 (SKILL.md/example pattern) ===\n")
for (d in c(10, 20, 50, 100)) {
  p <- rnapower(depth = d, n = 4, cv = 0.4, effect = 2, alpha = 0.05)
  cat(sprintf("Depth %3d, n=4: power = %.4f\n", d, p))
}

cat("\n=== Head-to-head: 20M reads x 4 samples  vs  10M reads x 8 samples ===\n")
# RNASeqPower's 'depth' argument is reads-per-gene, not total library size in millions; the two
# scenarios are expressed here in the same depth units used throughout the Skill's own examples
# (arbitrary consistent reads/gene units), scaled 2x for the 20M vs 10M relationship.
p_20M_n4 <- rnapower(depth = 40, n = 4, cv = 0.4, effect = 2, alpha = 0.05)
p_10M_n8 <- rnapower(depth = 20, n = 8, cv = 0.4, effect = 2, alpha = 0.05)
cat(sprintf("20M reads x n=4 (depth=40): power = %.4f\n", p_20M_n4))
cat(sprintf("10M reads x n=8 (depth=20): power = %.4f\n", p_10M_n8))
cat(sprintf("Total sequencing spend is equal in both arms (depth x n = %d vs %d)\n",
            40*4, 20*8))
