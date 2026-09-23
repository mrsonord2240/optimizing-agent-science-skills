# New independent input: execute the inline Milo design construction with only
# the libraries printed by SKILL.md.  The source block calls dplyr::distinct()
# but does not load dplyr; this minimal runnable probe reaches that exact line.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(miloR)
  library(SingleCellExperiment)
})

design_source_shape <- data.frame(
  sample = c('S1', 'S1', 'S2', 'S2'),
  condition = c('control', 'control', 'treated', 'treated')
)
cat('miloR=', as.character(packageVersion('miloR')), '\n', sep = '')
cat('dplyr attached before source-faithful call=', 'package:dplyr' %in% search(), '\n', sep = '')
result <- try(distinct(design_source_shape), silent = TRUE)
if (inherits(result, 'try-error')) {
  cat('EXPECTED_SOURCE_FAILURE=', conditionMessage(attr(result, 'condition')), '\n', sep = '')
} else {
  cat('UNEXPECTED_SUCCESS_ROWS=', nrow(result), '\n', sep = '')
  quit(status = 2)
}
