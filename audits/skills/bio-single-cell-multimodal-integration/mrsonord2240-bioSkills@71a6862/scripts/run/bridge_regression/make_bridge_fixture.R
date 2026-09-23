.libPaths(c('F:/OpenScience/audit-envs/single-cell-transcriptomics-analyst/R-lib', .libPaths()))
suppressPackageStartupMessages({ library(Seurat); library(Signac) })

set.seed(923)
d <- readRDS('F:/OpenScience/audits/bio-single-cell-multimodal-integration/data/synthetic_multiome.rds')
ref_idx <- 1:150
bridge_idx <- 151:300

ref <- CreateSeuratObject(counts = d$rna_cells[, ref_idx], assay = 'RNA')
ref$celltype <- d$truth[ref_idx]
ref <- NormalizeData(ref, verbose = FALSE)
ref <- FindVariableFeatures(ref, nfeatures = 300, verbose = FALSE)
ref <- ScaleData(ref, verbose = FALSE)
ref <- RunPCA(ref, npcs = 20, verbose = FALSE)
ref <- RunUMAP(ref, dims = 1:20, return.model = TRUE, verbose = FALSE)

bridge <- CreateSeuratObject(counts = d$rna_cells[, bridge_idx], assay = 'RNA')
bridge[['ATAC']] <- CreateAssayObject(counts = d$atac_cells[, bridge_idx])
DefaultAssay(bridge) <- 'RNA'
bridge <- NormalizeData(bridge, verbose = FALSE)
bridge <- FindVariableFeatures(bridge, nfeatures = 300, verbose = FALSE)
bridge <- ScaleData(bridge, verbose = FALSE)
bridge <- RunPCA(bridge, npcs = 20, verbose = FALSE)
DefaultAssay(bridge) <- 'ATAC'
bridge <- RunTFIDF(bridge, verbose = FALSE)
bridge <- FindTopFeatures(bridge, min.cutoff = 'q0', verbose = FALSE)
bridge <- RunSVD(bridge, n = 20, verbose = FALSE)

query <- CreateSeuratObject(counts = d$atac_cells[, ref_idx], assay = 'ATAC')
colnames(query) <- paste0('QUERY_', colnames(query))
query$truth <- unname(d$truth[ref_idx])
query <- RunTFIDF(query, verbose = FALSE)

saveRDS(ref, 'bridge_ref.rds')
saveRDS(bridge, 'bridge_multi.rds')
saveRDS(query, 'bridge_query.rds')
cat('BRIDGE_FIXTURE', ncol(ref), ncol(bridge), ncol(query), '\n')
