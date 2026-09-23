library(Seurat)
counts <- Read10X(data.dir = 'filtered_feature_bc_matrix/')          # list when multiple feature types present
seurat_obj <- CreateSeuratObject(counts = counts, project = 'PBMC', min.cells = 3, min.features = 200)
