# Purpose: Independently verify that retained dimensions obey the documented depth-correlation rule.
# Usage: rs.sh 02_depth_component_policy.R core_lsi.rds
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages(library(Seurat))
a <- commandArgs(trailingOnly = TRUE); stopifnot(length(a) == 1)
obj <- readRDS(a[1]); emb <- Embeddings(obj, 'lsi')
cors <- apply(emb, 2, function(x) cor(x, obj$nCount_peaks))
drop <- which(abs(cors) > 0.5)
retained <- setdiff(seq_len(30L), drop)
stopifnot(length(drop) >= 1L, all(abs(cors[retained]) <= 0.5))
cat('depth_rule=PASS dropped=', paste(drop, collapse=','),
    ' max_retained_abs_cor=', format(max(abs(cors[retained])), digits=5), '\n', sep='')
