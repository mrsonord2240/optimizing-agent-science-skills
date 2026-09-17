suppressMessages({
  ok <- function(p) tryCatch({requireNamespace(p, quietly=TRUE)}, error=function(e) FALSE)
})
for (p in c('GOSemSim','viridis','ggtangle','clusterProfiler','enrichplot','org.Hs.eg.db')) {
  cat(p, ":", ok(p), if(ok(p)) as.character(packageVersion(p)) else "", "\n")
}
