.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(MSstats); library(MSnbase); library(iq)})
h <- function(topic, pkg) { f <- utils:::index.search(topic, find.package(pkg)); tools::Rd2txt(utils:::.getHelpFile(f), options=list(underline_titles=FALSE)) }
out <- capture.output(h('dataProcess','MSstats')); i <- grep('censoredInt|MBimpute', out); print(out[sort(unique(unlist(lapply(i, function(k) k:(k+3)))))])
out <- capture.output(h('makeImpuritiesMatrix','MSnbase')); cat(out[1:60], sep='\n')
cat('\niq version', as.character(packageVersion('iq')), '\n'); print(args(iq::maxLFQ))
