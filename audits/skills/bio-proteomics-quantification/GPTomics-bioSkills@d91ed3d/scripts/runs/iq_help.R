.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
h <- function(topic, pkg) { f <- utils:::index.search(topic, find.package(pkg)); tools::Rd2txt(utils:::.getHelpFile(f), options=list(underline_titles=FALSE)) }
h('maxLFQ','iq'); h('preprocess','iq')
