# Input 1 regression: the MSstats summarization block, VERBATIM from the fork's
# SKILL.md, on the synthetic MaxQuant export.
suppressPackageStartupMessages({library(MSstats)})
cat('MSstats:', as.character(packageVersion('MSstats')), '\n')
QD <- 'F:/OpenScience/audits/bio-proteomics-quantification/data'
QW <- 'F:/OpenScience/audits/bio-proteomics-quantification/rerun4'
setwd(file.path(QW))
blk <- readLines(file.path(QW, 'blocks', 'msstats.R'))
cat('--- block as shipped ---\n'); cat(blk, sep = '\n'); cat('\n--- end ---\n')
blk <- gsub("'evidence.txt'", sprintf("'%s'", file.path(QD, 'evidence.txt')), blk, fixed = TRUE)
blk <- gsub("'proteinGroups.txt'", sprintf("'%s'", file.path(QD, 'proteinGroups.txt')), blk, fixed = TRUE)
blk <- gsub("'annotation.csv'", sprintf("'%s'", file.path(QD, 'annotation_msstats.csv')), blk, fixed = TRUE)
tf <- tempfile(fileext = '.R'); writeLines(blk, tf)
source(tf, echo = FALSE)
cat('[block verbatim] OK\n')
pld <- processed$ProteinLevelData
cat('ProteinLevelData rows:', nrow(pld), '| proteins:', length(unique(pld$Protein)),
    '| runs:', length(unique(pld$originalRUN)), '\n')
cat('NumImputedFeature > 0 rows:',
    if ('NumImputedFeature' %in% colnames(pld)) sum(pld$NumImputedFeature > 0) else NA, '\n')
med <- tapply(pld$LogIntensities, pld$originalRUN, median, na.rm = TRUE)
cat('per-run medians:', paste(round(med, 2), collapse = ' '), '\n')
