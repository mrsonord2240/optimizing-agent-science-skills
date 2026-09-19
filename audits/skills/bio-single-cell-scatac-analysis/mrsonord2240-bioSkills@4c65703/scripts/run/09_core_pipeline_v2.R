.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(Signac)
  library(Seurat)
  library(EnsDb.Hsapiens.v86)
  library(GenomicRanges)
})

cat('Signac version:', as.character(packageVersion('Signac')), '\n')
cat('Seurat version:', as.character(packageVersion('Seurat')), '\n')

data_dir <- 'F:/OpenScience/audits/bio-single-cell-scatac-analysis/data/reaudit_v2_20260919'
peaks <- readRDS(file.path(data_dir, 'peaks.rds'))
cell_meta <- readRDS(file.path(data_dir, 'cell_meta.rds'))
rownames(cell_meta) <- cell_meta$barcode

frag_path <- file.path(data_dir, 'fragments.tsv.bgz')

fragobj <- CreateFragmentObject(path = frag_path, cells = cell_meta$barcode, verbose = TRUE)
peak_counts <- FeatureMatrix(fragments = fragobj, features = peaks, cells = cell_meta$barcode)
cat('Peak count matrix dim:', dim(peak_counts), '\n')

chrom_assay <- CreateChromatinAssay(
  counts = peak_counts, sep = c(':', '-'), genome = 'hg38',
  fragments = fragobj, min.cells = 3, min.features = 20
)
obj <- CreateSeuratObject(counts = chrom_assay, assay = 'peaks', meta.data = cell_meta)
cat('Object after min.cells/min.features filter:', ncol(obj), 'cells x', nrow(obj), 'peaks\n')

# This is the exact documented call the P1 fix targets (GetGRangesFromEnsDb -> needs biovizBase)
annotations <- GetGRangesFromEnsDb(ensdb = EnsDb.Hsapiens.v86)
seqlevelsStyle(annotations) <- 'UCSC'
Annotation(obj) <- annotations
cat('Annotation() succeeded using GetGRangesFromEnsDb (biovizBase now a documented prerequisite)\n')

obj <- NucleosomeSignal(obj)
obj <- TSSEnrichment(obj, fast = FALSE)
cat('QC summary:\n')
print(summary(obj$nucleosome_signal))
print(summary(obj$TSS.enrichment))
print(summary(obj$nCount_peaks))

obj_qc <- subset(obj,
  nCount_peaks > quantile(obj$nCount_peaks, 0.05) &
  TSS.enrichment > quantile(obj$TSS.enrichment, 0.05)
)
cat('Cells after QC:', ncol(obj_qc), '(of', ncol(obj), ')\n')

obj_qc <- RunTFIDF(obj_qc)
obj_qc <- FindTopFeatures(obj_qc, min.cutoff = 'q0')
obj_qc <- RunSVD(obj_qc)

depth_cor_vals <- sapply(1:10, function(i) cor(Embeddings(obj_qc, 'lsi')[, i], obj_qc$nCount_peaks))
cat('Per-component depth correlation (LSI_1..10):\n')
print(round(depth_cor_vals, 3))
drop_dims <- which(abs(depth_cor_vals) > 0.75)
cat('Components exceeding |corr|>0.75 with depth (to drop):', drop_dims, '\n')
dims_use <- setdiff(1:min(10, ncol(Embeddings(obj_qc,'lsi'))), drop_dims)
cat('Dims retained for downstream analysis:', dims_use, '\n')

obj_qc <- RunUMAP(obj_qc, reduction = 'lsi', dims = dims_use)
obj_qc <- FindNeighbors(obj_qc, reduction = 'lsi', dims = dims_use)
obj_qc <- FindClusters(obj_qc, algorithm = 3, resolution = 0.5, verbose = FALSE)

cat('Clusters found:', length(unique(obj_qc$seurat_clusters)), '\n')
cat('Cross-tab clusters x true cell_type:\n')
print(table(obj_qc$seurat_clusters, obj_qc$cell_type))

ari <- function(cl1, cl2) {
  tab <- table(cl1, cl2); n <- sum(tab)
  a <- sum(choose(tab, 2)); br <- sum(choose(rowSums(tab), 2)); bc <- sum(choose(colSums(tab), 2))
  exp_idx <- br * bc / choose(n, 2); max_idx <- 0.5 * (br + bc)
  (a - exp_idx) / (max_idx - exp_idx)
}
cat('Adjusted Rand Index (cluster vs true cell type, 3-type):', round(ari(obj_qc$seurat_clusters, obj_qc$cell_type), 3), '\n')

saveRDS(obj_qc, file.path(data_dir, 'obj_qc.rds'))
cat('STAGE 2 (v2) DONE\n')
