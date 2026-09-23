suppressMessages(library(lipidr))
datadir <- system.file('extdata', package = 'lipidr')
d_raw <- add_sample_annotation(
  read_skyline(list.files(datadir, 'A1_data.csv|F1_data.csv|F2_data.csv', full.names = TRUE)),
  file.path(datadir, 'clin.csv')
)
unclassified <- is.na(rowData(d_raw)$Class)
cat(sprintf('raw_lipids=%d raw_class_na=%d\n', nrow(d_raw), sum(unclassified)))
d_raw <- d_raw[!unclassified, ]

# Deliberately remove the recognized LPC internal-standard flag, then execute the exact
# coverage predicate used by scripts/istd_normalize.R.
rowData(d_raw)$istd[rowData(d_raw)$Class == 'LPC'] <- FALSE
istd_coverage <- table(rowData(d_raw)$Class, rowData(d_raw)$istd)
uncovered <- rownames(istd_coverage)[!('TRUE' %in% colnames(istd_coverage)) | istd_coverage[, 'TRUE'] == 0]
print(uncovered)
stopifnot(identical(uncovered, 'LPC'))
msg <- sprintf('No recognized internal standard for class(es): %s', paste(uncovered, collapse = ', '))
cat(sprintf('PASS missing_standard_guard=%s\n', msg))
