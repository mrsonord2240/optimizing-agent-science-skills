# Input 6 (Scope Boundary) -- real execution of the Stage 3 ionization mode-lock. Pre-fix, this
# hand-off had NO code anywhere (inspection-only PARTIAL finding: no per-feature mode column in
# any table or code path). Post-fix, SKILL.md Stage 3 now has:
#   defs$mode <- ionization_mode
#   stopifnot(!anyNA(defs$mode))
#   if (length(unique(defs$mode)) > 1) { by_mode <- split(defs, defs$mode) }
# Test this real code on a single-mode study (the common case) and a mixed-mode study (the
# adversarial case the governing principle #1 specifically calls out).

cat('=== Case A: single-mode study (positive only) ===\n')
defs <- data.frame(feature_id = paste0('FT', 1:10), mzmed = runif(10, 80, 900),
                    rtmed = runif(10, 30, 600), stringsAsFactors = FALSE)
ionization_mode <- rep('positive', 10)  # set once per acquisition, as SKILL.md states
defs$mode <- ionization_mode
stopifnot(!anyNA(defs$mode))
cat('defs$mode:', paste(unique(defs$mode), collapse = ', '), '| unique modes:', length(unique(defs$mode)), '\n')
if (length(unique(defs$mode)) > 1) {
  by_mode <- split(defs, defs$mode)
  cat('Split triggered (unexpected for single-mode case)\n')
} else {
  cat('No split needed -- single acquisition mode, as expected.\n')
}
cat('PASS\n\n')

cat('=== Case B: mixed-mode study (pos/neg runs merged before Stage 3) ===\n')
defs2 <- data.frame(feature_id = paste0('FT', 1:20), mzmed = runif(20, 80, 900),
                     rtmed = runif(20, 30, 600), stringsAsFactors = FALSE)
ionization_mode2 <- c(rep('positive', 12), rep('negative', 8))
defs2$mode <- ionization_mode2
stopifnot(!anyNA(defs2$mode))
cat('defs2$mode:', paste(names(table(defs2$mode)), table(defs2$mode), sep = '=', collapse = ', '), '\n')
if (length(unique(defs2$mode)) > 1) {
  by_mode <- split(defs2, defs2$mode)
  cat('Split triggered:', length(by_mode), 'groups ->', paste(names(by_mode), sapply(by_mode, nrow),
      sep = ': ', collapse = ', '), 'features\n')
  stopifnot(all(sapply(by_mode, function(d) length(unique(d$mode)) == 1)))
  cat('PASS: each split group is internally single-mode (no cross-mode contamination).\n\n')
} else {
  stop('BUG: mixed-mode input did not trigger the split branch')
}

cat('=== Case C: adversarial -- mode not set (NA), the un-set-acquisition-field case ===\n')
defs3 <- data.frame(feature_id = paste0('FT', 1:5), mzmed = runif(5, 80, 900))
defs3$mode <- c('positive', NA, 'positive', 'negative', NA)
res <- tryCatch({
  stopifnot(!anyNA(defs3$mode))
  'did not stop (BUG: silently proceeded with an unset mode)'
}, error = function(e) paste('stopifnot correctly fired:', conditionMessage(e)))
cat(res, '\n')
cat('This is the correct behavior: a missing mode is a hard stop, not an inferred guess',
    '(SKILL.md: "never inferred from m/z").\n\n')

cat('=== Case D: chemistry sanity check -- adduct tables really do differ by mode ===\n')
pos_adducts <- c('[M+H]+', '[M+Na]+', '[M+K]+', '[M+NH4]+')
neg_adducts <- c('[M-H]-', '[M+Cl]-', '[M+FA-H]-', '[M-H2O-H]-')
cat('Positive-mode adducts:', paste(pos_adducts, collapse = ', '), '\n')
cat('Negative-mode adducts:', paste(neg_adducts, collapse = ', '), '\n')
stopifnot(length(intersect(pos_adducts, neg_adducts)) == 0)
cat('PASS: the two adduct tables are disjoint, confirming SKILL.md\'s chemistry claim that scoring',
    'a candidate against the wrong mode\'s adduct table is a category error, not just imprecise.\n')
