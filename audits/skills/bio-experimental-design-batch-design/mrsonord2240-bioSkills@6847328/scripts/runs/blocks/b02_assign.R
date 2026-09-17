# Extracted verbatim from SKILL.md "Constrained Sample-to-Batch Assignment"
# (post-fix SKILL.md; commit 6847328)
library(designit)                              # verify API against installed vignette
samples <- data.frame(id = sprintf('S%02d', 1:24),
                      condition = rep(c('ctrl', 'treat'), each = 12),
                      sex = rep(c('M', 'F'), 12))
bc <- BatchContainer$new(dimensions = list(batch = 3, position = 8))
bc <- assign_in_order(bc, samples = samples)
bc <- optimize_design(
  bc,
  scoring = osat_score_generator(batch_vars = 'batch',
                                 feature_vars = c('condition', 'sex')),   # balance both factors
  max_iter = 10000)                            # raise if the verification below still looks uneven
assignment <- bc$get_samples()                # R6 method on the container (no standalone get_samples())
