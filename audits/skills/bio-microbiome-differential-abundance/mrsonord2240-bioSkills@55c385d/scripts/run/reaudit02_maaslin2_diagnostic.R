# Diagnostic: SKILL.md's MaAsLin2 code block (unchanged by the fix pass) uses
# random_effects = c('SubjectID') and sits right next to the same cross-sectional
# fixture (phyloseq_object.rds) that the fixer used to verify the LinDA fix -- in
# that fixture SubjectID has exactly as many levels (40) as observations (40),
# the identical mismatch class that caused the original LinDA P1. Characterizing
# whether MaAsLin2's shown block silently produces garbage on this fixture.

setwd('F:/OpenScience/audits/bio-microbiome-differential-abundance')
library(phyloseq)
library(Maaslin2)

truth <- read.delim('data/asvtable/truth_da.tsv', stringsAsFactors = FALSE)
planted <- truth$ASV[truth$role != 'null']

ps <- readRDS('data/asvtable/phyloseq_object.rds')
keep <- filter_taxa(ps, function(x) sum(x > 0) >= 0.10 * nsamples(ps), TRUE)
ps <- keep
otu <- as.data.frame(otu_table(ps)); if (!taxa_are_rows(ps)) otu <- t(otu)
meta <- data.frame(as(sample_data(ps), 'data.frame'))
cat('n samples:', nrow(meta), ' n unique SubjectID:', length(unique(meta$SubjectID)), '\n')

otu_cols <- as.data.frame(t(otu))

cat('\n--- MaAsLin2 EXACTLY as SKILL.md shows it (fixed_effects + random_effects=SubjectID) ---\n')
out_dir1 <- tempfile('maaslin2_diag_with_re')
fit_a <- Maaslin2(input_data = otu_cols, input_metadata = meta,
                output = out_dir1, fixed_effects = c('Group', 'Age'),
                random_effects = c('SubjectID'),
                normalization = 'TSS', transform = 'LOG', analysis_method = 'LM',
                min_prevalence = 0.10, max_significance = 0.05)
r1 <- fit_a$results
r1g <- r1[r1$metadata == 'Group', ]
sig1 <- r1g$feature[r1g$qval < 0.05]
tp1 <- sum(sig1 %in% planted); fp1 <- sum(!(sig1 %in% planted))
cat(sprintf('With random_effects=SubjectID: sig=%d TP=%d/%d FP=%d\n', length(sig1), tp1, length(planted), fp1))
cat('Sample of pval/qval/coef for first 5 Group rows:\n')
print(head(r1g[, c('feature','coef','pval','qval')], 5))

cat('\n--- Same call WITHOUT random_effects (drop SubjectID) ---\n')
out_dir2 <- tempfile('maaslin2_diag_no_re')
fit_b <- Maaslin2(input_data = otu_cols, input_metadata = meta,
                output = out_dir2, fixed_effects = c('Group', 'Age'),
                normalization = 'TSS', transform = 'LOG', analysis_method = 'LM',
                min_prevalence = 0.10, max_significance = 0.05)
r2 <- fit_b$results
r2g <- r2[r2$metadata == 'Group', ]
sig2 <- r2g$feature[r2g$qval < 0.05]
tp2 <- sum(sig2 %in% planted); fp2 <- sum(!(sig2 %in% planted))
cat(sprintf('Without random_effects: sig=%d TP=%d/%d FP=%d\n', length(sig2), tp2, length(planted), fp2))
