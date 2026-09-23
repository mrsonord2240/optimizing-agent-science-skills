.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(Seurat))
out <- readRDS('bridge_out.rds')
needed <- c('predicted.celltype', 'predicted.celltype.score', 'ref.umap')
missing <- setdiff(needed, c(colnames(out[[]]), Reductions(out)))
if (length(missing)) stop('Missing bridge outputs: ', paste(missing, collapse = ', '))
truth <- out$truth
acc <- mean(as.character(out$predicted.celltype) == as.character(truth))
cat(sprintf('BRIDGE_OUTPUT n=%d accuracy=%.3f labels=%s\n', ncol(out), acc,
            paste(sort(unique(as.character(out$predicted.celltype))), collapse = ',')))
if (acc <= 1/3) stop('Bridge accuracy did not exceed chance')
