for (p in c("FRASER", "OUTRIDER")) { d <- system.file(package = p); cat(p, as.character(packageVersion(p)), "| DESCRIPTION License:", packageDescription(p)$License, "\n")
  f <- list.files(d, pattern = "^LICEN[SC]E", full.names = TRUE); for (x in f) { cat("  ", basename(x), ":", substr(paste(readLines(x, warn = FALSE), collapse = " "), 1, 160), "\n") } }
