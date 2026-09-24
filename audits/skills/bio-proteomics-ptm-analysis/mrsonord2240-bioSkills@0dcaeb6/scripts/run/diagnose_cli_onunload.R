cat("before-cli\n")
library(cli)
ns <- asNamespace("cli")
cat("has-onUnload=", exists(".onUnload", envir = ns, inherits = FALSE), "\n", sep = "")
if (exists(".onUnload", envir = ns, inherits = FALSE)) {
  print(get(".onUnload", envir = ns, inherits = FALSE))
  unlockBinding(".onUnload", ns)
  assign(".onUnload", function(libpath) invisible(NULL), envir = ns)
  lockBinding(".onUnload", ns)
}
cat("patched-onUnload\n")
q(save = "no", status = 0, runLast = FALSE)
