# Input 5 (Stress) + Input 7 (new) -- run SKILL.md's exact documented R import
# + honest-filter code verbatim against a REAL 2-sample MS-DIAL 5.5.260820 console
# export produced via the CSV `-i` file-list mechanism SKILL.md documents in
# "Run MS-DIAL Headless" (acquisition_type column, DDA for both files here --
# no real DIA/ABF data was available, same limitation the fixer recorded):
#   MSDIALCUI.exe lcms -i ./filelist.csv -o ./out_csv -m ./lcms_param.txt
# filelist.csv:
#   file_path,file_name,file_type,class_id,acquisition_type,batch_order,analytical_order,factor
#   in/LFQ_Astral_DDA_5min_250pg_Condition_A_REP1.mzML,CondA,Sample,A,DDA,1,1,1
#   in/LFQ_Astral_DDA_5min_250pg_Condition_B_REP1.mzML,CondB,Sample,B,DDA,1,2,1
# This independently confirms: (a) the CSV `-i` mechanism runs to completion and
# produces a real multi-sample alignment (the fixer only confirmed "no parse
# error", not a completed run); (b) the CSV's file_name column sets the sample
# column headers (CondA/CondB), not the raw mzML file names; (c) a genuinely
# real, non-degenerate Fill% distribution (some features present in only 1/2
# samples -> 0.50, others in both -> 1.00) to exercise the >= 0.70 filter
# meaningfully, unlike the single-sample run where every kept feature is 1.00.

export_file <- "../data/AlignResult-real-multisample.mdalign"
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

cat('Parsed', nrow(msdial), 'features x', ncol(msdial), 'columns from REAL 2-sample export\n')
cat('Sample columns detected:', paste(sample_cols, collapse=', '), '\n')
stopifnot(identical(sample_cols, c('CondA', 'CondB')))
cat('PASS: sample columns are named from the CSV file_name column (CondA, CondB), not the raw .mzML filenames.\n')
cat('PASS: storage.mode(intensity) <- numeric succeeded on a real 2-sample export (no text-column leakage).\n')

# ---- verbatim from SKILL.md "Filter the Table Honestly" (R path) ----
fill_floor <- 0.70
keep_fill <- feature_info[['Fill %']] >= fill_floor
has_msms <- tolower(trimws(feature_info[['MS/MS assigned']])) == 'true'
# ---- end verbatim ----

cat('\nReal Fill % unique values:', paste(sort(unique(feature_info[['Fill %']])), collapse=', '), '\n')
tab <- table(feature_info[['Fill %']])
cat('Fill % value counts:\n'); print(tab)
cat('Fill% >=', fill_floor, 'kept', sum(keep_fill), '/', nrow(feature_info), 'features\n')

# Independent ground truth: every kept feature must be a real Fill%==1.00 (present
# in both of the 2 real samples) feature, since 0.50 (1/2 samples) is below 0.70.
stopifnot(all(feature_info[['Fill %']][keep_fill] == 1.00))
stopifnot(all(feature_info[['Fill %']][!keep_fill] == 0.50))
cat('PASS: the >=0.70 filter correctly separates real 2-of-2-sample features (kept) from real 1-of-2-sample features (dropped) -- no off-by-one or fraction/percent confusion.\n')

cat('\nMS/MS assigned raw unique values:', paste(unique(feature_info[['MS/MS assigned']]), collapse=', '), '\n')
cat('has_msms TRUE count:', sum(has_msms), '/', nrow(feature_info), '\n')

filtered_intensity <- intensity[keep_fill, ]
cat('\nFinal filtered intensity matrix:', nrow(filtered_intensity), 'features x', ncol(filtered_intensity), 'samples\n')
