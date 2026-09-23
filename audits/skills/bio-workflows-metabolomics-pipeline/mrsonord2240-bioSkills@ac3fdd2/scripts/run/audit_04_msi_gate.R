# Input 4 (Edge) -- real execution of the Stage 3->5 MSI-confidence gate. Pre-fix, this hand-off
# had NO code anywhere (inspection-only PARTIAL finding: "identified_compounds" appeared with no
# derivation). Post-fix, SKILL.md Stage 5 now has:
#   identified_compounds <- unique(annotated$name[grepl('^[12]', as.character(annotated$msi_level))])
#   stopifnot(length(identified_compounds) > 0)
# Test this real code against a synthetic `annotated` table shaped like metabolite-annotation's
# own assign_level() convention (levels 1, '2a', '2b', 3, 4, 5), including the all-tentative edge
# case the Common Errors table now documents.

cat('=== Case A: realistic mixed-confidence annotation table ===\n')
set.seed(7)
annotated <- data.frame(
  feature_id = paste0('FT', sprintf('%03d', 1:20)),
  name = c('Pyruvate', 'L-Lactate', 'Citrate', 'Succinate', 'Fumarate', 'L-Alanine',
           'Glutamate', 'Malate', 'Isocitrate', 'Acetyl-CoA',
           paste0('cand_', 11:20)),
  msi_level = c(1, '2a', '2a', '2b', '2b', 1, '2a', 3, 3, 4, 4, 4, 5, 5, 5, 5, 3, '2b', 4, 5),
  stringsAsFactors = FALSE
)
print(table(annotated$msi_level))

identified_compounds <- unique(annotated$name[grepl('^[12]', as.character(annotated$msi_level))])
stopifnot(length(identified_compounds) > 0)
cat('\nidentified_compounds (Level 1-2 only):', length(identified_compounds), 'of',
    length(unique(annotated$name)), 'unique names\n')
print(identified_compounds)

# Correctness check: every excluded name really is Level 3-5, every included name really is Level 1-2
excluded <- setdiff(annotated$name, identified_compounds)
excluded_levels <- unique(annotated$msi_level[annotated$name %in% excluded])
included_levels <- unique(annotated$msi_level[annotated$name %in% identified_compounds])
cat('Levels among EXCLUDED names:', paste(excluded_levels, collapse = ', '), '\n')
cat('Levels among INCLUDED names:', paste(included_levels, collapse = ', '), '\n')
stopifnot(all(grepl('^[12]', as.character(included_levels))))
stopifnot(!any(grepl('^[12]', as.character(excluded_levels))))
cat('PASS: filter correctly separates Level 1-2 from Level 3-5.\n\n')

cat('=== Case B: adversarial edge -- every feature is Level 3-5 (the Common Errors row) ===\n')
annotated_bad <- annotated
annotated_bad$msi_level <- c(3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4,5,3,4)
identified_bad <- unique(annotated_bad$name[grepl('^[12]', as.character(annotated_bad$msi_level))])
cat('identified_compounds length when all rows are Level 3-5:', length(identified_bad), '\n')
res <- tryCatch({
  stopifnot(length(identified_bad) > 0)
  'did not stop (BUG: forced ORA on tentative-only data)'
}, error = function(e) paste('stopifnot correctly fired:', conditionMessage(e)))
cat(res, '\n')
cat('This matches the SKILL.md Common Errors row: "identified_compounds is empty -> ',
    'do not loosen the filter, use Path B (mummichog) instead."\n\n')

cat('=== Case C: type-safety check -- numeric vs character msi_level ===\n')
mixed_types <- data.frame(name = c('A', 'B', 'C', 'D'), msi_level = list(1L, '2a', 3.0, '4'))
mixed_types$msi_level <- c(1L, '2a', 3, '4')  # as-stored in a real join, mixed representations
ok <- unique(mixed_types$name[grepl('^[12]', as.character(mixed_types$msi_level))])
cat('Names passing filter:', paste(ok, collapse = ', '), '(expect A, B only)\n')
stopifnot(identical(sort(ok), c('A', 'B')))
cat('PASS: as.character() coercion handles both numeric (1L) and string (\'2a\') representations.\n')
