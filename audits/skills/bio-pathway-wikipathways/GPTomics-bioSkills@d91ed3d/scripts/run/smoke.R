suppressMessages({
  library(clusterProfiler)
  library(org.Hs.eg.db)
  library(rWikiPathways)
  library(tidyr)
})
cat("clusterProfiler:", as.character(packageVersion('clusterProfiler')), "\n")
cat("rWikiPathways:", as.character(packageVersion('rWikiPathways')), "\n")
cat("org.Hs.eg.db:", as.character(packageVersion('org.Hs.eg.db')), "\n")
cat("tidyr:", as.character(packageVersion('tidyr')), "\n")

t0 <- Sys.time()
orgs <- tryCatch(listOrganisms(), error = function(e) e)
cat("listOrganisms() took", as.numeric(Sys.time()-t0, units='secs'), "s\n")
if (inherits(orgs, 'error')) {
  cat("listOrganisms ERROR:", conditionMessage(orgs), "\n")
} else {
  cat("n organisms:", length(orgs), "\n")
  print(head(orgs, 10))
}
