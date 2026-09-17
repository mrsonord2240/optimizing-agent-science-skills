# Extracted verbatim from SKILL.md "Reference / Bridge Channel Layout" (new section, post-fix,
# commit 6847328).
library(designit)
samples <- data.frame(id = sprintf('S%02d', 1:60),
                      condition = rep(c('case', 'ctrl'), each = 30),
                      site = rep(c('A', 'B', 'C'), length.out = 60))

# Reserve channel 16 of every plex (4 plexes) for the pooled bridge sample -- exclude needs one
# row per excluded (plex, channel) combination, not just the channel column alone.
bc <- BatchContainer$new(
  dimensions = list(plex = 4, channel = 16),
  exclude = data.frame(plex = 1:4, channel = 16))
bc <- assign_in_order(bc, samples = samples)     # only fills the 60 non-reserved positions
bc <- optimize_design(
  bc,
  scoring = osat_score_generator(batch_vars = 'plex', feature_vars = c('condition', 'site')),
  max_iter = 10000)
assignment <- bc$get_samples()

# Verify: channel 16 must stay empty (holds the pooled reference, added outside this table) and
# every plex must have exactly 15 biological positions.
stopifnot(
  "channel 16 was assigned a biological sample" = !16 %in% assignment$channel,
  "a plex does not have exactly 15 biological positions" =
    all(table(assignment$plex) == 15)
)
tab <- table(assignment$condition, assignment$plex); print(tab)
stopifnot(all(tab > 0))                          # same confounding check as above
