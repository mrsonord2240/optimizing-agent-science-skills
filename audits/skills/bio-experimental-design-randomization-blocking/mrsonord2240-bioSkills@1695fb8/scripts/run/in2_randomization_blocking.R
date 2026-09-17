# Input 2 (regression) -- Variant A: restricted randomization + run-order randomization
# Prompt: "Randomize 30 zebrafish embryos across 2 treatments (drug, vehicle), processed over
# 3 days (10/day) with day as a blocking factor. Also randomize processing order within each
# day. Give R code with a set seed."
set.seed(20260917)
units <- data.frame(id = sprintf('E%02d', 1:30),
                     day = rep(c('day1', 'day2', 'day3'), each = 10))
units$treatment <- ave(units$id, units$day,
                        FUN = function(ids) sample(rep(c('drug', 'vehicle'), length.out = length(ids))))
units$run_order <- ave(seq_len(nrow(units)), units$day, FUN = function(idx) sample(length(idx)))

bal <- table(units$day, units$treatment)
print(bal)
stopifnot(
  "each day must have exactly 5 drug and 5 vehicle" = all(bal == 5),
  "run_order must be a within-day permutation of 1:10" =
    all(sapply(split(units$run_order, units$day), function(x) setequal(x, 1:10)))
)
cat('Balance + run-order assertions passed.\n')
