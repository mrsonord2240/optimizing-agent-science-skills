.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Input 4 (Variant B), R half: the Skill names QFeatures::readQFeatures() + aggregateFeatures() but gives no R code.
# This is the code Claude-with-this-Skill writes from the Skill's rules (flags, leading ID, LFQ columns, 0 -> NA, log2).
# Data SYNTHETIC: proteinGroups_failed.txt.
suppressPackageStartupMessages(library(QFeatures))
pg <- read.delim('F:/OpenScience/audits/bio-proteomics-data-import/data/proteinGroups_failed.txt',
                 check.names = FALSE, stringsAsFactors = FALSE)
cat('flag column classes:', sapply(pg[c('Reverse', 'Potential contaminant', 'Only identified by site')], class), '\n')
pg$leading_protein <- sub(';.*', '', pg[['Protein IDs']])
lfq <- grep('^LFQ intensity ', names(pg))
qf <- readQFeatures(pg, quantCols = lfq, name = 'proteins', fnames = 'leading_protein')
cat('features read:', nrow(qf[['proteins']]), '\n')
res <- try(filterFeatures(qf, ~ Reverse != '+' & `Potential contaminant` != '+' & `Only identified by site` != '+'), silent = TRUE)
if (inherits(res, 'try-error')) {
  cat('ATTEMPT 1 (backticked MaxQuant names) FAILED:', conditionMessage(attr(res, 'condition')), '\n')
  # adaptation: syntactic rowData names before filtering
  rd <- rowData(qf[['proteins']])
  names(rd) <- make.names(names(rd))
  rowData(qf[['proteins']]) <- rd
  qf <- filterFeatures(qf, ~ Reverse != '+' & Potential.contaminant != '+' & Only.identified.by.site != '+')
} else qf <- res
cat('after flag filter:', nrow(qf[['proteins']]), '\n')
qf <- zeroIsNA(qf, 'proteins')
qf <- logTransform(qf, i = 'proteins', name = 'log2_lfq', base = 2)
a <- assay(qf[['log2_lfq']])
cat('any -Inf:', any(is.infinite(a)), '| NA %:', round(100 * mean(is.na(a)), 1), '\n')
print(round(apply(a, 2, median, na.rm = TRUE), 2))
# edge: a flag column that is entirely empty is read as logical NA -> does filterFeatures keep or drop the rows?
pg2 <- pg; pg2[['Only identified by site']] <- NA
names(pg2) <- sub('^Potential contaminant$', 'Potential.contaminant', sub('^Only identified by site$', 'Only.identified.by.site', names(pg2)))
qf2 <- readQFeatures(pg2, quantCols = lfq, name = 'proteins', fnames = 'leading_protein', verbose = FALSE)
qf2 <- filterFeatures(qf2, ~ Reverse != '+' & Potential.contaminant != '+' & Only.identified.by.site != '+')
cat('[AUDIT] all-empty site column (logical NA): features kept =', nrow(qf2[['proteins']]), '(expect 1515: 25 REV + 20 CON removed, NA rows kept, not dropped)\n')
