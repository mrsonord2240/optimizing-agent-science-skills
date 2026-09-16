# Input 2 (Variant A) - bio-workflows-scrnaseq-pipeline
# The "Complete R Workflow" block, SKILL.md:339-395, run VERBATIM (only data_dir/output_dir
# repointed) on one SYNTHETIC sample, then scored against ground truth so the cost of the
# single-sample, filtered-matrix, flat-cutoff shortcuts is visible.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
library(Seurat)
library(scDblFinder)
library(ggplot2)
library(dplyr)

D <- 'F:/OpenScience/audits/_partial-20260911/bio-workflows-scrnaseq-pipeline/data/synthetic_pbmc_8samples'
data_dir <- file.path(D, 'S2/outs/filtered_feature_bc_matrix')
output_dir <- 'F:/OpenScience/audits/bio-workflows-scrnaseq-pipeline/run/input2_results'
dir.create(output_dir, showWarnings = FALSE)
set.seed(20260916)

counts <- Read10X(data.dir = data_dir)
seurat_obj <- CreateSeuratObject(counts = counts, min.cells = 3, min.features = 200)
cat('Initial cells:', ncol(seurat_obj), '\n')

seurat_obj[['percent.mt']] <- PercentageFeatureSet(seurat_obj, pattern = '^MT-')
seurat_obj <- subset(seurat_obj, nFeature_RNA > 200 & nFeature_RNA < 5000 & percent.mt < 20)
cat('After QC:', ncol(seurat_obj), '\n')

sce <- as.SingleCellExperiment(seurat_obj)
sce <- scDblFinder(sce)
seurat_obj$doublet <- sce$scDblFinder.class
seurat_obj <- subset(seurat_obj, doublet == 'singlet')
cat('After doublet removal:', ncol(seurat_obj), '\n')

seurat_obj <- SCTransform(seurat_obj, verbose = FALSE)
seurat_obj <- RunPCA(seurat_obj, npcs = 50, verbose = FALSE)
seurat_obj <- RunUMAP(seurat_obj, dims = 1:30, verbose = FALSE)
seurat_obj <- FindNeighbors(seurat_obj, dims = 1:30, verbose = FALSE)
seurat_obj <- FindClusters(seurat_obj, resolution = 0.5, verbose = FALSE)

markers <- FindAllMarkers(seurat_obj, only.pos = TRUE, min.pct = 0.25, logfc.threshold = 0.25)
write.csv(markers, file.path(output_dir, 'markers.csv'))
saveRDS(seurat_obj, file.path(output_dir, 'seurat_object.rds'))
pdf(file.path(output_dir, 'umap.pdf'), width = 10, height = 8)
DimPlot(seurat_obj, reduction = 'umap', label = TRUE)
dev.off()
cat('Pipeline complete. Object saved to:', output_dir, '\n')

## ---- audit additions: what did the verbatim block actually achieve? ----
cat('\n=== AUDIT ===\n')
cat('files written:', paste(list.files(output_dir), collapse=', '), '\n')
cat('marker rows:', nrow(markers), '| clusters:', length(unique(Idents(seurat_obj))), '\n')
tc <- read.csv(file.path(D, 'truth_cells.csv'))
tc$true_doublet <- tc$true_doublet %in% c('True','TRUE',TRUE)
tc$true_low_quality <- tc$true_low_quality %in% c('True','TRUE',TRUE)
tc <- tc[tc$sample == 'S2', ]; rownames(tc) <- tc$barcode
kept <- colnames(seurat_obj)
ari <- function(x,y){t<-table(x,y);n<-sum(t);s<-sum(choose(t,2));a<-sum(choose(rowSums(t),2))
  b<-sum(choose(colSums(t),2));e<-a*b/choose(n,2);(s-e)/((a+b)/2-e)}
cat(sprintf('true doublets: %d injected, %d still present after the block (%.0f%% removed)\n',
            sum(tc$true_doublet), sum(tc[kept,'true_doublet']),
            100*(1-sum(tc[kept,'true_doublet'])/sum(tc$true_doublet))))
cat(sprintf('true low-quality: %d injected, %d still present (%.0f%% removed)\n',
            sum(tc$true_low_quality), sum(tc[kept,'true_low_quality']),
            100*(1-sum(tc[kept,'true_low_quality'])/sum(tc$true_low_quality))))
cat(sprintf('clustering ARI vs true cell type: %.3f\n',
            ari(as.character(Idents(seurat_obj)), tc[kept,'true_cell_type'])))
cat('cells lost to the flat nFeature/percent.mt cutoffs that were GOOD cells:',
    sum(!tc$true_doublet & !tc$true_low_quality) - sum(!tc[kept,'true_doublet'] & !tc[kept,'true_low_quality']), '\n')
cat('\nwhat the verbatim block does NOT do (per the Skill\'s own ordering rules):\n')
cat('  - ambient removal on the RAW matrix: NOT in the block (data_dir is filtered_feature_bc_matrix)\n')
cat('  - per-sample-before-merge structure: N/A, the block is single-sample\n')
cat('  - integration: NOT in the block\n')
cat('  - annotation: NOT in the block (Step 8 is in the step-by-step section only)\n')
cat('  - pseudobulk DE / differential abundance: NOT in the block\n')
cat('DONE\n')
