# Phase 2 syntax evidence: parse every shipped R executable without modifying source.
paths <- c(
  'F:/OpenScience/wt/metabolomics-normalization-qc/metabolomics/normalization-qc/examples/normalize_data.R',
  'F:/OpenScience/wt/metabolomics-normalization-qc/metabolomics/normalization-qc/scripts/robust_dratio_filter.R'
)
for (path in paths) {
  parse(path)
  cat(sprintf('PARSE PASS: %s\n', path))
}
