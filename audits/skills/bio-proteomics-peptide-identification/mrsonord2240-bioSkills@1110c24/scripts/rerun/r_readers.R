.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
# Re-audit 2026-09-15: the R readers SKILL.md names, on the SYNTHETIC mzid exported in the pre-fix audit.
f <- 'F:/OpenScience/audits/bio-proteomics-peptide-identification/data/search_results.mzid'
suppressPackageStartupMessages({library(mzID); library(mzR)})
x <- flatten(mzID(f)); cat('mzID::mzID + flatten rows:', nrow(x), ' decoys:', sum(x$isdecoy), '\n')
id <- openIDfile(f); ps <- psms(id); cat('mzR::openIDfile + psms rows:', nrow(ps), '\n')
cat('packageVersion mzID', as.character(packageVersion('mzID')), ' mzR', as.character(packageVersion('mzR')), '\n')
