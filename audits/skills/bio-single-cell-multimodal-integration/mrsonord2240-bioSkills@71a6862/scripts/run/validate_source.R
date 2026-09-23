.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))

source_root <- 'F:/OpenScience/wt/single-cell-multimodal-integration/single-cell/multimodal-integration'
r_files <- c(
  file.path(source_root, 'examples/cite_seq_analysis.R'),
  file.path(source_root, 'scripts/seurat_bridge_integration.R')
)
for (path in r_files) {
  parse(path)
  cat('R_PARSE_PASS', path, '\n')
}

py_files <- c(
  file.path(source_root, 'examples/cite_seq_analysis.py'),
  file.path(source_root, 'scripts/totalvi_cite_seq.py'),
  file.path(source_root, 'scripts/multivi_mosaic.py')
)
for (path in py_files) {
  output <- system2(
    'F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/Scripts/python.exe',
    c('-c', shQuote(sprintf("compile(open(r'%s', encoding='utf-8').read(), r'%s', 'exec'); print('PY_COMPILE_PASS')", path, path))),
    stdout = TRUE, stderr = TRUE
  )
  if (!is.null(attr(output, 'status'))) stop(paste(output, collapse = '\n'))
  cat('PY_PARSE_PASS', path, '\n')
}
cat('VALIDATION_COMPLETED\n')
