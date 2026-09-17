# Input 2 (Variant A) — Randomization mechanics + blocking
# Prompt: "Randomize 30 zebrafish embryos across 2 treatments (drug, vehicle), processed
#  over 3 days (10/day) with day as a nuisance blocking factor. Also randomize processing
#  order within each day. Give R code with a set seed."
# SYNTHETIC unit list generated below.
# Following SKILL.md "Randomization Mechanics" + "Blocking and Local Control" patterns.

set.seed(20260917)  # record the seed for reproducibility

units <- data.frame(id = sprintf('E%02d', 1:30),
                     day = rep(c('day1', 'day2', 'day3'), each = 10))

# Restricted (block) randomization: randomize treatment WITHIN each block (day)
units$treatment <- ave(units$id, units$day,
                        FUN = function(ids) sample(rep(c('vehicle', 'drug'),
                                                        length.out = length(ids))))
# Randomize RUN ORDER so processing position is not confounded with treatment
units$run_order <- ave(seq_len(nrow(units)), units$day,
                        FUN = function(x) sample(seq_along(x)))

cat('=== Assignment table (first 10 rows) ===\n')
print(head(units, 10))

cat('\n=== Balance check: treatment x day (should be even within each day) ===\n')
bal <- table(units$day, units$treatment)
print(bal)

cat('\n=== ASSERTION CHECK ===\n')
cat('Every day has exactly 5 vehicle / 5 drug:',
    all(bal[, 'vehicle'] == 5) && all(bal[, 'drug'] == 5), '\n')
cat('Run order is a permutation of 1:10 within each day:',
    all(sapply(split(units$run_order, units$day), function(x) setequal(x, 1:10))), '\n')
cat('Seed recorded (20260917): TRUE\n')
