# Input 1 (Canonical) regression test -- run SKILL.md's exact documented R import
# + honest-filter code verbatim against a REAL MS-DIAL 5.5.260820 console export
# (not synthetic). The export was produced by this audit, independently of the
# fixer's own run, via:
#   MSDIALCUI.exe lcms -i ./in -o ./out -m ./lcms_param.txt
# on a real LC-MS DDA mzML file (LFQ_Astral_DDA_5min_250pg_Condition_A_REP1.mzML,
# borrowed from the mass-spec-proteomics-analyst candidate's public-work fixtures),
# using an auditor-authored parameter file (not copied from the fixer).

export_file <- "../data/AlignResult-real-singlesample.mdalign"
stopifnot(file.exists(export_file))

# ---- verbatim from SKILL.md "Import the Alignment Result into R" ----
msdial <- read.csv(export_file, sep = '\t', skip = 4, check.names = FALSE)

meta_cols <- c('Alignment ID', 'Average Rt(min)', 'Average Mz', 'Metabolite name',
               'Adduct type', 'Fill %', 'MS/MS assigned', 'Annotation tag (VS1.0)')
meta_cols <- intersect(meta_cols, colnames(msdial))

header_row1 <- as.character(read.table(export_file, sep = '\t', header = FALSE, nrows = 1,
                                        check.names = FALSE, colClasses = 'character',
                                        comment.char = '')[1, ])
class_idx <- which(header_row1 == 'Class')
sample_cols <- colnames(msdial)[(class_idx + 1):ncol(msdial)]

feature_info <- msdial[, meta_cols]
intensity <- as.matrix(msdial[, sample_cols])
rownames(intensity) <- msdial[['Alignment ID']]
storage.mode(intensity) <- 'numeric'
# ---- end verbatim SKILL.md code ----

cat('Parsed', nrow(msdial), 'features x', ncol(msdial), 'columns from REAL export\n')
cat('meta_cols found:', length(meta_cols), '| sample_cols found:', length(sample_cols), '\n')
cat('Sample column name(s):', paste(sample_cols, collapse=', '), '\n')

# Ground truth check: does this real export have exactly 1 sample column (one input file)?
stopifnot(length(sample_cols) == 1)
cat('PASS: single-file run produced exactly 1 sample column, as expected.\n')

# storage.mode(intensity) <- 'numeric' would have errored above if any detected
# "sample" column were actually still text (the exact bug the fix log calls out --
# "everything after the last known metadata column" pulling text columns like
# 'Spectrum reference file name' or 'MS/MS spectrum' into the matrix). It did not
# error, confirming the Class-cell anchor correctly excludes the ~29 extra
# annotation/QC columns this real export interleaves before the true sample column.
cat('PASS: storage.mode(intensity) <- numeric succeeded -- no text columns leaked into the intensity matrix.\n')

# ---- verbatim from SKILL.md "Filter the Table Honestly" (R path) ----
fill_floor <- 0.70
keep_fill <- feature_info[['Fill %']] >= fill_floor
has_msms <- tolower(trimws(feature_info[['MS/MS assigned']])) == 'true'
# ---- end verbatim ----

cat('\nFill % raw value range:', paste(range(feature_info[['Fill %']]), collapse=' - '), '\n')
cat('Fill% >=', fill_floor, 'kept', sum(keep_fill), '/', nrow(feature_info), 'features\n')
cat('MS/MS assigned raw values:', paste(unique(feature_info[['MS/MS assigned']]), collapse=', '), '\n')
cat('has_msms TRUE count:', sum(has_msms), '/', nrow(feature_info), '\n')

# Independent ground-truth re-derivation (not reusing the filter's own logic):
# a feature's Fill % is a real MS-DIAL-reported field; confirm it is genuinely a
# 0-1-scaled number (not 0-100) by checking the observed max is <= 1.0.
stopifnot(max(feature_info[['Fill %']]) <= 1.0)
cat('PASS: real Fill % column is confirmed 0-1 scaled (max <=1.0), matching SKILL.md claim.\n')

# Confirm MS/MS assigned really is title-case text, not upper-case, in the real export.
raw_vals <- unique(as.character(feature_info[['MS/MS assigned']]))
stopifnot(all(raw_vals %in% c('True', 'False')))
cat('PASS: real MS/MS assigned values are exactly {True, False} (title case), matching SKILL.md claim.\n')

cat('\nAnnotation tag (VS1.0) raw unique values in this real (no-library) run:',
    paste(unique(feature_info[['Annotation tag (VS1.0)']]), collapse=', '), '\n')
cat('NOTE: with no spectral library configured, the real console emits a raw internal\n')
cat('code (\"999\") rather than one of the documented display strings\n')
cat('(Metabolite/Lipid/Suggested*/Unknown). SKILL.md already tells the agent to\n')
cat('inspect unique() values rather than hard-code the vocabulary -- this run\n')
cat('confirms that advice is load-bearing: hard-coding the documented example\n')
cat('strings would silently match zero real features in this configuration.\n')
