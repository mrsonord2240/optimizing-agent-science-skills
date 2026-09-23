suppressMessages(library(lipidr))
source_path <- 'F:/OpenScience/wt/metabolomics-lipidomics/metabolomics/lipidomics/scripts/lipidr_import_checks.R'
source(source_path)

raw <- data.frame(
  Molecule = c('Cer 18:1;O2/16:0', 'HexCer 18:1;O1/16:0', 'SM 18:1;O3/16:0', 'Cer d18:1/16:0'),
  Sample_A = c(1200, 1100, 900, 1000),
  Sample_B = c(1250, 1080, 920, 1020),
  check.names = FALSE
)
converted <- to_lipidr_sphingoid(raw$Molecule)
expected <- c('Cer d18:1/16:0', 'HexCer m18:1/16:0', 'SM t18:1/16:0', 'Cer d18:1/16:0')
stopifnot(identical(converted, expected))
raw$Molecule <- converted
d <- import_with_class_check(raw, convert = FALSE)
classes <- as.character(rowData(d)$Class)
print(data.frame(Molecule = rowData(d)$Molecule, Class = classes))
stopifnot(!anyNA(classes), identical(classes, c('Cer', 'HexCer', 'SM', 'Cer')))
out <- 'F:/OpenScience/audits/bio-metabolomics-lipidomics/data/final-pass-20260923/sphingoid_input.csv'
write.csv(raw, out, row.names = FALSE)
cat(sprintf('PASS converted=%d class_na=%d input=%s\n', length(converted), sum(is.na(classes)), out))
