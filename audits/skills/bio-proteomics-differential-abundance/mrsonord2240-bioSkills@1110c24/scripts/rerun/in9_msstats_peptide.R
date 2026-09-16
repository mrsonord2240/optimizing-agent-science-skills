# Input 9 (NEW, scope/coverage): reviewer asks for feature-level testing (msqrob2 or MSstats) from evidence.txt.
# The Skill names msqrob2/MSstats but gives no code for either; msqrob2 is not installed. The agent writes MSstats code.
# SYNTHETIC data (300-protein evidence subset).
source('F:/OpenScience/audits/bio-proteomics-differential-abundance/rerun/common.R')
cat('msqrob2 installed:', requireNamespace('msqrob2', quietly = TRUE), '\n')
suppressPackageStartupMessages(library(MSstats))
D <- file.path(RR, 'data')
ev <- read.table(file.path(D, 'evidence.txt'), sep = '\t', header = TRUE, quote = '', comment.char = '')
pg <- read.table(file.path(D, 'proteinGroups_evidence_subset.txt'), sep = '\t', header = TRUE, quote = '', comment.char = '')
ann <- read.csv(file.path(D, 'annotation_msstats.csv'))
truth <- read.csv(file.path(D, 'truth_proteins.csv'))
inp <- MaxQtoMSstatsFormat(evidence = ev, proteinGroups = pg, annotation = ann, use_log_file = FALSE)
proc <- dataProcess(inp, normalization = 'equalizeMedians', summaryMethod = 'TMP', censoredInt = 'NA', MBimpute = TRUE, use_log_file = FALSE)
cm <- matrix(c(-1, 1), nrow = 1, dimnames = list('Treatment-Control', c('Control', 'Treatment')))
gc <- groupComparison(contrast.matrix = cm, data = proc, use_log_file = FALSE)
r <- gc$ComparisonResult
r$Protein <- as.character(r$Protein)
cat('proteins tested:', nrow(r), '| issue table:', paste(names(table(r$issue, useNA = 'ifany')), table(r$issue, useNA = 'ifany'), collapse = ' '), '\n')
ok <- r[is.finite(r$log2FC) & !is.na(r$adj.pvalue), ]
truth_eval(ok$Protein[ok$adj.pvalue < 0.05], truth, 'MSstats TMP+AFT groupComparison adj.p<0.05')
inf <- r[!is.finite(r$log2FC), ]
cat('infinite log2FC rows (oneConditionMissing):', nrow(inf), '| classes:', paste(names(table(truth$class[match(inf$Protein, truth$protein)])), table(truth$class[match(inf$Protein, truth$protein)]), collapse = ' '), '\n')
