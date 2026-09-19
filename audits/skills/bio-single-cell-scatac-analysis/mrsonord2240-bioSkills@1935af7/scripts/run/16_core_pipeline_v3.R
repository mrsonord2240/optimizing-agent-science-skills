.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(Signac)
  library(Seurat)
  library(EnsDb.Hsapiens.v86)
  library(GenomicRanges)
})

cat('Signac version:', as.character(packageVersion('Signac')), '\n')
cat('Seurat version:', as.character(packageVersion('Seurat')), '\n')
cat('chromVAR version:', as.character(packageVersion('chromVAR')), '\n')

data_dir <- 'F:/OpenScience/audits/bio-single-cell-scatac-analysis/data/reaudit4_20260919'
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

annotations <- GetGRangesFromEnsDb(ensdb = EnsDb.Hsapiens.v86)
seqlevelsStyle(annotations) <- 'UCSC'
Annotation(obj) <- annotations
cat('Annotation() succeeded using GetGRangesFromEnsDb (biovizBase prerequisite, re-confirmed on the 4th dataset)\n')

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

table(obj_qc$cell_type)
cat('Cell type breakdown post-QC:\n')
print(table(obj_qc$cell_type))

saveRDS(obj_qc, file.path(data_dir, 'obj_qc.rds'))
cat('STAGE 2 (v3) DONE\n')
