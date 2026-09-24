# Final-pass regression for microbiome/differential-abundance.
# Exercises the revised cross-sectional MaAsLin2 block and the documented
# repeated-measures escape hatch against independent fixture shapes.
setwd('F:/OpenScience/audits/bio-microbiome-differential-abundance')
library(phyloseq)
library(Maaslin2)

run_model <- function(ps_path, output, fixed_effects, random_effects = NULL) {
  ps <- readRDS(ps_path)
  ps <- filter_taxa(ps, function(x) sum(x > 0) >= 0.10 * nsamples(ps), TRUE)
  otu <- as.data.frame(otu_table(ps))
  if (!taxa_are_rows(ps)) otu <- t(otu)
  meta <- data.frame(as(sample_data(ps), 'data.frame'))
  unlink(output, recursive = TRUE)
  args <- list(
    input_data = as.data.frame(t(otu)), input_metadata = meta,
    output = output, fixed_effects = fixed_effects,
    normalization = 'TSS', transform = 'LOG', analysis_method = 'LM',
    min_prevalence = 0.10, max_significance = 0.05,
    plot_heatmap = FALSE, plot_scatter = FALSE
  )
  if (!is.null(random_effects)) args$random_effects <- random_effects
  invisible(capture.output(do.call(Maaslin2, args)))
  result_path <- file.path(output, 'all_results.tsv')
  stopifnot(file.exists(result_path))
  result <- read.delim(result_path, stringsAsFactors = FALSE)
  effect_rows <- result[result$metadata == fixed_effects[[1]], , drop = FALSE]
  stopifnot(nrow(effect_rows) > 0L)
  cat(sprintf('%s: %s_rows=%d; significant=%d\n', output, fixed_effects[[1]],
              nrow(effect_rows), sum(!is.na(effect_rows$qval) & effect_rows$qval < 0.05)))
}

# Fresh test 1: the revised shown block must produce usable cross-sectional results.
run_model('data/asvtable/phyloseq_object.rds', 'run/finalpass_cross_sectional',
          fixed_effects = c('Group', 'Age'))

# Fresh test 2: the documented random-effect variant is reserved for actual repeats.
run_model('data/asvtable/long_phyloseq.rds', 'run/finalpass_repeated',
          fixed_effects = c('Arm'), random_effects = c('SubjectID'))
cat('FINALPASS_MAASLIN2_REGRESSION_PASS\n')
