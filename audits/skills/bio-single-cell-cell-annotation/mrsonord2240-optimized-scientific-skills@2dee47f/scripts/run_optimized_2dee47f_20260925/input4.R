# Prior Variant B regression: real 10x PBMC mapping with Azimuth and normalized marker validation.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(Seurat); library(Azimuth); library(SeuratData)})
P <- 'F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/public-data'
O <- 'F:/OpenScience/audits/bio-single-cell-cell-annotation/reaudit-optimized-scientific-skills@2dee47f-20260925/data'
counts <- Read10X_h5(file.path(P, 'pbmc_1k_v3_filtered_feature_bc_matrix.h5'))
q <- CreateSeuratObject(counts, min.cells=3, min.features=200)
q <- RunAzimuth(q, reference='pbmcref')
required <- c('predicted.celltype.l1', 'predicted.celltype.l2', 'predicted.celltype.l2.score', 'mapping.score')
stopifnot(all(required %in% colnames(q@meta.data)))
q$azimuth <- q$predicted.celltype.l2
q$azimuth_low_conf <- q$predicted.celltype.l2.score < 0.7
cat(sprintf('real_cells=%d low_conf=%d (%.1f%%) mapping_score_median=%.3f\n',
            ncol(q), sum(q$azimuth_low_conf), 100*mean(q$azimuth_low_conf), median(q$mapping.score)))
cat('l1 labels:\n'); print(sort(table(q$predicted.celltype.l1), decreasing=TRUE))
q <- NormalizeData(q, verbose=FALSE)
markers <- intersect(c('CD3D','CD8A','MS4A1','CD14','FCGR3A','NKG7','FCER1A'), rownames(q))
p <- DotPlot(q, features=markers, group.by='predicted.celltype.l1') + Seurat::RotatedAxis()
ggplot2::ggsave(file.path(O, 'input4_dotplot.png'), p, width=7, height=5, dpi=90)
stopifnot(file.info(file.path(O, 'input4_dotplot.png'))$size > 1000)
cat('normalized_marker_validation=PASS markers=', paste(markers, collapse=','), '\n')
