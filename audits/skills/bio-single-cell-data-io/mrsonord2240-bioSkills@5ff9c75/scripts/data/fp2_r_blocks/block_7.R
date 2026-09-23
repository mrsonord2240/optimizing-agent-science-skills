scale_data <- as.matrix(LayerData(seurat_obj, layer = 'scale.data'))
saveRDS(scale_data, 'scale_data.rds')   # reload later with readRDS(); or write.csv(scale_data, 'scale_data.csv')
