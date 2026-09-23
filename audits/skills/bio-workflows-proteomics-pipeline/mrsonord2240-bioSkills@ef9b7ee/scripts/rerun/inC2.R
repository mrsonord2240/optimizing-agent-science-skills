
# Re-audit Input C, part 2: isolate the two failure points of the Complete R Workflow block on a
# >2-condition design. (a) prcomp with zero complete cases; (b) the hard-coded two-level contrast.
.libPaths(c('F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(limma))
PP <- 'F:/OpenScience/audits/bio-workflows-proteomics-pipeline'
setwd(file.path(PP, 'rerun', 'workC'))
blk <- list.files(file.path(PP, 'rerun', 'blocks'), pattern = '^b01', full.names = TRUE)
src <- readLines(blk)
# (a) how the block dies at the QC step
cat('--- (a) PCA step, 0 complete cases ---\n')
i <- grep('prcomp', src); cat('offending line:', trimws(src[i]), '\n')
cat('block error was: "a dimension is zero" (prcomp on a 0-row matrix) - halts before any statistics\n')

# (b) neutralise ONLY the PCA lines and re-run, to reach the contrast step
src2 <- src
src2[grep('^pca <- prcomp', src2)] <- 'pca <- NULL'
src2[grep('^pca_df <- ', src2)] <- 'pca_df <- NULL'
tf <- tempfile(fileext = '.R'); writeLines(src2, tf)
e <- new.env(parent = globalenv())
r <- tryCatch({ suppressWarnings(sys.source(tf, envir = e)); 'OK' }, error = function(z) paste('ERROR:', conditionMessage(z)))
cat('\n--- (b) with the PCA lines neutralised, the block reaches the contrast step ---\n')
cat('[block minus PCA]', r, '\n')
if (exists('design', envir = e)) cat('design columns:', paste(colnames(get('design', envir = e)), collapse = ' '), '\n')
cat('\nConclusion: on a 3-level condition factor the block hard-codes makeContrasts(Treatment - Control)\n')
