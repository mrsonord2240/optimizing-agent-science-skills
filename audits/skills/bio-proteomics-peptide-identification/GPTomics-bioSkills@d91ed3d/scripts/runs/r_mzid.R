.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
f <- 'F:/OpenScience/audits/bio-proteomics-peptide-identification/data/search_results.mzid'
# Skill: mzID::mzID() + flatten()
m <- mzID::mzID(f); d1 <- mzID::flatten(m)
cat('mzID+flatten:', nrow(d1), 'rows', ncol(d1), 'cols; isdecoy table:\n'); print(table(d1$isdecoy))
# Skill: mzR::openIDfile() + psms()
id <- mzR::openIDfile(f); d2 <- mzR::psms(id)
cat('mzR openIDfile+psms:', nrow(d2), 'rows; isDecoy table:\n'); print(table(d2$isDecoy))
# Skill says this 'does not exist':
d3 <- MSnbase::readMzIdData(f); cat('MSnbase::readMzIdData:', nrow(d3), 'rows\n')
