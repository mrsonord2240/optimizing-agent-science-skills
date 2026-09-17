# Input 6 (NEW, re-audit) -- "Using the ICH M10 QC data from Input 5 (2-day, 3-replicate,
# LLOQ/LOW/MID/HIGH), compute inter-day precision the way SKILL.md's new 'Precision: Intra-Day
# and Inter-Day (Nested ANOVA, Not Pooled SD)' subsection specifies, for ALL FOUR QC levels --
# not just the one level the fix log already checked -- and tell me whether the naive pooled-SD
# shortcut would have given a different pass/fail verdict at any level."
#
# Independently re-implemented from SKILL.md's prose + formula (not copied from the fix's own
# code block or the fix log), to re-derive the headline claim from first principles as the
# dispatch requires, and to check the new formula generalizes beyond the single cherry-picked
# LLOQ case the fixer verified.
#
# SKILL.md formula (verbatim from "Precision: Intra-Day and Inter-Day" subsection):
#   within-day variance  = MSwithin  (mean square error from aov(conc ~ factor(day)))
#   between-day variance = max(0, (MSbetween - MSwithin) / replicates_per_day)
#   total variance        = within + between
#   inter-day CV%         = sqrt(total variance) / grand_mean * 100

qc <- read.csv('F:/OpenScience/audits/bio-metabolomics-targeted-analysis/data/input5_ich_m10_validation.csv')

prec_tol <- function(level) ifelse(level == 'LLOQ', 20, 15)

levels_order <- c('LLOQ', 'LOW', 'MID', 'HIGH')
results <- do.call(rbind, lapply(levels_order, function(lvl) {
  g <- qc[qc$qc_level == lvl, ]

  # Naive pooled SD across both days' raw replicates (the WRONG shortcut SKILL.md now warns
  # against) -- this is what an agent might do if it only read the threshold table row without
  # the Precision subsection.
  naive_cv <- sd(g$measured_conc) / mean(g$measured_conc) * 100

  # Nested ANOVA variance-components approach, exactly as SKILL.md's Precision subsection
  # specifies (re-derived independently here, not copy-pasted from the Skill's own code block).
  fit <- aov(measured_conc ~ factor(day), data = g)
  ms <- summary(fit)[[1]][["Mean Sq"]]
  ms_between <- ms[1]
  ms_within  <- ms[2]
  n_per_day  <- nrow(g) / length(unique(g$day))
  var_within  <- ms_within
  var_between <- max(0, (ms_between - ms_within) / n_per_day)
  nested_cv <- sqrt(var_within + var_between) / mean(g$measured_conc) * 100

  tol <- prec_tol(lvl)
  data.frame(
    qc_level = lvl, tol_pct = tol,
    naive_pooled_cv = round(naive_cv, 2), naive_pass = naive_cv <= tol,
    nested_anova_cv = round(nested_cv, 2), nested_pass = nested_cv <= tol,
    verdicts_disagree = (naive_cv <= tol) != (nested_cv <= tol)
  )
}))

cat('=== Inter-day precision: naive pooled SD vs. nested ANOVA, all 4 QC levels ===\n')
print(results, row.names = FALSE)

cat('\n=== HEADLINE CHECK (independent re-derivation) ===\n')
lloq <- results[results$qc_level == 'LLOQ', ]
cat(sprintf('LLOQ naive pooled CV  = %.1f%% -> %s (tol %d%%)\n', lloq$naive_pooled_cv, ifelse(lloq$naive_pass, 'PASS', 'FAIL'), lloq$tol_pct))
cat(sprintf('LLOQ nested ANOVA CV  = %.1f%% -> %s (tol %d%%)\n', lloq$nested_anova_cv, ifelse(lloq$nested_pass, 'PASS', 'FAIL'), lloq$tol_pct))
cat('Naive method silently PASSES a level the nested method correctly FAILS:',
    lloq$naive_pass && !lloq$nested_pass, '\n')

cat('\n=== ASSERTION CHECKS ===\n')
cat('LLOQ naive pooled CV is within [18.5, 19.5) (matches fix log\'s 18.9% claim):',
    lloq$naive_pooled_cv >= 18.5 && lloq$naive_pooled_cv < 19.5, '\n')
cat('LLOQ nested ANOVA CV is within [20.5, 21.5) (matches fix log\'s 21.1% claim):',
    lloq$nested_anova_cv >= 20.5 && lloq$nested_anova_cv < 21.5, '\n')
cat('LLOQ verdicts disagree (naive PASS, nested FAIL) -- the exact defect the fix targeted:',
    lloq$naive_pass && !lloq$nested_pass, '\n')
cat('LOW/MID/HIGH: nested method introduces no new failures vs. naive on clean data:',
    all(!results$verdicts_disagree[results$qc_level != 'LLOQ']), '\n')
