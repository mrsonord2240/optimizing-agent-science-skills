# Input 4 (Variant B): "Process my 10x Multiome RNA+ATAC data: PCA on RNA, TF-IDF/LSI on
# ATAC, drop depth-correlated components, then joint WNN clustering."
# Follows SKILL.md's "Multiome (RNA + ATAC, same cell)" pattern verbatim.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(Signac)
  library(Seurat)
})

d <- readRDS("data/synthetic_multiome.rds")

obj <- CreateSeuratObject(counts = d$rna_cells, assay = 'RNA')
obj[['ATAC']] <- CreateAssayObject(counts = d$atac_cells)
obj$truth <- d$truth

DefaultAssay(obj) <- 'RNA'
obj <- NormalizeData(obj) |> FindVariableFeatures() |> ScaleData() |> RunPCA(verbose = FALSE)

DefaultAssay(obj) <- 'ATAC'
obj <- RunTFIDF(obj, verbose = FALSE) |> FindTopFeatures(min.cutoff = 'q0') |> RunSVD(verbose = FALSE)
dc <- DepthCor(obj)
cat("\n=== DepthCor correlations (LSI component vs sequencing depth) ===\n")
print(dc$data)

# SKILL.md: "dims = 2:30 drops LSI_1 ONLY if DepthCor confirms it tracks depth (usually true,
# not guaranteed)". Check that programmatically rather than blindly dropping LSI_1.
lsi1_cor <- dc$data$counts[dc$data$Component == 1]
cat("LSI_1 correlation with depth:", lsi1_cor, "-> drop LSI_1?", abs(lsi1_cor) > 0.5, "\n")

obj <- FindMultiModalNeighbors(obj, reduction.list = list('pca', 'lsi'),
                                dims.list = list(1:min(30, ncol(obj[['pca']])), 2:min(30, ncol(obj[['lsi']]))),
                                verbose = FALSE)
obj <- RunUMAP(obj, nn.name = 'weighted.nn', reduction.name = 'wnn.umap', verbose = FALSE)
obj <- FindClusters(obj, graph.name = 'wsnn', algorithm = 3, verbose = FALSE)

cat("\n=== Cluster x truth cross-tab ===\n")
print(table(obj$seurat_clusters, obj$truth))

saveRDS(obj, "run/input4_output.rds")
cat("\nStatus: COMPLETED\n")
