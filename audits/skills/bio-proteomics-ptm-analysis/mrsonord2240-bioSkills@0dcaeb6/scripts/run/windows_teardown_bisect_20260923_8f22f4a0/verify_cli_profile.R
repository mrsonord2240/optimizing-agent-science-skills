library(cli)
state <- get('clienv', envir = asNamespace('cli'), inherits = FALSE)
cat('cli_unloaded=', state$unloaded, '\n', sep = '')
cat('PROFILE_STATE_OBSERVED\n')
