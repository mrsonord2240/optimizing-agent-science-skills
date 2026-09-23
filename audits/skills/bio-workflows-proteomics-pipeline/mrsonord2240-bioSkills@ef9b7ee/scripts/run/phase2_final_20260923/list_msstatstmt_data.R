#!/usr/bin/env Rscript
# Phase 2 audit helper: inventory the bundled MSstatsTMT fixture used by the shipped multiplex route.
library(MSstatsTMT)
fixture_root <- system.file(package = "MSstatsTMT")
stopifnot(nzchar(fixture_root), dir.exists(fixture_root))
files <- list.files(fixture_root, recursive = TRUE, full.names = TRUE)
cat(paste(files, collapse = "\n"), "\n")
