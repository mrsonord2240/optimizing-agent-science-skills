# Purpose: Fresh regression of documented logistic-regression differential accessibility.
# Usage: rs.sh 03_depth_aware_da.R obj_with_comparison_idents.rds da_markers.csv
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({ library(Seurat); library(Signac) })
a <- commandArgs(trailingOnly = TRUE); stopifnot(length(a) == 2)
obj <- readRDS(a[1]); DefaultAssay(obj) <- 'peaks'
groups <- levels(Idents(obj)); stopifnot(length(groups) >= 2L)
res <- FindMarkers(obj, ident.1 = groups[1], ident.2 = groups[2],
                   latent.vars = 'nCount_peaks', test.use = 'LR')
res$peak <- rownames(res); write.csv(res, a[2], row.names = FALSE)
stopifnot(nrow(res) > 0L, all(c('p_val', 'p_val_adj', 'peak') %in% colnames(res)))
cat('groups=', groups[1], ',', groups[2], ' da_rows=', nrow(res),
    ' adjusted_significant=', sum(res$p_val_adj < 0.05), '\n', sep='')
