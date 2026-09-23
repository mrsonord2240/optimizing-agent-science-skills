for (f in list.files('F:/OpenScience/audits/bio-workflows-proteomics-pipeline/rerun/blocks', full.names=TRUE)) {
  r <- tryCatch({parse(f); 'PARSE OK'}, error=function(e) paste('PARSE FAIL:', conditionMessage(e)))
  cat(basename(f), '->', r, '\n')
}
