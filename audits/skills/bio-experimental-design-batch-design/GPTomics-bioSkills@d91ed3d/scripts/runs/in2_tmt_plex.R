# Batch-design Input 2 (variant): 60 plasma samples (30 case / 30 ctrl; 3 sites) into 4 TMTpro 16plex plexes, channel 134N
# reserved for a pooled reference (bridge) in every plex. The Skill gives the designit pattern but no bridge-channel code; the
# agent adapts it (exclude the reference positions). SYNTHETIC design.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(designit))
set.seed(16)
samples <- data.frame(id = sprintf('P%02d', 1:60), condition = rep(c('ctrl', 'case'), each = 30), site = rep(c('A', 'B', 'C'), 20))
excl <- data.frame(plex = 1:4, channel = 16L)
t0 <- Sys.time()
bc <- tryCatch(BatchContainer$new(dimensions = list(plex = 4, channel = 16), exclude = excl), error = function(e) { cat('BatchContainer ERROR:', conditionMessage(e), '\n'); NULL })
bc <- assign_in_order(bc, samples = samples)
bc <- optimize_design(bc, scoring = osat_score_generator(batch_vars = 'plex', feature_vars = c('condition', 'site')))
a <- bc$get_samples()
cat('elapsed s:', round(as.numeric(difftime(Sys.time(), t0, units = 'secs')), 1), '\n')
cat('condition x plex:\n'); print(table(a$condition, a$plex)); cat('site x plex:\n'); print(table(a$site, a$plex))
cat('reference channel 16 occupied by a sample:', any(a$channel == 16 & !is.na(a$id)), '| positions per plex used:', paste(table(a$plex[!is.na(a$id)]), collapse = ','), '\n')
cat('condition x channel position (126 vs 134 end effects), cases per channel:', paste(tapply(a$condition == 'case', a$channel, sum, na.rm = TRUE), collapse = ' '), '\n')
