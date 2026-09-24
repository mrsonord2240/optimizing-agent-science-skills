library(cli)
ns <- asNamespace('cli')
matches <- grep('unload|cleanup|final', ls(ns, all.names = TRUE), value = TRUE, ignore.case = TRUE)
cat('MATCHES=', paste(matches, collapse = '|'), '\n', sep = '')
for (name in matches) {
  obj <- get(name, envir = ns, inherits = FALSE)
  if (is.function(obj)) {
    cat('FUNCTION=', name, '\n', sep = '')
    print(obj)
  }
}
cat('ONUNLOAD_EXISTS=', exists('.onUnload', envir = ns, inherits = FALSE), '\n', sep = '')
if (exists('.onUnload', envir = ns, inherits = FALSE)) print(get('.onUnload', envir = ns, inherits = FALSE))
