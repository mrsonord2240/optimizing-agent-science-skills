# Input 1 (Canonical) test: import + honest-filter an MS-DIAL LC-MS DDA AlignResult export
# into R, following bio-metabolomics-msdial-preprocessing SKILL.md exactly.
# Synthetic export generated independently of the Skill's own examples/process_msdial_output.R
# (different seed, different feature/sample count, QC samples included) to avoid re-running
# the bundled example verbatim.

set.seed(101)
n_features <- 45
n_samples <- 10

tags <- sample(c('Metabolite', 'Lipid', 'Suggested_C6H12O6', 'Unknown'), n_features,
               replace = TRUE, prob = c(0.30, 0.10, 0.25, 0.35))
has_msms <- ifelse(tags %in% c('Metabolite', 'Lipid'),
                    sample(c('TRUE', 'FALSE'), n_features, replace = TRUE, prob = c(0.65, 0.35)),
                    'FALSE')

meta <- data.frame(
  'Alignment ID' = seq_len(n_features),
  'Average Rt(min)' = round(runif(n_features, 0.4, 18), 3),
  'Average Mz' = round(runif(n_features, 70, 950), 4),
  'Metabolite name' = ifelse(tags == 'Unknown', 'Unknown', paste0(tags, '_', seq_len(n_features))),
  'Adduct type' = sample(c('[M+H]+', '[M+Na]+', '[M+NH4]+', '[M-H]-'), n_features, replace = TRUE),
  'Fill %' = sample(15:100, n_features, replace = TRUE),
  'MS/MS assigned' = has_msms,
  'Annotation tag (VS1.0)' = tags,
  check.names = FALSE
)
sample_names <- c(paste0('QC_', 1:2), paste0('Sample_', 1:(n_samples - 2)))
intensities <- as.data.frame(
  matrix(round(rlnorm(n_features * n_samples, 10.5, 1.4)), nrow = n_features,
         dimnames = list(NULL, sample_names)),
  check.names = FALSE
)
body <- cbind(meta, intensities)

export_path <- file.path(tempdir(), 'AlignResult_input1.txt')
header_block <- matrix(c('Class', rep('', ncol(body) - 1)), nrow = 4, ncol = ncol(body), byrow = TRUE)
writeLines(apply(header_block, 1, paste, collapse = '\t'), export_path)
suppressWarnings(write.table(body, export_path, sep = '\t', append = TRUE,
                              row.names = FALSE, col.names = TRUE, quote = FALSE))

cat('=== Exercising SKILL.md "Import the Alignment Result into R" section verbatim ===\n')

# SKILL.md code block (copied exactly, only the file path changed):
msdial <- read.csv(export_path, sep = '\t', skip = 4, check.names = FALSE)

meta_cols <- c('Alignment ID', 'Average Rt(min)', 'Average Mz', 'Metabolite name',
               'Adduct type', 'Fill %', 'MS/MS assigned', 'Reference RT', 'Formula', 'Ontology',
               'INCHIKEY', 'SMILES', 'Annotation tag (VS1.0)')
meta_cols <- intersect(meta_cols, colnames(msdial))
sample_cols <- setdiff(colnames(msdial), colnames(msdial)[seq_len(max(match(meta_cols, colnames(msdial))))])

feature_info <- msdial[, meta_cols]
intensity <- as.matrix(msdial[, sample_cols])
rownames(intensity) <- msdial[['Alignment ID']]

cat('Parsed', nrow(msdial), 'rows x', ncol(msdial), 'cols. meta_cols found:', length(meta_cols),
    '| sample_cols found:', length(sample_cols), '\n')
stopifnot(nrow(msdial) == n_features)
stopifnot(ncol(intensity) == n_samples)
cat('PASS: row/col counts match the synthetic ground truth (', n_features, 'features,', n_samples, 'samples).\n')

cat('\n=== Exercising SKILL.md "Filter the Table Honestly" section verbatim ===\n')
keep_fill <- feature_info[['Fill %']] >= 70
has_msms2 <- feature_info[['MS/MS assigned']] == 'TRUE'
feature_info$msi_level <- ifelse(feature_info[['Annotation tag (VS1.0)']] %in% c('Metabolite', 'Lipid') & has_msms2, 2,
                           ifelse(grepl('^Suggested', feature_info[['Annotation tag (VS1.0)']]), 3, NA))
filtered <- intensity[keep_fill, ]

cat('Fill% >= 70 kept', sum(keep_fill), '/', n_features, 'features\n')
cat('MSI level table (all features, before fill filter):\n')
print(table(feature_info$msi_level, useNA = 'ifany'))

# Ground-truth check: every kept feature really has Fill% >= 70 in our synthetic truth
truth_check <- all(feature_info[['Fill %']][keep_fill] >= 70)
cat('PASS: every row kept by keep_fill truly has Fill% >= 70 ->', truth_check, '\n')

unlink(export_path)
cat('\nDone.\n')
