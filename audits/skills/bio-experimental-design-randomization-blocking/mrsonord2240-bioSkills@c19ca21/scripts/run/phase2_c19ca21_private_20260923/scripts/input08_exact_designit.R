set.seed(20260528)
units <- data.frame(id = sprintf('S%02d', 1:24),
                    block = rep(c('day1','day2','day3'), each = 8))
units$treatment <- ave(units$id, units$block,
                       FUN = function(ids) sample(rep(c('ctrl','treat'), length.out = length(ids))))
units$run_order <- sample(nrow(units))

library(designit)
bc <- BatchContainer$new(dimensions = c(processing_day = 3, position = 8))
bc <- assign_in_order(bc, samples = units)
scoring <- osat_score_generator(batch_vars = 'processing_day', feature_vars = 'treatment')
bc <- optimize_design(bc, scoring = scoring, n_shuffle = 2, check_score_variance = FALSE,
                      max_iter = 20, min_delta = 0.01, quiet = TRUE)
layout <- bc$get_samples(assignment = TRUE)
balance <- with(layout, table(processing_day, treatment))
stopifnot(all(balance == 4L), nrow(layout) == 24L, identical(sort(layout$run_order), seq_len(24L)))
write.csv(layout, '/mnt/openscience/audits/bio-experimental-design-randomization-blocking/run/phase2_c19ca21_private_20260923/outputs/input08_designit_layout.csv', row.names = FALSE)
cat('ASSERT designit_version=', as.character(packageVersion('designit')), '\n', sep='')
cat('ASSERT processing_day_balance=4/4/4\n')
cat('ASSERT layout_rows=24\n')
cat('ASSERT run_order_permutation=TRUE\n')
