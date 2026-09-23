# Input 2 (Variant A): "Pick a rarefaction sampling depth from my feature table and tell me which
# samples it drops." Directly exercises Common Errors #1 and Quantitative Thresholds row 1/2
# (SKILL.md explicitly says min(sample_sums) is "the worst of both worlds").
# We quantify exactly how bad the min() choice is vs. the plateau-based choice on real data.
library(phyloseq)

ps <- readRDS('F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/asvtable/phyloseq_object.rds')
depths <- sort(sample_sums(ps))
cat('Per-sample depth distribution:\n')
print(summary(depths))
cat('\nFull sorted depths:\n')
print(depths)

min_depth <- min(depths)
plateau_depth <- as.integer(quantile(depths, 0.10))

cat(sprintf('\nmin(sample_sums) = %d  (SKILL.md: the worst choice)\n', min_depth))
cat(sprintf('plateau-based (10th pctile) = %d\n', plateau_depth))

# Rarefy at min() depth -- richness saturation check
ps_min <- rarefy_even_depth(ps, sample.size = min_depth, rngseed = 42, replace = FALSE, verbose = FALSE)
ps_plateau <- rarefy_even_depth(ps, sample.size = plateau_depth, rngseed = 42, replace = FALSE, verbose = FALSE)

rich_min <- estimate_richness(ps_min, measures = 'Observed')
rich_plateau <- estimate_richness(ps_plateau, measures = 'Observed')

cat(sprintf('\nAt min depth (%d): mean Observed richness = %.1f, samples kept = %d\n',
            min_depth, mean(rich_min$Observed), nsamples(ps_min)))
cat(sprintf('At plateau depth (%d): mean Observed richness = %.1f, samples kept = %d\n',
            plateau_depth, mean(rich_plateau$Observed), nsamples(ps_plateau)))
cat(sprintf('\nRichness recovered at plateau depth relative to min-depth subsampling: %.1f%% higher\n',
            100 * (mean(rich_plateau$Observed) - mean(rich_min$Observed)) / mean(rich_min$Observed)))
cat('\nDone.\n')
