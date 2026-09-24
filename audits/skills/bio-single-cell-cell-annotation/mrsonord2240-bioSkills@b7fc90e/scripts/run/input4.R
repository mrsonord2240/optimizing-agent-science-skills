# Input 4 (Variant B) - bio-single-cell-cell-annotation
# Azimuth exactly as SKILL.md:109-116. Run on the REAL public 10x PBMC 1k v3 dataset
# (pbmcref is a curated human PBMC atlas, so a real PBMC query is the fair test).
# Checks the metadata column names the Skill hard-codes and the mapping-score gate.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({library(Seurat); library(Azimuth); library(SeuratData)})
cat('Azimuth', as.character(packageVersion('Azimuth')), '| Seurat',
    as.character(packageVersion('Seurat')), '\n')

P <- 'F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/public-data'
counts <- Read10X_h5(file.path(P, 'pbmc_1k_v3_filtered_feature_bc_matrix.h5'))
seurat_obj <- CreateSeuratObject(counts, min.cells = 3, min.features = 200)
cat('REAL 10x PBMC 1k v3:', ncol(seurat_obj), 'cells\n')

t0 <- Sys.time()
seurat_obj <- RunAzimuth(seurat_obj, reference = 'pbmcref')
cat('RunAzimuth took', round(as.numeric(difftime(Sys.time(), t0, units = 'secs')), 1), 's\n')

cols <- grep('predicted|mapping', colnames(seurat_obj@meta.data), value = TRUE)
cat('metadata columns Azimuth added:', paste(cols, collapse = ', '), '\n')

# the Skill's exact two lines
seurat_obj$azimuth <- seurat_obj$predicted.celltype.l2
seurat_obj$azimuth_low_conf <- seurat_obj$predicted.celltype.l2.score < 0.7
cat('SKILL.md:114-115 column names resolve:',
    all(c('predicted.celltype.l2', 'predicted.celltype.l2.score') %in% colnames(seurat_obj@meta.data)),
    '\n')

cat('\npredicted.celltype.l1:\n'); print(sort(table(seurat_obj$predicted.celltype.l1), decreasing = TRUE))
cat('\npredicted.celltype.l2 (top 12):\n')
print(head(sort(table(seurat_obj$predicted.celltype.l2), decreasing = TRUE), 12))
cat(sprintf('\nlow-confidence cells at the Skill\'s 0.7 gate: %d/%d (%.1f%%)\n',
            sum(seurat_obj$azimuth_low_conf), ncol(seurat_obj),
            100 * mean(seurat_obj$azimuth_low_conf)))
cat(sprintf('mapping.score: median %.3f, 5%% quantile %.3f; cells below 0.5: %d\n',
            median(seurat_obj$mapping.score), quantile(seurat_obj$mapping.score, 0.05),
            sum(seurat_obj$mapping.score < 0.5)))
cat(sprintf('prediction.score.l2 vs mapping.score correlation: %.3f\n',
            cor(seurat_obj$predicted.celltype.l2.score, seurat_obj$mapping.score)))

# marker triangulation, SKILL.md:155-158
canonical <- c('CD3D', 'CD8A', 'MS4A1', 'CD14', 'FCGR3A', 'NKG7', 'FCER1A')
present <- intersect(canonical, rownames(seurat_obj))
cat('\ncanonical markers present:', paste(present, collapse = ', '), '\n')
dp <- try({
  p <- DotPlot(seurat_obj, features = present, group.by = 'predicted.celltype.l1') +
    Seurat::RotatedAxis()
  ggplot2::ggsave('F:/OpenScience/audits/bio-single-cell-cell-annotation/run/input4_dotplot.png',
                  p, width = 7, height = 5, dpi = 90)
  'DotPlot rendered'
}, silent = TRUE)
cat('DotPlot:', if (inherits(dp, 'try-error')) paste('FAILED:', as.character(dp)) else dp, '\n')
ln <- LayerData(seurat_obj, assay = 'RNA', layer = 'data')
if (all(dim(ln) == 0)) { seurat_obj <- NormalizeData(seurat_obj, verbose = FALSE)
                         ln <- LayerData(seurat_obj, assay = 'RNA', layer = 'data') }
cat('mean normalized expression by predicted.celltype.l1:\n')
print(round(t(sapply(present, function(g)
  tapply(ln[g, ], seurat_obj$predicted.celltype.l1, mean))), 2))
cat('DONE\n')
