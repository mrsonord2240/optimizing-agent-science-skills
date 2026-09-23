# Input 5: exercise current MS-DIAL import script with a representative export.
tmp <- tempfile(fileext = '.mdalign')
hdr <- c(
  paste(c('', '', 'Class', 'QC', 'Control', 'Treatment', 'Blank', 'Standard'), collapse = '\t'),
  paste(c('', '', 'FileType', 'QC', 'Sample', 'Sample', 'Blank', 'Standard'), collapse = '\t'),
  paste(c('', '', 'InjectionOrder', '1', '2', '3', '4', '5'), collapse = '\t'),
  paste(c('', '', 'Batch', '1', '1', '2', '2', '2'), collapse = '\t')
)
body <- c(
  'Alignment ID\tAverage Mz\tAverage Rt(min)\tQC\tControl\tTreatment\tBlank\tStandard',
  '1\t100.1\t1.5\t1000\t0\t2500\t99\t88',
  '2\t200.2\t2.0\t0\t1250\t0\t77\t66'
)
writeLines(c(hdr, body), tmp)
export_file <- tmp
source('F:/OpenScience/wt/workflows-metabolomics-pipeline/workflows/metabolomics-pipeline/scripts/msdial_import.R')
cat('Imported columns:', paste(colnames(feat), collapse = ', '), '\n')
cat('Imported row names:', paste(rownames(feat), collapse = ', '), '\n')
stopifnot(identical(dim(feat), c(2L, 3L)), identical(sample_class, c('QC', 'Control', 'Treatment')),
          !any(c('Blank', 'Standard') %in% colnames(feat)), is.na(feat['FT1', 'Control']),
          is.na(feat['FT2', 'QC']), identical(as.numeric(defs$rtmed), c(90, 120)),
          identical(injection_order, c(1L, 2L, 3L)), identical(batch_id, c(1L, 1L, 2L)))
cat('MS-DIAL import PASS: 2x3 feature matrix; zeros converted to NA; Blank/Standard excluded; RT converted to seconds.\n')
unlink(tmp)
