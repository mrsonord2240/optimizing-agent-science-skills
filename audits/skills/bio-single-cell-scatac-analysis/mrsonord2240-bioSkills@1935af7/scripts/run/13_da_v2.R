.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(Signac); library(Seurat); library(GenomicRanges)
})
data_dir <- 'F:/OpenScience/audits/bio-single-cell-scatac-analysis/data/reaudit_v2_20260919'
obj <- readRDS(file.path(data_dir, 'obj_qc.rds'))
cat('Loaded object:', ncol(obj), 'cells x', nrow(obj), 'peaks\n')

DefaultAssay(obj) <- 'peaks'
da <- FindMarkers(obj, ident.1 = 'Tcell', ident.2 = 'Bcell', group.by = 'cell_type',
                   test.use = 'LR', latent.vars = 'nCount_peaks')
cat('DA peaks found (p_val_adj<0.05):', sum(da$p_val_adj < 0.05), 'of', nrow(da), 'tested\n')
da_sig <- da[da$p_val_adj < 0.05, ]
da_sig <- da_sig[order(da_sig$p_val_adj), ]

gene_windows <- readRDS(file.path(data_dir, 'gene_windows.rds'))
peak_gr <- StringToGRanges(rownames(da_sig), sep = c(':', '-'))
ov <- findOverlaps(peak_gr, gene_windows)
cat('Of', length(peak_gr), 'significant DA peaks (Tcell vs Bcell),', length(unique(queryHits(ov))),
    'overlap a known marker-gene window (expected: mostly CD3D/MS4A1)\n')
if (length(ov) > 0) print(table(names(gene_windows)[subjectHits(ov)]))
cat('STAGE 4 (v2 DA) DONE\n')
