suppressMessages(library(rWikiPathways))
for (code in c('L','H','En')) {
  r <- tryCatch(getXrefList('WP554', code), error=function(e) e)
  if (inherits(r,'error')) cat(code, "ERROR:", conditionMessage(r), "\n") else cat(code, "-> n=", length(r), " sample:", paste(head(r,3),collapse=','), "\n")
}
