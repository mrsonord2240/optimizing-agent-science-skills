if (nzchar(Sys.getenv("SIGNAC_LIB"))) .libPaths(c(Sys.getenv("SIGNAC_LIB"), .libPaths()))
suppressPackageStartupMessages({library(Signac);library(Seurat);library(JASPAR2024);library(TFBSTools);library(BSgenome.Hsapiens.UCSC.hg38);library(RSQLite);library(GenomicRanges);library(Matrix)})
D <- Sys.getenv("ATACDATA")
cat("Signac",as.character(packageVersion("Signac")),"chromVAR",as.character(packageVersion("chromVAR")),"
")
m <- Read10X_h5(file.path(D,"scatac/outs/filtered_peak_bc_matrix.h5"))
m <- m[grepl("^chr1:",rownames(m)),]
gr <- StringToGRanges(rownames(m), sep=c(":","-")); m <- m[end(gr)<=30e6,]; m <- m[, Matrix::colSums(m)>=500]
cat("matrix",dim(m),"
")
ca <- CreateChromatinAssay(m, sep=c(":","-"), fragments=file.path(D,"scatac/outs/fragments.tsv.gz"), genome="hg38")
obj <- CreateSeuratObject(ca, assay="ATAC")
obj <- RunTFIDF(obj); obj <- FindTopFeatures(obj, min.cutoff=20); obj <- RunSVD(obj)
obj <- FindNeighbors(obj, reduction="lsi", dims=2:20); obj <- FindClusters(obj, algorithm=3, resolution=0.3, verbose=FALSE)
print(table(obj$seurat_clusters)); seurat_obj <- obj
library(Signac); library(Seurat); library(JASPAR2024); library(TFBSTools)
library(BSgenome.Hsapiens.UCSC.hg38); library(RSQLite)
library(chromVAR); library(SummarizedExperiment)

# Assume `seurat_obj` has an ATAC assay with consensus peaks
# JASPAR2024 + TFBSTools workaround (see TFBSTools issue #39):
jaspar2024 <- JASPAR2024::JASPAR2024()
sq <- dbConnect(SQLite(), db(jaspar2024))
pfm <- getMatrixSet(sq, opts=list(collection='CORE', tax_group='vertebrates'))
seurat_obj <- AddMotifs(seurat_obj, genome=BSgenome.Hsapiens.UCSC.hg38, pfm=pfm)

# chromVAR on the ATAC counts
counts <- GetAssayData(seurat_obj, assay='ATAC', layer='counts')
se <- SummarizedExperiment(assays=list(counts=counts), rowRanges=granges(seurat_obj[['ATAC']]))
se <- addGCBias(se, genome=BSgenome.Hsapiens.UCSC.hg38)
# empty peaks and peaks with undefined GC (assembly gaps, NaN bias) break background matching
keep <- Matrix::rowSums(counts) > 0 & !is.na(rowData(se)$bias)
se <- se[keep, ]
set.seed(2024)                                   # background sampling is random; report the seed
bg <- getBackgroundPeaks(se)
dev <- computeDeviations(se, annotations=GetMotifData(seurat_obj[['ATAC']], slot='data')[keep, ],
                         background_peaks=bg)
z <- deviationScores(dev)                        # motifs x cells
cat('NA z-scores:', sum(is.na(z)), '\n')       # expect 0; see the ArchR note if not
seurat_obj[['chromvar']] <- CreateAssayObject(data=z)
DefaultAssay(seurat_obj) <- 'chromvar'

# Per-cluster differential motifs.
# `mean.fxn` is the standard FindAllMarkers/FindMarkers control for the per-feature summary.
# `fc.name` controls the output column name and is accepted by Seurat 4.x/5.x; if it errors,
# fall back to renaming the output column post-hoc.
markers <- FindAllMarkers(seurat_obj, only.pos=TRUE, mean.fxn=rowMeans, fc.name='avg_diff')

markers$tf <- ConvertMotifID(seurat_obj[['ATAC']], id=markers$gene)
cat("markers cols:",paste(colnames(markers),collapse=","),"
")
zz <- GetAssayData(seurat_obj,layer="data"); cat("chromvar assay",dim(zz),"NA",sum(is.na(zz)),"range",range(zz),"
")
for (cl in levels(markers$cluster)) { s <- markers[markers$cluster==cl,]; s<-s[order(s$p_val_adj),]; cat("cluster",cl,":",paste(head(s$tf,8),collapse=" "),"
") }
write.csv(markers,file.path(Sys.getenv("OUTD"),"markers.csv"))
