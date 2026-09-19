# Input 3 (Variant B - longitudinal): "My samples are repeated within subjects over three
# visits (Arm: placebo vs treatment). Use a DA method with a subject random effect so I do
# not pseudo-replicate." Follows SKILL.md's LinDA mixed-model pattern, plus a pseudo-
# replication control run (ignoring SubjectID) to check whether ignoring it actually
# inflates significance, as SKILL.md's "Failure Modes" section claims.
suppressMessages({
  library(phyloseq)
  library(MicrobiomeStat)
})

lps <- readRDS('F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/asvtable/long_phyloseq.rds')
truth <- read.delim('F:/OpenScience/audit-envs/microbiome-metagenomics-analyst/datagen/asvtable/truth_da.tsv', stringsAsFactors = FALSE)
true_pos <- truth$ASV[truth$role != 'null']

keep <- filter_taxa(lps, function(x) sum(x > 0) >= 0.10 * nsamples(lps), TRUE)
cat('Taxa after prevalence filter:', ntaxa(keep), '\n')

otu <- as.data.frame(otu_table(keep)); if (!taxa_are_rows(keep)) otu <- t(otu)
# TRAP CHECK (TOOLS.md sec 6): as.data.frame(sample_data(ps)) silently keeps class "sample_data"
meta_naive <- as.data.frame(sample_data(keep))
cat('Naive as.data.frame() class (should still show sample_data - the trap):', paste(class(meta_naive), collapse=','), '\n')
meta <- data.frame(as(sample_data(keep), 'data.frame'))
cat('Coerced meta class (fixed):', paste(class(meta), collapse=','), '\n')

# Mixed model WITH subject random effect (correct, per SKILL.md)
fit_mixed <- linda(feature.dat = otu, meta.dat = meta,
                    formula = '~ Arm + (1 | SubjectID)',
                    feature.dat.type = 'count', prev.filter = 0, alpha = 0.05)
res_mixed <- fit_mixed$output[[1]]
sig_mixed <- rownames(res_mixed)[res_mixed$reject]
cat('\nLinDA (mixed, +SubjectID random effect) significant:', length(sig_mixed), '\n')

# Pseudo-replicated control: ignore subject structure entirely
fit_naive <- linda(feature.dat = otu, meta.dat = meta,
                    formula = '~ Arm',
                    feature.dat.type = 'count', prev.filter = 0, alpha = 0.05)
res_naive <- fit_naive$output[[1]]
sig_naive <- rownames(res_naive)[res_naive$reject]
cat('LinDA (naive, no random effect - pseudo-replication) significant:', length(sig_naive), '\n')

cat('\n=== GROUND TRUTH CHECK (longitudinal, mixed model) ===\n')
tp <- sum(sig_mixed %in% true_pos); fp <- sum(!(sig_mixed %in% true_pos)); fn <- length(true_pos) - tp
cat(sprintf('Mixed model: TP=%d/%d, FP=%d, FN=%d\n', tp, length(true_pos), fp, fn))
cat('Recovered:', paste(sort(intersect(sig_mixed, true_pos)), collapse=', '), '\n')
cat('Missed:', paste(sort(setdiff(true_pos, sig_mixed)), collapse=', '), '\n')
cat('False positives:', paste(sort(setdiff(sig_mixed, true_pos)), collapse=', '), '\n')

cat('\nNaive (pseudo-replicated) vs mixed model comparison:\n')
cat('  Naive found', length(sig_naive), 'vs mixed found', length(sig_mixed), '\n')
cat('  Extra taxa flagged ONLY by naive (pseudo-replication artifact candidates):',
    paste(sort(setdiff(sig_naive, sig_mixed)), collapse=', '), '\n')
extra_naive_fp <- setdiff(sig_naive, sig_mixed)
cat('  Of those, how many are truly null (i.e. pseudo-replication false positives):',
    sum(extra_naive_fp %in% truth$ASV[truth$role=='null']), '/', length(extra_naive_fp), '\n')
