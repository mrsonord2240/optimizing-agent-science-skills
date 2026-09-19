# Re-run both MaAsLin2 variants with plotting disabled (the earlier run showed
# a ggplot2-version plotting crash unrelated to the random-effects question) so
# we can read clean TP/FP numbers from the written result files.

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
otu_cols <- as.data.frame(t(otu))

report <- function(dir_path, label) {
  f <- file.path(dir_path, 'all_results.tsv')
  if (!file.exists(f)) { cat(label, ': all_results.tsv NOT WRITTEN\n'); return(invisible(NULL)) }
  r <- read.delim(f)
  rg <- r[r$metadata == 'Group', ]
  n_na <- sum(is.na(rg$qval))
  sig <- rg$feature[!is.na(rg$qval) & rg$qval < 0.05]
  tp <- sum(sig %in% planted); fp <- sum(!(sig %in% planted))
  cat(sprintf('%-30s n_group_rows=%d  n_NA_qval=%d  sig=%d  TP=%d/%d  FP=%d\n',
              label, nrow(rg), n_na, length(sig), tp, length(planted), fp))
}

cat('--- WITH random_effects=SubjectID (as SKILL.md shows it) ---\n')
out1 <- 'run/_maaslin2_with_re'
unlink(out1, recursive = TRUE)
invisible(capture.output(
  Maaslin2(input_data = otu_cols, input_metadata = meta,
           output = out1, fixed_effects = c('Group', 'Age'),
           random_effects = c('SubjectID'),
           normalization = 'TSS', transform = 'LOG', analysis_method = 'LM',
           min_prevalence = 0.10, max_significance = 0.05,
           plot_heatmap = FALSE, plot_scatter = FALSE)
))
report(out1, 'WITH random_effects=SubjectID')

cat('\n--- WITHOUT random_effects (SubjectID dropped) ---\n')
out2 <- 'run/_maaslin2_no_re'
unlink(out2, recursive = TRUE)
invisible(capture.output(
  Maaslin2(input_data = otu_cols, input_metadata = meta,
           output = out2, fixed_effects = c('Group', 'Age'),
           normalization = 'TSS', transform = 'LOG', analysis_method = 'LM',
           min_prevalence = 0.10, max_significance = 0.05,
           plot_heatmap = FALSE, plot_scatter = FALSE)
))
report(out2, 'WITHOUT random_effects')
