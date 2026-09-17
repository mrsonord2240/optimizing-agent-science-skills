cat('R version:', R.version.string, '\n')
for (p in c('RNASeqPower','PROPER','edgeR','DESeq2','pwr')) {
  cat(p, ':', as.character(packageVersion(p)), '\n')
}
