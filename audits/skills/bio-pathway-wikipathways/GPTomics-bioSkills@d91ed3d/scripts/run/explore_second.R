suppressMessages(library(rWikiPathways))
for (id in c('WP15','WP430','WP176','WP2059')) {
  info <- tryCatch(getPathwayInfo(id), error=function(e) e)
  if (inherits(info,'error')) { cat(id, "ERROR", conditionMessage(info), "\n"); next }
  genes <- tryCatch(getXrefList(id, 'L'), error=function(e) e)
  n <- if (inherits(genes,'error')) NA else length(genes)
  cat(id, "-", info$name, "- n genes:", n, "\n")
}
