suppressMessages(library(Sierra)); cat('Sierra', as.character(packageVersion('Sierra')), '\n')
for (f in c('FindPeaks','CountPeaks','AnnotatePeaksFromGTF','NewPeakSeurat','DUTest','DetectUTRLengthShift','MergePeakCoordinates','PeakSeuratFromTransfer','PeakSeuratFromSeurat')) {
  if (exists(f)) { cat('\n##', f, ':', paste(names(formals(get(f))), collapse=', '), '\n') } else cat('\n##', f, 'DOES NOT EXIST\n') }
cat('\nexports:', paste(sort(getNamespaceExports('Sierra')), collapse=', '), '\n')
