suppressMessages(library(rWikiPathways))
r <- tryCatch(searchPathways('cancer','Homo sapiens'), error=function(e) e)
if (inherits(r,'error')) cat("searchPathways ERROR (as documented):", conditionMessage(r), "\n") else cat("searchPathways succeeded unexpectedly\n")
