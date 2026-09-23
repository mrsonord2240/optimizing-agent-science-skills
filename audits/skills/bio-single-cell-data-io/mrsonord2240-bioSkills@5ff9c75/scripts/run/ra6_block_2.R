counts <- LayerData(seurat_obj, layer = 'counts')      # v5; GetAssayData(slot=) is the superseded v4 form
counts <- seurat_obj[['RNA']]$counts                   # shorthand
merged <- merge(obj1, y = c(obj2, obj3), add.cell.ids = c('S1', 'S2', 'S3'))
merged <- JoinLayers(merged)                           # merge() splits layers (counts.1, counts.2); rejoin first
