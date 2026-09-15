.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(QFeatures))
cat('QFeatures', as.character(packageVersion('QFeatures')), '\n')
cat('readQFeatures exists:', exists('readQFeatures'), '\n')
print(args(readQFeatures))
cat('aggregateFeatures exists:', exists('aggregateFeatures'), '| zeroIsNA:', exists('zeroIsNA'),
    '| filterFeatures:', exists('filterFeatures'), '| logTransform:', exists('logTransform'), '\n')
cat('Spectra installed:', requireNamespace('Spectra', quietly = TRUE), '\n')
cat('MSnbase installed:', requireNamespace('MSnbase', quietly = TRUE), '\n')
