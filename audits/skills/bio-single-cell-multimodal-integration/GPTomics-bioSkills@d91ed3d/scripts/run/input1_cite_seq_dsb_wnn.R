# Input 1 (Canonical): "My ADT clusters look like background smears; denoise with DSB
# using empty droplets, then run WNN and show me the modality weights."
# Follows SKILL.md's "CITE-seq: Denoise ADT, Then Joint Embed (Seurat)" pattern verbatim,
# on synthetic data with a known ambient background + 3 known cell populations.
.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({
  library(dsb)
  library(Seurat)
})

d <- readRDS("data/synthetic_cite_seq.rds")

adt_cells <- d$adt_cells
adt_empty <- d$adt_raw[, setdiff(colnames(d$adt_raw), colnames(adt_cells))]

# isotype.control.name.vec must name the ACTUAL isotype rows -- SKILL.md's own comment warns the
# regex it ships (grep('[Ii]sotype|IgG', ...)) can miss real isotype names. Test that regex here.
iso_regex_hits <- grep('[Ii]sotype|IgG', rownames(adt_cells), value = TRUE)
cat("Isotype regex matched:", paste(iso_regex_hits, collapse = ", "), "\n")

adt_dsb <- DSBNormalizeProtein(
  cell_protein_matrix = adt_cells,
  empty_drop_matrix = adt_empty,
  denoise.counts = TRUE,
  use.isotype.control = TRUE,
  isotype.control.name.vec = iso_regex_hits
)
cat("DSB output dims:", paste(dim(adt_dsb), collapse = " x "), "\n")
cat("DSB output range:", round(range(adt_dsb), 2), "\n")

obj <- CreateSeuratObject(counts = d$rna_cells, assay = 'RNA', min.cells = 0, min.features = 0)
obj[['ADT']] <- CreateAssay5Object(data = adt_dsb)
obj$truth <- d$truth[colnames(obj)]

DefaultAssay(obj) <- 'RNA'
obj <- NormalizeData(obj) |> FindVariableFeatures() |> ScaleData() |> RunPCA(reduction.name = 'pca', verbose = FALSE)

DefaultAssay(obj) <- 'ADT'
VariableFeatures(obj) <- rownames(obj[['ADT']])
obj <- ScaleData(obj) |> RunPCA(reduction.name = 'apca', npcs = min(18, nrow(obj[['ADT']]) - 1), verbose = FALSE)

obj <- FindMultiModalNeighbors(obj, reduction.list = list('pca', 'apca'),
                                dims.list = list(1:min(30, ncol(obj[['pca']])), 1:min(18, ncol(obj[['apca']]))),
                                verbose = FALSE)
obj <- FindClusters(obj, graph.name = 'wsnn', algorithm = 3, verbose = FALSE)

cat("\n=== Cluster x truth cross-tab (run 1) ===\n")
print(table(obj$seurat_clusters, obj$truth))

cat("\n=== RNA.weight summary by truth label (run 1) ===\n")
print(tapply(obj$RNA.weight, obj$truth, summary))

# Determinism check: identical inputs, identical downstream call -- rerun the stochastic steps
obj2 <- obj
obj2 <- FindMultiModalNeighbors(obj2, reduction.list = list('pca', 'apca'),
                                 dims.list = list(1:min(30, ncol(obj2[['pca']])), 1:min(18, ncol(obj2[['apca']]))),
                                 verbose = FALSE)
obj2 <- FindClusters(obj2, graph.name = 'wsnn', algorithm = 3, verbose = FALSE)
identical_clusters <- identical(as.character(obj$seurat_clusters), as.character(obj2$seurat_clusters))
cat("\nDeterminism check -- identical clusters across 2 runs, same session:", identical_clusters, "\n")

saveRDS(obj, "run/input1_output.rds")
cat("\nStatus: COMPLETED\n")
