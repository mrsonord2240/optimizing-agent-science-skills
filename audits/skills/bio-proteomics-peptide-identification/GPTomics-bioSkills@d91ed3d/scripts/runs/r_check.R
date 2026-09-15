.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
for (p in c('MSnbase','mzR','mzID','PSMatch')) cat(p, ':', requireNamespace(p, quietly=TRUE), if (requireNamespace(p, quietly=TRUE)) as.character(packageVersion(p)) else '', '\n')
cat('MSnbase exports readMzIdData:', 'readMzIdData' %in% getNamespaceExports('MSnbase'), '\n')
cat('mzR exports openIDfile:', 'openIDfile' %in% getNamespaceExports('mzR'), ' psms:', 'psms' %in% getNamespaceExports('mzR'), '\n')
suppressMessages(library(MSnbase))
f <- system.file('extdata','dummyiTRAQ.mzid', package='MSnbase')
if (!nzchar(f)) f <- dir(system.file(package='msdata'), pattern='mzid$', recursive=TRUE, full.names=TRUE)[1]
cat('example mzid:', f, '\n')
if (!is.na(f) && nzchar(f)) { d <- readMzIdData(f); cat('readMzIdData rows:', nrow(d), ' cols:', ncol(d), '\n'); print(head(names(d), 12)) }
