# Re-draws the shipped top-50 heatmap call as PNG from the saved CSVs to inspect label legibility
library(pheatmap)
z <- as.matrix(read.csv('bulk_A/chromvar_deviations.csv', row.names=1, check.names=FALSE))
v <- read.csv('bulk_A/chromvar_variability.csv', row.names=1)
lab <- setNames(paste0(rownames(v),' (',v$name,')'), rownames(v))
top50 <- lab[head(rownames(v),50)]
info <- data.frame(Condition=factor(rep(c('control','treated'),each=3)), row.names=colnames(z))
png('bulk_A/heat.png', 1000, 1200, res=100)
pheatmap(z[top50,], annotation_col=info, scale='row', clustering_method='ward.D2', fontsize_row=8)
dev.off()
