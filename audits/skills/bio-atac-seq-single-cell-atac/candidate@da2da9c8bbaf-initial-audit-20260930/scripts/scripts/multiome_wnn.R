# Multiome WNN block from references/ecosystem-workflows.md on real 10x PBMC granulocyte-sorted 3k Multiome (full genome, counts only)
suppressPackageStartupMessages({library(Signac);library(Seurat);library(magrittr);library(ggplot2)})
SCA <- Sys.getenv("SCA"); set.seed(1)
h5 <- file.path(Sys.getenv("CACHE"),"pbmc_granulocyte_sorted_3k_filtered_feature_bc_matrix.h5")
x <- Read10X_h5(h5); print(names(x)); print(sapply(x,dim))
obj <- CreateSeuratObject(x[["Gene Expression"]], assay="RNA")
obj[["ATAC"]] <- CreateChromatinAssay(x[["Peaks"]], sep=c(":","-"), genome="hg38", min.cells=10)
obj[["pct_mt"]] <- PercentageFeatureSet(obj, pattern="^MT-")
obj <- subset(obj, nCount_RNA>1000 & nCount_RNA<25000 & nCount_ATAC>1000 & nCount_ATAC<100000 & pct_mt<20)
cat("cells after QC", ncol(obj), "\n")
# --- as documented ---
DefaultAssay(obj) <- 'RNA'
obj <- NormalizeData(obj) %>% FindVariableFeatures() %>% ScaleData() %>% RunPCA()
DefaultAssay(obj) <- 'ATAC'
obj <- RunTFIDF(obj) %>% FindTopFeatures(min.cutoff='q0') %>% RunSVD()
cat("depth cor LSI1..3:", round(sapply(1:3,function(i) cor(Embeddings(obj,"lsi")[,i], log10(obj$nCount_ATAC))),2), "\n")
obj <- FindMultiModalNeighbors(obj, reduction.list=list('pca','lsi'), dims.list=list(1:30,2:30))
obj <- RunUMAP(obj, nn.name='weighted.nn', reduction.name='wnn.umap')
obj <- FindClusters(obj, graph.name="wsnn", algorithm=3, resolution=0.5, verbose=FALSE)
# ATAC-only clustering with dims 2:30 vs 1:30 (Skill's key claim)
obj <- FindNeighbors(obj, reduction="lsi", dims=2:30, graph.name="atac_2_30"); obj <- FindClusters(obj, graph.name="atac_2_30", algorithm=4, resolution=0.5, verbose=FALSE)
obj$atac_c <- obj$seurat_clusters
obj <- RunUMAP(obj, reduction="lsi", dims=2:30, reduction.name="umap.atac2", verbose=FALSE)
obj <- RunUMAP(obj, reduction="lsi", dims=1:30, reduction.name="umap.atac1", verbose=FALSE)
cat("modality weights: RNA", round(summary(obj$RNA.weight),3), "\nATAC", round(summary(obj$ATAC.weight),3), "\n")
cat("wnn clusters:", table(obj$wsnn_res.0.5), "\n")
ari <- function(a,b){t<-table(a,b);n<-sum(t);s<-function(x)sum(choose(x,2));ex<-s(rowSums(t))*s(colSums(t))/choose(n,2);(s(t)-ex)/(0.5*(s(rowSums(t))+s(colSums(t)))-ex)}
DefaultAssay(obj) <- 'RNA'; obj <- FindNeighbors(obj, reduction="pca", dims=1:30, graph.name="rna_g"); obj <- FindClusters(obj, graph.name="rna_g", resolution=0.5, verbose=FALSE)
cat("ARI(wnn,RNA)", round(ari(obj$wsnn_res.0.5, obj$seurat_clusters),3), " ARI(wnn,ATAC 2:30)", round(ari(obj$wsnn_res.0.5, obj$atac_c),3), "\n")
# density-gradient check: cor of UMAP1/2 with depth for dims 1:30 vs 2:30
gr <- function(nm){e<-Embeddings(obj,nm);max(abs(cor(e,log10(obj$nCount_ATAC))))}
cat("max|cor(UMAP,depth)| dims1:30", round(gr("umap.atac1"),3), " dims2:30", round(gr("umap.atac2"),3), "\n")
# markers sanity: monocyte vs T-cell by RNA
obj$wnn <- obj$wsnn_res.0.5
png(file.path(Sys.getenv("AUDOUT"),"multiome_wnn_umap.png"), 1200, 400, res=110)
print(DimPlot(obj, reduction="wnn.umap", group.by="wnn", label=TRUE) + DimPlot(obj, reduction="umap.atac1", group.by="wnn") + DimPlot(obj, reduction="umap.atac2", group.by="wnn"))
dev.off()
DefaultAssay(obj) <- "RNA"
m <- c("CD3E","CD14","MS4A1","NKG7","GNLY","CST3")
print(round(sapply(m, function(g) tapply(GetAssayData(obj,assay="RNA",layer="data")[g,], obj$wnn, mean)),2))
saveRDS(obj, file.path(SCA,"work/multiome_wnn.rds"))
