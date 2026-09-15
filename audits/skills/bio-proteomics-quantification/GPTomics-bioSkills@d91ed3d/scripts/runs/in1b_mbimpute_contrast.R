.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Lead 2 check: MBimpute=FALSE (quantification Skill) vs MBimpute=TRUE (= the AFT route that differential-abundance calls "MSstats-AFT")
setwd('F:/OpenScience/audits/bio-proteomics-quantification/data')
suppressPackageStartupMessages(library(MSstats))
ev <- read.table('evidence.txt', sep = '\t', header = TRUE, quote = '', comment.char = '')
pg <- read.table('proteinGroups.txt', sep = '\t', header = TRUE, quote = '', comment.char = '')
annot <- read.csv('annotation_msstats.csv')
mi <- MaxQtoMSstatsFormat(evidence = ev, proteinGroups = pg, annotation = annot, use_log_file = FALSE, verbose = FALSE)
truth <- read.csv('truth_proteins.csv')
onoff <- truth$protein[truth$class == 'on_off']
res <- list()
for (mb in c(FALSE, TRUE)) {
  pr <- dataProcess(mi, normalization = 'equalizeMedians', summaryMethod = 'TMP', censoredInt = 'NA',
                    MBimpute = mb, use_log_file = FALSE, verbose = FALSE)
  pa <- as.data.frame(pr$ProteinLevelData)
  pa$prot1 <- sub(';.*', '', pa$Protein)
  sub <- pa[pa$prot1 %in% onoff, ]
  cat(sprintf('MBimpute=%s: protein-run rows=%d | on/off protein-run rows in Treatment runs=%d | NumImputedFeature>0 rows=%d\n',
              mb, nrow(pa), sum(grepl('^T', sub$originalRUN)), sum(pa$NumImputedFeature > 0, na.rm = TRUE)))
  if (mb) { cat('on/off proteins, Treatment-run TMP values after AFT imputation:\n'); print(sub[grepl('^T', sub$originalRUN), c('Protein', 'originalRUN', 'LogIntensities', 'NumMeasuredFeature', 'NumImputedFeature')], row.names = FALSE) }
  res[[as.character(mb)]] <- pr
}
# groupComparison on each: does the downstream step have any censoring model of its own?
cm <- matrix(c(-1, 1), nrow = 1, dimnames = list('T-C', c('Control', 'Treatment')))
for (mb in names(res)) {
  gc <- groupComparison(contrast.matrix = cm, data = res[[mb]], use_log_file = FALSE, verbose = FALSE)
  r <- gc$ComparisonResult; r$prot1 <- sub(';.*', '', r$Protein)
  o <- r[r$prot1 %in% onoff, c('Protein', 'log2FC', 'pvalue', 'issue')]
  cat(sprintf('\ngroupComparison after MBimpute=%s: %d proteins tested; on/off rows:\n', mb, nrow(r))); print(o, row.names = FALSE)
}
