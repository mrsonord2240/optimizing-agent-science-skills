.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(MSnbase))
print(getMethod('purityCorrect', c('MSnSet', 'matrix')))
f <- dir(system.file('extdata', package = 'MSnbase'), pattern = 'PurityCorrection', full.names = TRUE); print(basename(f))
for (x in f) { cat('\n==', basename(x), '\n'); cat(readLines(x), sep = '\n') }
