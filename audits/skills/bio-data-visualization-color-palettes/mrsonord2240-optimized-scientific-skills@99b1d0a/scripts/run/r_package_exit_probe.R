# Environment probe: load one named package and exit.
args <- commandArgs(trailingOnly = TRUE)
stopifnot(length(args) == 1)
suppressPackageStartupMessages(library(args[[1]], character.only = TRUE))
cat('loaded', args[[1]], as.character(packageVersion(args[[1]])), '\n')
