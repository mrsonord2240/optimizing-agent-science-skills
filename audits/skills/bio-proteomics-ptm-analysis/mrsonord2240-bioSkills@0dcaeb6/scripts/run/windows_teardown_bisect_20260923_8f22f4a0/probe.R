#!/usr/bin/env Rscript
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2L || !(args[[1]] %in% c('base', 'package', 'dll'))) stop('usage: probe.R base|package|dll <name-or-path>')
mode <- args[[1]]
target <- args[[2]]
cat('R=', R.version.string, '\n', sep = '')
cat('mode=', mode, ' target=', target, '\n', sep = '')
if (mode == 'package') library(target, character.only = TRUE)
if (mode == 'dll') dyn.load(target)
dlls <- getLoadedDLLs()
for (n in names(dlls)) cat('DLL=', n, '|', dlls[[n]][['path']], '\n', sep = '')
cat('PROBE_BEFORE_EXIT_OK\n')
