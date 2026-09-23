# RE-AUDIT Input 1 (canonical): MaxQuant LFQ 4v4 with batch -> fixed "Complete R Workflow" block, VERBATIM. SYNTHETIC.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
PP <- 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
WD <- commandArgs(TRUE)[1]
setwd(file.path(PP,'rerun',WD)); set.seed(1)
blk <- list.files(file.path(PP,'rerun','blocks'), pattern='^b01', full.names=TRUE)
res <- tryCatch({ withCallingHandlers(sys.source(blk, envir=globalenv()),
  warning=function(w){cat('  [warning]', conditionMessage(w), '\n'); invokeRestart('muffleWarning')}); 'OK' },
  error=function(e) paste('ERROR:', conditionMessage(e)))
cat('[Complete R Workflow block verbatim]', res, '\n')
raw <- read.delim('proteinGroups.txt', stringsAsFactors=FALSE, quote='', comment.char='')
cat('file data lines:', length(readLines('proteinGroups.txt'))-1, '| rows read by the block:', if (exists('proteins')) NA else NA, '\n')
cat('flag column classes (default read.delim):', paste(sapply(read.delim('proteinGroups.txt', stringsAsFactors=FALSE)[,c('Reverse','Potential.contaminant','Only.identified.by.site')], class), collapse=' '), '\n')
if (exists('proteins')) cat('rows after the block filter:', nrow(proteins), '| all-NA rows:', sum(is.na(proteins$Protein.IDs)), '| REV/CON left:', sum(grepl('^(REV__|CON__)', proteins$Protein.IDs)), '\n')
if (exists('failed')) cat('failed samples flagged:', if (length(failed)) paste(failed, collapse=',') else '(none)', '\n')
if (exists('results')) {
  truth <- read.csv(file.path(PP,'data','truth_proteins.csv'), na.strings=character(0))
  id <- sub(';.*','',results$protein); cls <- truth$class[match(id, truth$protein)]; s <- results$significant
  cat(sprintf('treat(1.5-fold) BH<0.05: %d called | FALSE POS (null) %d | on_off %d | up %d | down %d | unmatched %d\n',
      sum(s), sum(cls[s]=='null',na.rm=TRUE), sum(cls[s]=='on_off',na.rm=TRUE), sum(cls[s]=='up',na.rm=TRUE), sum(cls[s]=='down',na.rm=TRUE), sum(is.na(cls[s]))))
  cat('true changers recovered:', sum(cls[s] %in% c('up','down')), 'of', sum(cls %in% c('up','down'), na.rm=TRUE), 'tested\n')
  cat('design columns:', colnames(design), '| batch in design:', has_batch, '\n')
  cat('contrast not estimable (NA logFC):', sum(is.na(results$logFC)), '\n')
  nn <- !is.na(cls) & cls=='null' & !is.na(results$logFC)
  cat(sprintf('null centre after median normalization: mean log2FC %+.4f (compositional-bias check)\n', mean(results$logFC[nn])))
  cat('RNG calls in block (set.seed/rnorm/runif/sample):', sum(sapply(c('set.seed','rnorm(','runif(','sample('), function(k) length(grep(k, readLines(blk), fixed=TRUE)))), 'hits')
}
