cat("before-cli\n")
library(cli)
ns <- asNamespace("cli")
cli_state <- get("clienv", envir = ns)
cli_state$unloaded <- TRUE
cat("marked-unloaded\n")
q(save = "no", status = 0, runLast = FALSE)
