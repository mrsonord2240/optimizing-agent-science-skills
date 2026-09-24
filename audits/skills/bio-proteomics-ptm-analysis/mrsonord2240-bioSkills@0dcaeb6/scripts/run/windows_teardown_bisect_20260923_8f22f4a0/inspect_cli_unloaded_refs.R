library(cli)
ns <- asNamespace('cli')
names_all <- ls(ns, all.names = TRUE)
refs <- vapply(names_all, function(name) {
  obj <- get(name, envir = ns, inherits = FALSE)
  is.function(obj) && grepl('unloaded', paste(deparse(obj), collapse = '\n'), fixed = TRUE)
}, logical(1))
cat('UNLOADED_REFERENCES=', paste(names_all[refs], collapse = '|'), '\n', sep = '')
