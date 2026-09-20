suppressMessages({library(MARVEL)})
cat('MARVEL', as.character(packageVersion('MARVEL')), '\n')
cat('Seurat installed:', requireNamespace('Seurat', quietly=TRUE), ' data.table:', requireNamespace('data.table', quietly=TRUE), ' rtracklayer:', requireNamespace('rtracklayer', quietly=TRUE), '\n')
for (f in c('CreateMarvelObject','ComputePSI','AssignModality','CompareValues','CreateMarvelObject.10x','AnnotateSJ.10x','CheckAlignment','ComputePSI.10x','CompareValues.10x','AssignModality.10x')) {
  if (exists(f)) { cat('\n##', f, '\n'); print(names(formals(get(f)))) } else cat('\n##', f, 'DOES NOT EXIST\n')
}
cat('\nexports:\n'); print(sort(getNamespaceExports('MARVEL')))
