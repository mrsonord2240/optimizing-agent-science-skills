# Input 1 (regression) -- Canonical: EU/pseudoreplication
# Prompt: "I measured a marker in 300 cells from each of 4 control and 4 treated mice.
# A reviewer says my n is 4, not 1200 -- how should I analyze this?"
# Follows SKILL.md's "Choosing and Counting the Experimental Unit" pattern verbatim.
suppressPackageStartupMessages(library(dplyr))

set.seed(101)
n_per_group <- 4
cells_per_animal <- 300
cells <- expand.grid(cell = seq_len(cells_per_animal),
                      donor = paste0('M', seq_len(2 * n_per_group)))
cells$condition <- ifelse(as.integer(sub('M', '', cells$donor)) <= n_per_group, 'ctrl', 'treat')
donor_effect <- setNames(rnorm(length(unique(cells$donor)), 0, 0.5), unique(cells$donor))
cells$measurement <- donor_effect[cells$donor] +
  ifelse(cells$condition == 'treat', 0.3, 0) + rnorm(nrow(cells), 0, 1)

cat('=== WRONG: cell-level t-test (pseudoreplicated) ===\n')
wrong <- t.test(measurement ~ condition, data = cells)
cat(sprintf('n = %d, p = %.3e, df = %.1f\n', nrow(cells), wrong$p.value, wrong$parameter))

eu_level <- cells |>
  group_by(donor, condition) |>
  summarise(value = mean(measurement), .groups = 'drop')

cat('\n=== CORRECT: experimental units (n) per group ===\n')
print(table(eu_level$condition))

cat('\n=== CORRECT: animal-level t-test (true EU) ===\n')
right <- t.test(value ~ condition, data = eu_level)
cat(sprintf('n = %d, p = %.4f, df = %.2f\n', nrow(eu_level), right$p.value, right$parameter))

stopifnot(
  "EU count must be 4/4, not 1200/1200" = all(table(eu_level$condition) == 4),
  "cell-level and EU-level p-values must differ by orders of magnitude" =
    abs(log10(wrong$p.value) - log10(right$p.value)) > 5
)
cat('\nAssertions passed.\n')
