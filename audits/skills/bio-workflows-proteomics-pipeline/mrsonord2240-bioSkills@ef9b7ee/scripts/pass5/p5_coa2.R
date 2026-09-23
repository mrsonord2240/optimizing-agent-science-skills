.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressMessages(library(MSnbase))
setwd('F:/OpenScience/audits/bio-workflows-proteomics-pipeline/pass5/work4')
coa <- as.matrix(read.csv('tmt10_coa.csv', row.names = 1, check.names = FALSE))
cat('CoA names:', paste(rownames(coa), collapse=','), '\n')
cat('reporterNames(TMT10):', paste(reporterNames(TMT10), collapse=','), '\n')
dimnames(coa) <- list(reporterNames(TMT10), reporterNames(TMT10))
coa <- coa[reporterNames(TMT10), reporterNames(TMT10)]
raw <- readMSData('tmt.mzML', mode='onDisk')
q <- suppressMessages(quantify(raw, reporters=TMT10, method='max'))
tr <- t(coa); dimnames(tr) <- dimnames(coa)
bad <- purityCorrect(q, tr/100); good <- purityCorrect(q, coa/100)
cat('negatives, correct CoA:', sum(exprs(good)<0, na.rm=TRUE),
    '| negatives, TRANSPOSED CoA:', sum(exprs(bad)<0, na.rm=TRUE),
    '-> the pre-fix stopifnot(negatives==0) passes either way\n')
