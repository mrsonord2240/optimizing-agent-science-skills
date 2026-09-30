# Skill references/single-cell.md Signac chain on real 10x PBMC 5k (chr1:1-30Mb slice)
if (nzchar(Sys.getenv("SIGNAC_LIB"))) .libPaths(c(Sys.getenv("SIGNAC_LIB"), .libPaths()))
suppressPackageStartupMessages({library(Signac);library(Seurat);library(JASPAR2024);library(TFBSTools);library(BSgenome.Hsapiens.UCSC.hg38);library(RSQLite);library(GenomicRanges);library(Matrix)})
D <- Sys.getenv("ATACDATA"); O <- file.path(Sys.getenv("MD"),"work/signac"); dir.create(O,recursive=TRUE,showWarnings=FALSE)
cat("Signac",as.character(packageVersion("Signac")),"Seurat",as.character(packageVersion("Seurat")),"chromVAR",as.character(packageVersion("chromVAR")),"\n")
m <- Read10X_h5(file.path(D,"scatac/outs/filtered_peak_bc_matrix.h5"))
keep <- grepl("^chr1:",rownames(m)); m <- m[keep,]
gr <- StringToGRanges(rownames(m), sep=c(":","-")); m <- m[end(gr)<=30e6,]; m <- m[, Matrix::colSums(m)>=500]
cat("matrix",dim(m),"\n")
ca <- CreateChromatinAssay(m, sep=c(":","-"), fragments=file.path(D,"scatac/outs/fragments.tsv.gz"), genome="hg38")
obj <- CreateSeuratObject(ca, assay="ATAC")
obj <- RunTFIDF(obj); obj <- FindTopFeatures(obj, min.cutoff=20); obj <- RunSVD(obj)
obj <- FindNeighbors(obj, reduction="lsi", dims=2:20); obj <- FindClusters(obj, algorithm=3, resolution=0.3, verbose=FALSE)
print(table(obj$seurat_clusters))
# --- exactly as Skill ---
jaspar2024 <- JASPAR2024::JASPAR2024()
sq <- dbConnect(SQLite(), db(jaspar2024))
pfm <- getMatrixSet(sq, opts=list(collection='CORE', tax_group='vertebrates'))
cat("pfm",length(pfm),"\n")
seurat_obj <- AddMotifs(obj, genome=BSgenome.Hsapiens.UCSC.hg38, pfm=pfm)
seurat_obj <- RunChromVAR(seurat_obj, genome=BSgenome.Hsapiens.UCSC.hg38, new.assay.name='chromvar')
DefaultAssay(seurat_obj) <- 'chromvar'
markers <- FindAllMarkers(seurat_obj, only.pos=TRUE, mean.fxn=rowMeans, fc.name='avg_diff')
cat("markers cols:",paste(colnames(markers),collapse=","),"\n")
markers$tf <- ConvertMotifID(seurat_obj[['ATAC']], id=markers$gene)
print(head(markers[order(markers$p_val_adj),c("cluster","tf","avg_diff","p_val_adj")],25))
z <- GetAssayData(seurat_obj,layer="data"); cat("chromvar assay",dim(z),"NA",sum(is.na(z)),"range",range(z),"\n")
saveRDS(markers[,1:7], file.path(O,"markers.rds"))
# top per cluster
for (cl in levels(markers$cluster)) { s <- markers[markers$cluster==cl,]; s<-s[order(s$p_val_adj),]; cat("cluster",cl,":",paste(head(s$tf,8),collapse=" "),"\n") }
