#!/usr/bin/env Rscript
# Phase 2 static-executability check: each shipped R program must parse before runtime routing.
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 1L, dir.exists(args[[1]]))
files <- sort(list.files(args[[1]], pattern = '\\.R$', full.names = TRUE))
stopifnot(length(files) == 6L)
for (f in files) {
  parse(file = f)
  cat('PARSE PASS', basename(f), '\n')
}
