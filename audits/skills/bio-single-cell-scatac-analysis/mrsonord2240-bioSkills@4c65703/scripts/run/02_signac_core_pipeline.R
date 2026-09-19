.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(Signac)
  library(Seurat)
  library(EnsDb.Hsapiens.v86)
  library(GenomicRanges)
})

cat('Signac version:', as.character(packageVersion('Signac')), '\n')
cat('Seurat version:', as.character(packageVersion('Seurat')), '\n')

data_dir <- 'F:/OpenScience/audits/bio-single-cell-scatac-analysis/data'
peaks <- readRDS(file.path(data_dir, 'peaks.rds'))
cell_meta <- readRDS(file.path(data_dir, 'cell_meta.rds'))
rownames(cell_meta) <- cell_meta$barcode

frag_path <- file.path(data_dir, 'fragments.tsv.bgz')

# ---- Following the skill's documented pattern: CreateFragmentObject + FeatureMatrix + CreateChromatinAssay ----
fragobj <- CreateFragmentObject(path = frag_path, cells = cell_meta$barcode, verbose = TRUE)
peak_names <- paste0(as.character(seqnames(peaks)), ':', start(peaks), '-', end(peaks))
peak_counts <- FeatureMatrix(fragments = fragobj, features = peaks, cells = cell_meta$barcode)
cat('Peak count matrix dim:', dim(peak_counts), '\n')
cat('Total counts in matrix:', sum(peak_counts), '\n')

chrom_assay <- CreateChromatinAssay(
  counts = peak_counts,
  sep = c(':', '-'),
  genome = 'hg38',
  fragments = fragobj,
  min.cells = 3,
  min.features = 20
)
obj <- CreateSeuratObject(counts = chrom_assay, assay = 'peaks', meta.data = cell_meta)
cat('Object after min.cells/min.features filter:', ncol(obj), 'cells x', nrow(obj), 'peaks\n')

# Gene annotation, as the SKILL.md pattern specifies
annotations <- GetGRangesFromEnsDb(ensdb = EnsDb.Hsapiens.v86)
seqlevelsStyle(annotations) <- 'UCSC'
Annotation(obj) <- annotations

# ---- QC metrics, per SKILL.md ----
obj <- NucleosomeSignal(obj)
obj <- TSSEnrichment(obj, fast = FALSE)
cat('QC summary:\n')
print(summary(obj$nucleosome_signal))
print(summary(obj$TSS.enrichment))
print(summary(obj$nCount_peaks))

# Data-derived QC filter (skill explicitly says: threshold from the joint distribution, not copied defaults).
# NOTE: this synthetic fragment simulator draws fragment lengths from N(200,40) with no mono/di-nucleosome
# banding, so nucleosome_signal is uninformative here (all cells >> the skill's <4 rule-of-thumb) -- an
# artifact of the synthetic generator, not the skill. Filtering uses nCount_peaks/TSS.enrichment only;
# nucleosome_signal is still computed and reported above to exercise that code path.
obj_qc <- subset(obj,
  nCount_peaks > quantile(obj$nCount_peaks, 0.05) &
  TSS.enrichment > quantile(obj$TSS.enrichment, 0.05)
)
cat('Cells after QC:', ncol(obj_qc), '(of', ncol(obj), ')\n')

# ---- TF-IDF + LSI, diagnose depth component (skill's core method) ----
obj_qc <- RunTFIDF(obj_qc)
obj_qc <- FindTopFeatures(obj_qc, min.cutoff = 'q0')
obj_qc <- RunSVD(obj_qc)

dc <- DepthCor(obj_qc, n = 10)
depth_cor_vals <- sapply(1:10, function(i) cor(Embeddings(obj_qc, 'lsi')[, i], obj_qc$nCount_peaks))
cat('Per-component depth correlation (LSI_1..10):\n')
print(round(depth_cor_vals, 3))
drop_dims <- which(abs(depth_cor_vals) > 0.75)
cat('Components exceeding |corr|>0.75 with depth (to drop):', drop_dims, '\n')
dims_use <- setdiff(1:min(10, ncol(Embeddings(obj_qc,'lsi'))), drop_dims)
if (1 %in% dims_use && !(1 %in% drop_dims)) {
  cat('NOTE: component 1 NOT flagged as depth-correlated in this run -- verifying the skills stated caveat that it is not always component 1.\n')
}
cat('Dims retained for downstream analysis:', dims_use, '\n')

# ---- Clustering on the depth-cleaned embedding ----
obj_qc <- RunUMAP(obj_qc, reduction = 'lsi', dims = dims_use)
obj_qc <- FindNeighbors(obj_qc, reduction = 'lsi', dims = dims_use)
obj_qc <- FindClusters(obj_qc, algorithm = 3, resolution = 0.5, verbose = FALSE)

cat('Clusters found:', length(unique(obj_qc$seurat_clusters)), '\n')
cat('Cross-tab clusters x true cell_type:\n')
print(table(obj_qc$seurat_clusters, obj_qc$cell_type))

ari <- function(cl1, cl2) {
  tab <- table(cl1, cl2)
  n <- sum(tab)
  a <- sum(choose(tab, 2))
  br <- sum(choose(rowSums(tab), 2))
  bc <- sum(choose(colSums(tab), 2))
  exp_idx <- br * bc / choose(n, 2)
  max_idx <- 0.5 * (br + bc)
  (a - exp_idx) / (max_idx - exp_idx)
}
cat('Adjusted Rand Index (cluster vs true cell type):', round(ari(obj_qc$seurat_clusters, obj_qc$cell_type), 3), '\n')

# ---- Gene activity (cluster-level proxy only, per skill's governing principle) ----
gene_act <- GeneActivity(obj_qc, features = c('CD3D','MS4A1','CD14','GAPDH'))
cat('Gene activity matrix dim:', dim(gene_act), '\n')
obj_qc[['ACT']] <- CreateAssayObject(counts = gene_act)
obj_qc <- NormalizeData(obj_qc, assay = 'ACT', scale.factor = median(obj_qc$nCount_ACT), verbose = FALSE)
act_by_cluster <- AverageExpression(obj_qc, assays = 'ACT', group.by = 'seurat_clusters', layer = 'data')$ACT
cat('Mean gene-activity (normalized) per cluster:\n')
print(round(act_by_cluster, 3))

saveRDS(obj_qc, file.path(data_dir, 'obj_qc.rds'))
cat('STAGE 2 DONE\n')
