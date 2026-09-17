# Input 1 (Canonical) — EU / pseudoreplication
# Prompt: "I measured a marker in 300 cells per animal, 4 control mice and 4 treated mice.
#  A reviewer flagged pseudoreplication. What's my true n and how do I correctly test for
#  a treatment effect on this marker?"
# SYNTHETIC DATA generated below (not real biological data).
# Following SKILL.md "Choosing and Counting the Experimental Unit" pattern exactly.

suppressPackageStartupMessages(library(dplyr))

set.seed(101)
n_animals_per_group <- 4
cells_per_animal <- 300

cells <- expand.grid(cell = seq_len(cells_per_animal),
                      animal = paste0('A', seq_len(2 * n_animals_per_group)))
cells$condition <- ifelse(as.integer(sub('A', '', cells$animal)) <= n_animals_per_group,
                           'ctrl', 'treat')
animal_effect <- setNames(rnorm(length(unique(cells$animal)), 0, 0.4), unique(cells$animal))
cells$measurement <- animal_effect[cells$animal] +
  ifelse(cells$condition == 'treat', 0.25, 0) + rnorm(nrow(cells), 0, 1)

# WRONG (what the reviewer flagged): naive t-test on all 2400 cells as if independent
wrong <- t.test(measurement ~ condition, data = cells)
cat('=== WRONG: cell-level t-test (n=2400, pseudoreplicated) ===\n')
cat('p =', wrong$p.value, '  df =', wrong$parameter, '\n\n')

# CORRECT per SKILL.md: aggregate to the experimental unit (animal) first
eu_level <- cells |>
  group_by(animal, condition) |>
  summarise(value = mean(measurement), .groups = 'drop')
cat('=== CORRECT: experimental units (n) per group ===\n')
print(table(eu_level$condition))

correct <- t.test(value ~ condition, data = eu_level)
cat('\n=== CORRECT: animal-level t-test (n=8 animals, true EU) ===\n')
cat('p =', correct$p.value, '  df =', correct$parameter, '\n')

cat('\n=== ASSERTION CHECK ===\n')
cat('True n per group == 4:', all(table(eu_level$condition) == 4), '\n')
cat('EU-level df ~= 6:', abs(correct$parameter - 6) < 1, '\n')
cat('Pseudoreplicated df (cell-level) >> EU df:', wrong$parameter > 100, '\n')
