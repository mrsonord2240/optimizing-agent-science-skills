library(designit)                              # verify API against installed vignette
samples <- data.frame(id = sprintf('S%02d', 1:24),
                      condition = rep(c('ctrl', 'treat'), each = 12),
                      sex = rep(c('M', 'F'), 12))
bc <- BatchContainer$new(dimensions = list(batch = 3, position = 8))
bc <- assign_in_order(bc, samples = samples)
bc <- optimize_design(
  bc,
  scoring = osat_score_generator(batch_vars = 'batch',
                                 feature_vars = c('condition', 'sex')))   # balance both factors
assignment <- bc$get_samples()                # R6 method on the container (no standalone get_samples())

# OSAT alternative (Bioconductor): build a setup object, then optimal.shuffle() -- NOT a bare osat().
